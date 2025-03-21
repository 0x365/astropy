// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

// Consensus Segments

// This file contains:
// A. Initial data gatherer
// B. Consensus Segments
// C. Find next connection function

// STEPS:
// 0. Get initial data
// 1. Pre-Prepare
// 2. Prepare
// 3. Commit
// 4. Reply

// #########################

package main

// PRE-PREPARE
func consensus_pre_prepare(t_local []int, sat_data_big [][][]bool, num_sats int, primary int, completeness int) (bool, int, []int, int) {
	var conn_time int
	var max_time int
	var j int
	for j = 0; j < num_sats; j++ {
		if primary != j {
			conn_time = find_next_conn(t_local[primary], sat_data_big[primary][j])
			if conn_time == -1 {
				return false, 0, nil, completeness
			}
			t_local[j] = conn_time
			completeness += 1
			if max_time < conn_time {
				max_time = conn_time
			}
		}
	}
	return true, max_time, t_local, completeness
}

// PREPARE
func consensus_prepare(t_local []int, sat_data_big [][][]bool, num_sats int, primary int, completeness int) (bool, int, []int, int) {
	var conn_time int
	var max_time int
	var i, j int
	for j = 0; j < num_sats; j++ {
		max_time = 0
		for i = 0; i < num_sats; i++ {
			if i != j && i != primary {
				conn_time = find_next_conn(t_local[i], sat_data_big[j][i])
				if conn_time == -1 {
					return false, 0, nil, completeness
				}
				completeness += 1
				if max_time < conn_time {
					max_time = conn_time
				}
			}
		}
		t_local[j] = max_time
	}
	max_time = get_max(t_local)
	return true, max_time, t_local, completeness
}

// COMMIT
func consensus_commit(t_local []int, sat_data_big [][][]bool, num_sats int, completeness int) (bool, int, []int, int) {
	var conn_time int
	var max_time int
	var i, j int
	for j = 0; j < num_sats; j++ {
		max_time = 0
		for i = 0; i < num_sats; i++ {
			if i != j {
				conn_time = find_next_conn(t_local[i], sat_data_big[j][i])
				if conn_time == -1 {
					return false, 0, nil, completeness
				}
				completeness += 1
				if max_time < conn_time {
					max_time = conn_time
				}
			}
		}
		t_local[j] = max_time
	}
	max_time = get_max(t_local)
	return true, max_time, t_local, completeness
}

// REPLY
func consensus_reply(t_local []int, sat_data_big [][][]bool, num_sats int, primary int, completeness int) (bool, int, int) {
	var conn_time int
	var max_time int
	var i int
	for i = 0; i < num_sats; i++ {
		if i != primary {
			conn_time = find_next_conn(t_local[i], sat_data_big[i][primary])
			if conn_time == -1 {
				return false, 0, completeness
			}
			completeness += 1
			if max_time < conn_time {
				max_time = conn_time
			}
		}
	}
	return true, max_time, completeness
}

// Find next valid connection in sat_data
func find_next_conn(t_0 int, sat_data []bool) int {
	var t int
	for t = t_0; t < len(sat_data); t++ {
		if sat_data[t] {
			return t
		}
	}
	return -1
}

func get_max(input_array []int) (max_val int) {
	max_val = 0
	var i int
	for i = 0; i < len(input_array); i++ {
		if max_val < input_array[i] {
			max_val = input_array[i]
		}
	}
	return max_val
}
