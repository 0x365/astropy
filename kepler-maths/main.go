package main

import (
	"fmt"
	"os"
	"strconv"

	"github.com/schollz/progressbar/v3"
)

const ITERATIONS = 2880 // 3600 * 24
const APPLY_SUBSET = true
const START_TIME = 1709222233
const DIS_SQ = 500 * 500
const LAG_TIME = 0

type TLE struct {
	name string
	l1   string
	l2   string
}

type Coord struct {
	X float64
	Y float64
	Z float64
}

func main() {

	os.Mkdir("data", 0755)
	// os.Mkdir("data/interactions", 0755)

	var times [][]string
	var min_time int
	var interactions [][][]bool
	var original_interactions [][][]bool
	var sat_coords [][]Coord
	var single_sim_coords []Coord
	var max_completness int

	fmt.Println("Creating real satellites")
	sat_coords_real := generateRealSats()
	fmt.Println("Generated", len(sat_coords_real), "real satellites")

	fmt.Println("Building Combinations")
	max_val := len(sat_coords_real) + 1
	bar := progressbar.Default(int64(max_val))
	// Generate first set
	var comb_list [][]int
	var i1, i2, i3 int
	for i1 = 0; i1 < max_val-1; i1++ {
		for i2 = 0; i2 < max_val-1; i2++ {
			for i3 = i2 + 1; i3 < max_val-1; i3++ {
				if i1 != i2 && i1 != i3 && i2 != i3 {
					comb_list = append(comb_list, []int{i1, i2, i3, max_val - 1})
				}
			}
		}
		bar.Add(1)
	}
	// var i1, i2, i3, i4 int
	// for i1 = 0; i1 < max_val; i1++ {
	// 	for i2 = 0; i2 < max_val; i2++ {
	// 		for i3 = i2 + 1; i3 < max_val; i3++ {
	// 			for i4 = i3 + 1; i4 < max_val; i4++ {
	// 				//if STARTING_SAT != i1 && STARTING_SAT != i2 && STARTING_SAT != i3 && i1 != i2 && i1 != i3 && i2 != i3 {
	// 				if i4 != i1 && i4 != i2 && i4 != i3 && i1 != i2 && i1 != i3 && i2 != i3 {
	// 					if i2 == max_val-1 || i3 == max_val-1 || i4 == max_val-1 {
	// 						comb_list = append(comb_list, []int{i1, i2, i3, i4})
	// 					}
	// 				}
	// 			}
	// 		}
	// 		bar.Add(1)
	// 	}
	// }

	fmt.Println(len(comb_list))

	var INC_li []float64    // INC - 0 to 180
	var RAAN_li []float64   // RAAN - 0 to 360
	var ECC_li []float64    // ECC - 1 to 250000
	var ARGP_li []float64   // ARGP - 0 to 360
	var ANOM_li []float64   // ANOM - 0 to 360
	var MOTION_li []float64 // MOTION - 11.25 to 16

	// INC_li = []float64{0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180}
	RAAN_li = []float64{0}
	ECC_li = []float64{1, 100, 250, 500, 1000, 1500, 2500, 5000}
	// ECC_li = []float64{1}
	// ARGP_li = []float64{0}
	// ANOM_li = []float64{0}
	// MOTION_li = []float64{0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180}

	var i int
	top_i := 10
	for i = 0; i <= top_i; i++ {
		ARGP_li = append(ARGP_li, 0.0+((360.0-0.0)/float64(top_i))*float64(i))
		INC_li = append(INC_li, 0.0+((180.0-0.0)/float64(top_i))*float64(i))
		ANOM_li = append(ANOM_li, 0.0+((360.0-0.0)/float64(top_i))*float64(i))
		MOTION_li = append(MOTION_li, 11.25+((16.0-11.25)/float64(top_i))*float64(i))
	}

	fmt.Println("Generating bulk of interactions")
	original_interactions = getInteractionsBinary(sat_coords_real)
	var c int

	var total_runs int = len(INC_li) * len(RAAN_li) * len(ECC_li) * len(ARGP_li) * len(ANOM_li) * len(MOTION_li)
	fmt.Println("Starting grid search")
	bar = progressbar.Default(int64(total_runs))

	for _, RAAN := range RAAN_li {
		for _, ECC := range ECC_li {
			for _, ARGP := range ARGP_li {
				for _, ANOM := range ANOM_li {
					for _, INC := range INC_li {
						for _, MOTION := range MOTION_li {
							c += 1
							// fmt.Println(c, "out of", total_runs, "---", INC, RAAN, ECC, ARGP, ANOM, MOTION)

							single_sim_coords = generateSimSats(INC, RAAN, ECC, ARGP, ANOM, MOTION)
							sat_coords = combineCoords(sat_coords_real, [][]Coord{single_sim_coords})

							interactions = specialCombine(original_interactions, sat_coords, max_val-1) // Maybe add +1 to len()

							// saveInteractions(sat_coords)

							// Genetic algorithm find fastest (Maybe brute force?)

							min_time, _, comb_list, max_completness = getConsensusTime(interactions, comb_list)

							times = append(times, []string{strconv.Itoa(min_time), strconv.Itoa(max_completness),
								fmt.Sprintf("%08.4f", float64(INC)),
								fmt.Sprintf("%08.4f", float64(RAAN)),
								fmt.Sprintf("%07.0f", float64(ECC)),
								fmt.Sprintf("%08.4f", float64(ARGP)),
								fmt.Sprintf("%08.4f", float64(ANOM)),
								fmt.Sprintf("%10.8f", float64(MOTION))})

							bar.Add(1)

						}
						writeFile2D(times, "data/grid_search2.csv")
					}
				}

			}
		}
	}
}

func specialCombine(interactions_all [][][]bool, sat_coords [][]Coord, extra_id int) [][][]bool {
	var extra_interaction [][]bool = getInteractionsSmall(sat_coords, extra_id)
	interactions_all = append(interactions_all, extra_interaction)
	var i int
	for i = 0; i < len(extra_interaction); i++ {
		if i != extra_id {
			interactions_all[i] = append(interactions_all[i], extra_interaction[i])
		}
	}
	return interactions_all
}

func getConsensusTime(interactions [][][]bool, comb_list [][]int) (min_time int, best_set []int, good_comb [][]int, max_completeness int) {
	// fmt.Println("Building initial combinations")

	min_time = 9999999999999
	var time int
	var completeness int
	// fmt.Println("Start Consensus Measure")
	var num_combs int = len(comb_list)
	var num_sats int = len(interactions)
	// bar := progressbar.Default(int64(num_combs))
	var i, j int
	var passed bool
	for i = 0; i < num_combs; i++ {
		time, completeness = consensus_time3(comb_list[i], LAG_TIME, interactions)
		if completeness > max_completeness {
			max_completeness = completeness
		}
		if time > 4 {
			good_comb = append(good_comb, comb_list[i])
			if time < min_time {
				min_time = time
				best_set = comb_list[i]
			}
		} else {
			passed = true
			for j = 0; j < len(comb_list[i]); j++ {
				if num_sats-1 == comb_list[i][j] {
					passed = false
					break
				}
			}
			if !passed {
				good_comb = append(good_comb, comb_list[i])
			}
		}
		// bar.Add(1)
	}
	return min_time, best_set, good_comb, max_completeness
}

func consensus_time3(bin_li []int, LAG_TIME int, interactions [][][]bool) (int, int) {

	primary := 0

	num_sats := len(bin_li)

	var pass bool
	var max_time, completeness int
	var t_local []int

	var i int
	for i = 0; i < num_sats; i++ {
		t_local = append(t_local, 0)
	}

	var sat_data_big [][][]bool
	var temp [][]bool
	var j int
	for i = 0; i < num_sats; i++ {
		temp = nil
		for j = 0; j < num_sats; j++ {
			temp = append(temp, interactions[bin_li[i]][bin_li[j]])
		}
		sat_data_big = append(sat_data_big, temp)
	}

	// ################# Start Consensus
	pass, _, t_local, completeness = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if !pass {
		return 1, completeness
	}

	// Decision Lag
	for i := 0; i < num_sats; i++ {
		t_local[i] += LAG_TIME
	}

	pass, _, t_local, completeness = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if !pass {
		return 2, completeness
	}

	pass, _, t_local, completeness = consensus_commit(t_local, sat_data_big, num_sats, completeness)
	if !pass {
		return 3, completeness
	}

	pass, max_time, completeness = consensus_reply(t_local, sat_data_big, num_sats, primary, completeness)
	if pass {
		return max_time, completeness
	} else {
		return 4, completeness
	}
}

func combineCoords(coords_li1 [][]Coord, coords_li2 [][]Coord) [][]Coord {
	for i := 0; i < len(coords_li2); i++ {
		coords_li1 = append(coords_li1, coords_li2[i])
	}
	return coords_li1
}
