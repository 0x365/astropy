# astropy

This image displays the shape of all keplerian orbital elements for all current satellites.

<img src="https://github.com/0x365/astropy/blob/main/perm_data/animation.gif" width="600" height="408"></img>





### Consensus Algorithm

```go
func consensus(comm [][][]int, ec []int, grid [][][]float64, num_participants int) (bool, int) {
	var i int
	var j int
	var c int
	var c2 int
	var t int
	var found bool
	var final_time int
	var t_local []float64
	var t_local_next []float64
	for i = 0; i < num_participants; i++ {
		t_local = append(t_local, 0.0)
		t_local_next = append(t_local_next, 0.0)
	}
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
	for t = 0; t < num_participants; t++ {
		if final_time < int(t_local[t]) {
			final_time = int(t_local[t])
		}
	}
	return true, final_time
}
```