// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package main

import (
	"C"
)
import (
	"fmt"
	"math"
	"unsafe"
)

func main() {}

func convert_to_n_by_rest(grid []float64, n_div int) [][]float64 {

	var depth int
	// Calculate the number of rows (n) based on the length of the flat grid
	depth = int(math.Ceil(float64(len(grid)) / float64(n_div)))

	// Create the 2D slice
	result := make([][]float64, depth)

	// Fill the 2D slice
	for i := 0; i < depth; i++ {
		// Determine the starting and ending index for the row
		start := i * n_div
		end := start + n_div
		if end > len(grid) {
			end = len(grid) // Handle the case where we exceed the grid length
		}
		// Slice the grid and append to result
		result[i] = grid[start:end]
	}

	return result
}

func convert_to_n_by_n_by_rest(grid []float64, n int) [][][]float64 {

	var depth int
	var i, j, k int

	depth = len(grid) / (n * n)

	// Create a 3D slice with dimensions [cols][rows][depth]
	var temp []float64
	var temp2 [][]float64
	var result [][][]float64

	for i = 0; i < n; i++ {
		temp2 = [][]float64{}
		for j = 0; j < n; j++ {
			temp = []float64{}
			for k = 0; k < depth; k++ {
				temp = append(temp, grid[k+(i*n*depth)+(j*depth)])
			}
			temp2 = append(temp2, temp)
		}
		result = append(result, temp2)
	}

	return result
}

func consensus(comm [][][]int, ec []int, grid [][][]float64) (bool, int) {
	var i int
	var j int
	var c int
	var c2 int
	var t int
	var found bool
	var final_time int
	t_local := []float64{0, 0, 0, 0}
	t_local_next := []float64{0, 0, 0, 0}
	for c = 0; c < len(comm); c++ {
		copy(t_local_next, t_local)
		for c2 = 0; c2 < len(comm[c]); c2++ {
			found = false
			i = comm[c][c2][0]
			j = comm[c][c2][1]

			for t = 0; t < len(grid[ec[i]][ec[j]]); t++ {

				if grid[ec[i]][ec[j]][t] >= t_local[i] {
					found = true
					if grid[ec[i]][ec[j]][t] > t_local_next[j] {
						t_local_next[j] = grid[ec[i]][ec[j]][t]
					}
					break
				} else if grid[ec[i]][ec[j]][t] == -1 {
					break
				}
			}
			if !found {
				return false, -1
			}
		}
		copy(t_local, t_local_next)
		// fmt.Println(t_local)
	}
	final_time = 0
	for t = 0; t < 4; t++ {
		if final_time < int(t_local[t]) {
			final_time = int(t_local[t])
		}
	}
	return true, final_time
}

//export consensus_completeness_per
func consensus_completeness_per(combs_raw *float64, combs_n int64, grid_raw *float64, grid_n int64, num_sats int64) C.int {

	var grid_flat []float64
	var combs_flat []float64

	var combs [][]float64
	var grid [][][]float64

	var comm [][][][]int
	var ec [][]int

	var completed bool
	var timer int

	var i int
	var j int
	var c int
	var timer_all int

	combs_flat = unsafe.Slice(combs_raw, combs_n)

	grid_flat = unsafe.Slice(grid_raw, grid_n)

	combs = convert_to_n_by_rest(combs_flat, 3)

	for i = 0; i < len(combs); i++ {
		var temp = []int{0}
		for j = 0; j < len(combs[i]); j++ {
			temp = append(temp, int(combs[i][j]))
		}
		if len(temp) == 4 {
			ec = append(ec, temp)
		}
	}

	grid = convert_to_n_by_n_by_rest(grid_flat, int(num_sats))

	comm = [][][][]int{
		{
			{{0, 1}, {0, 2}, {0, 3}},
			{{1, 0}, {1, 2}, {1, 3}, {2, 0}, {2, 1}, {2, 3}, {3, 0}, {3, 1}, {3, 2}},
			{{0, 1}, {0, 2}, {0, 3}, {1, 0}, {1, 2}, {1, 3}, {2, 0}, {2, 1}, {2, 3}, {3, 0}, {3, 1}, {3, 2}},
			{{1, 0}, {2, 0}, {3, 0}},
		},
		{
			{{1, 0}, {1, 2}, {1, 3}},
			{{0, 1}, {0, 2}, {0, 3}, {2, 0}, {2, 1}, {2, 3}, {3, 0}, {3, 1}, {3, 2}},
			{{1, 0}, {1, 2}, {1, 3}, {0, 1}, {0, 2}, {0, 3}, {2, 0}, {2, 1}, {2, 3}, {3, 0}, {3, 1}, {3, 2}},
			{{0, 1}, {2, 1}, {3, 1}},
		},
		{
			{{2, 0}, {2, 1}, {2, 3}},
			{{0, 1}, {0, 2}, {0, 3}, {1, 0}, {1, 2}, {1, 3}, {3, 0}, {3, 1}, {3, 2}},
			{{2, 0}, {2, 1}, {2, 3}, {1, 0}, {1, 2}, {1, 3}, {0, 1}, {0, 2}, {0, 3}, {3, 0}, {3, 1}, {3, 2}},
			{{0, 2}, {1, 2}, {3, 2}},
		},
		{
			{{3, 0}, {3, 1}, {3, 2}},
			{{0, 1}, {0, 2}, {0, 3}, {1, 0}, {1, 2}, {1, 3}, {2, 0}, {2, 1}, {2, 3}},
			{{3, 0}, {3, 1}, {3, 2}, {1, 0}, {1, 2}, {1, 3}, {0, 1}, {0, 2}, {0, 3}, {2, 0}, {2, 1}, {2, 3}},
			{{0, 3}, {1, 3}, {2, 3}},
		},
	}

	var k int
	var kk int
	var uni []int
	var already bool

	c = 0
	timer_all = 0

	for j = 0; j < len(comm); j++ {
		for i = 0; i < len(ec); i++ {
			completed, timer = consensus(comm[j], ec[i], grid)
			if completed {
				c += 1
				timer_all += timer

				for kk = 0; kk < len(ec[i]); kk++ {
					already = false
					for k = 0; k < len(uni); k++ {
						if ec[i][kk] == uni[k] {
							already = true
						}
					}
					if !already {
						uni = append(uni, ec[i][kk])
					}
				}

			}
		}
	}

	// if c == 0 {
	// 	timer_all = 2881
	// } else {
	// 	timer_all = int(float64(timer_all) / float64(c))
	// }
	fmt.Println(len(uni), num_sats)

	return C.int(c) //C.int(timer_all)
}
