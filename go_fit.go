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
	// Calculate the number of rows (n) based on the length of the flat grid
	n := int(math.Ceil(float64(len(grid)) / float64(n_div)))

	// Create the 2D slice
	result := make([][]float64, n)

	// Fill the 2D slice
	for i := 0; i < n; i++ {
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
	totalElements := len(grid)

	// Calculate the missing dimension (depth)
	// if totalElements%(n*n) != 0 {
	// 	return nil, fmt.Errorf("length of flat array (%d) is not divisible by rows*cols (%d*%d)", totalElements, rows, cols)
	// }
	depth := totalElements / (n * n)

	// Create a 3D slice with dimensions [depth][rows][cols]
	result := make([][][]float64, depth)
	for d := 0; d < depth; d++ {
		result[d] = make([][]float64, n)
		for r := 0; r < n; r++ {
			start := d*n*n + r*n
			end := start + n
			result[d][r] = grid[start:end] // Extract a sub-slice for each row
		}
	}

	return result
}

func consensus(comm [][][]int, ec []int, grid [][][]float64) (bool, int) {
	var i int
	var j int
	var found bool
	// var t_local_next [4]float64
	var final_time int
	// fmt.Println(ec[e])
	t_local := []float64{0, 0, 0, 0}
	t_local_next := []float64{0, 0, 0, 0}
	for c := 0; c < len(comm); c++ {
		// for t := 0; t < 4; t++ {
		// 	t_local_next[t] = t_local[t]
		// }
		copy(t_local_next, t_local)
		for c2 := 0; c2 < len(comm[c]); c2++ {
			found = false
			i = comm[c][c2][0]
			j = comm[c][c2][1]

			for t := 0; t < len(grid[:][ec[i]][ec[j]]); t++ {

				if grid[t][ec[i]][ec[j]] >= t_local[i] {
					// fmt.Println("Test")
					found = true
					if grid[t][ec[i]][ec[j]] > t_local_next[j] {
						t_local_next[j] = grid[t][ec[i]][ec[j]]
						break
					}
				} else {
					break
				}
			}
			if !found {
				// fmt.Println(t_local_next)
				return false, -1
			}
		}
		// fmt.Println(t_local_next)
		// for t := 0; t < 4; t++ {
		// 	t_local[t] = t_local_next[t]
		// }
		copy(t_local, t_local_next)
	}
	final_time = 0
	for t := 0; t < 4; t++ {
		if final_time > int(t_local[t]) {
			final_time = int(t_local[t])
		}
	}
	fmt.Println("test")
	return true, final_time
}

//export consensus_completeness_per
func consensus_completeness_per(combs_raw *float64, combs_n int64, grid_raw *float64, grid_n int64, num_sats int64) C.int {
	// fmt.Println("Started")
	// fmt.Println(documentPtr)
	combs_flat := unsafe.Slice(combs_raw, combs_n)

	grid_flat := unsafe.Slice(grid_raw, grid_n)
	// fmt.Println(grid_flat)

	combs := convert_to_n_by_rest(combs_flat, 3)
	var ec [][]int
	for i := 0; i < len(combs); i++ {
		var temp = []int{0}
		for j := 0; j < len(combs[i]); j++ {
			temp = append(temp, int(combs[i][j]))
		}
		if len(temp) == 4 {
			ec = append(ec, temp)
		}
	}
	// fmt.Println(ec)

	grid := convert_to_n_by_n_by_rest(grid_flat, int(num_sats))
	// fmt.Println(grid)

	// for i := 0; i < 10; i++ {
	// 	fmt.Println(grid[i][0])
	// }

	// var comm [][][]float64
	comm := [][][]int{
		{{0, 1}, {0, 2}, {0, 3}},
		{{1, 0}, {1, 2}, {1, 3}, {2, 0}, {2, 1}, {2, 3}, {3, 0}, {3, 1}, {3, 2}},
		{{0, 1}, {0, 2}, {0, 3}, {1, 0}, {1, 2}, {1, 3}, {2, 0}, {2, 1}, {2, 3}, {3, 0}, {3, 1}, {3, 2}},
		{{1, 0}, {2, 0}, {3, 0}},
		// [][]float64{[]float64{0, 1}, []float64{0, 2}, []float64{0, 3}},
	}

	// fmt.Println(comm)
	// var small_grid [4][4][]float64
	c := 0
	var completed bool
	for e := 0; e < len(ec); e++ {
		completed, _ = consensus(comm, ec[e], grid)
		if completed {
			c += 1
		}
	}

	// t_local = np.zeros(np.shape(small_grid)[0])

	// # Iterate through communication rounds and process satellite pairs for each round
	// for c, conn_round in enumerate(comm):
	//     t_local_next = t_local.copy()
	//     for i,j in conn_round:
	//         x = small_grid[i,j][small_grid[i,j] >= t_local[i]]
	//         if len(x) > 0:
	//             y = np.amin(x)
	//             if y > t_local_next[j]:
	//                 t_local_next[j] = y
	//         else:
	//             return False, -1
	//     # Update time arrary as round has ended
	//     t_local = t_local_next.copy()

	// return True, np.amax(t_local)

	// 	[[0,1],[0,2],[0,3]],
	// 	[[1,0],[1,2],[1,3], [2,0],[2,1],[2,3], [3,0],[3,1],[3,2]],
	// 	[[0,1],[0,2],[0,3], [1,0],[1,2],[1,3], [2,0],[2,1],[2,3], [3,0],[3,1],[3,2]],
	// 	[[1,0],[2,0],[3,0]]

	return C.int(c)
}
