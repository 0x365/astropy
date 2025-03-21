package main

import (
	"fmt"
	"math"
	"os"

	// "time"
	// "math/rand"
	"encoding/csv"
	"strconv"

	// "encoding/json"
	// "io/ioutil"
	"github.com/schollz/progressbar/v3"
)

// type OutStuff struct {
//	NumOrbits int
//	ProcessTime float64
//}

func get_acceleration(y []float64) (out []float64) {

	out = []float64{}

	m1, m2, m3 := 1.0, 1.0, 1.0
	G := 1.0

	r1x, r1y := y[0], y[1]
	r2x, r2y := y[2], y[3]
	r3x, r3y := y[4], y[5]

	// r12 := math.Sqrt(math.Pow(r1x-r2x, 2) + math.Pow(r1y-r2y, 2))

	r12 := math.Pow(math.Sqrt(math.Pow(r1x-r2x, 2)+math.Pow(r1y-r2y, 2)), 3)
	r13 := math.Pow(math.Sqrt(math.Pow(r1x-r3x, 2)+math.Pow(r1y-r3y, 2)), 3)
	r23 := math.Pow(math.Sqrt(math.Pow(r2x-r3x, 2)+math.Pow(r2y-r3y, 2)), 3)

	if r12 == 0 {
		r12 = 1.0
	}
	if r13 == 0 {
		r13 = 1.0
	}
	if r23 == 0 {
		r23 = 1.0
	}

	f1x := -G*m2*(r1x-r2x)/r12 + -G*m3*(r1x-r3x)/r13
	f1y := -G*m2*(r1y-r2y)/r12 + -G*m3*(r1y-r3y)/r13
	f2x := -G*m1*(r2x-r1x)/r12 + -G*m3*(r2x-r3x)/r23
	f2y := -G*m1*(r2y-r1y)/r12 + -G*m3*(r2y-r3y)/r23
	f3x := -G*m1*(r3x-r1x)/r13 + -G*m2*(r3x-r2x)/r23
	f3y := -G*m1*(r3y-r1y)/r13 + -G*m2*(r3y-r2y)/r23

	out = append(out, f1x)
	out = append(out, f1y)
	out = append(out, f2x)
	out = append(out, f2y)
	out = append(out, f3x)
	out = append(out, f3y)

	return out
}

func arr_m(y []float64, multiplier float64) (z []float64) {
	var i int
	for i = 0; i < len(y); i++ {
		z = append(z, y[i]*multiplier)
	}
	return z
}

func arr_a(x []float64, y []float64) (z []float64) {
	var i int
	for i = 0; i < len(x); i++ {
		z = append(z, x[i]+y[i])
	}
	return z
}

func save_to_csv(data_2d [][]string, number string) {
	// Save data to csv
	file, _ := os.Create("data/out_file_name" + number + ".csv")
	defer file.Close()
	// check(err)
	w := csv.NewWriter(file)
	defer w.Flush()
	// for i:=0;i<len(data_1d);i++{
	// }
	// w.Write(data_1d)	// Can iterate over this one
	w.WriteAll(data_2d)
}

func main() {
	// Change go.mod file location
	fmt.Println("Hi")
	// fmt.Println(step())

	total_num := 100
	no_circle := true

	bar := progressbar.Default(2 * int64(total_num))

	// v_1 := 0.3471128135672417
	// v_2 := 0.532726851767674

	var v_1 float64
	var v_2 float64

	// var k1 []float64
	// var k2 []float64
	// var k3 []float64
	// var k4 []float64

	var x0 []float64
	var v0 []float64
	var x []float64
	var v []float64

	var rel float64
	var relative_distance []string
	var all_rel [][]string
	// var y_string []string
	// var all_values [][]string

	dt := 0.001

	var v1 int
	var v2 int
	var i int

	var target bool
	var start bool

	c1 := 0.6756
	c2 := -0.1756
	c3 := -0.1756
	c4 := 0.6756

	d1 := 1.3512
	d2 := -1.7024
	d3 := 1.3512

	var r12 float64
	var r13 float64
	var r23 float64

	var pe1 float64
	var ke1 float64
	var pe2 float64
	var ke2 float64
	var pe3 float64
	var ke3 float64
	var se float64

	var energy_string []string
	var all_energy_string [][]string
	// var j int;

	sqrt3 := math.Sqrt(3.0)

	for v1 = -total_num; v1 < total_num; v1++ {
		all_rel = [][]string{}
		all_energy_string = [][]string{}
		for v2 = -total_num; v2 < total_num; v2++ {

			// all_values = [][]string{}

			v_1 = 1.5 * float64(v1) / float64(total_num)
			v_2 = 1.5 * float64(v2) / float64(total_num)

			relative_distance = []string{}

			if math.Sqrt(math.Pow(v_1, 2)+math.Pow(v_2, 2)) <= 1.5 || no_circle {

				energy_string = []string{}

				// Line configuration
				// x0 = []float64{-1.0, 0.0, 1.0, 0.0, 0.0, 0.0}
				// v0 = []float64{v_1, v_2, v_1, v_2, -2.0 * v_1 / 1.0, -2.0 * v_2 / 1.0}

				// Triangle configuration
				x0 = []float64{-sqrt3 / 2.0, -0.5, sqrt3 / 2.0, -0.5, 0.0, 1.0}
				v0 = []float64{v_1 * 1.0 / 2.0, v_2 * (-sqrt3) / 2.0, v_1 / 2.0, v_2 * sqrt3 / 2.0, v_1 * (-1.0), 0.0}

				// N-bodies configuration
				// x = r*cos(pi/2 + 2*pi*i/n)
				// y = r*sin(pi/2 + 2*pi*i/n)
				// Where r is radius of orbit, i is body number, and n is number of bodies

				x = x0
				v = v0

				target = false
				start = false
				for i = 0; i < 50000; i++ {

					// y_string = []string{}

					// for j=0;j<len(y);j++ {
					// 	y_string = append(y_string, strconv.FormatFloat(y[j], 'f', -1, 64))
					// }
					// all_values = append(all_values, y_string)
					r12 = math.Sqrt(math.Pow(x[0]-x[2], 2) + math.Pow(x[1]-x[3], 2))
					r13 = math.Sqrt(math.Pow(x[0]-x[4], 2) + math.Pow(x[1]-x[5], 2))
					r23 = math.Sqrt(math.Pow(x[2]-x[4], 2) + math.Pow(x[3]-x[5], 2))

					pe1, pe2, pe3 = -2/r12-2/r13, -2/r12-2/r23, -2/r13-2/r23
					ke1 = 0.5 * (math.Pow(v[0], 2) + math.Pow(v[1], 2))
					ke2 = 0.5 * (math.Pow(v[2], 2) + math.Pow(v[3], 2))
					ke3 = 0.5 * (math.Pow(v[4], 2) + math.Pow(v[5], 2))

					se = (pe1 + ke1 + pe2 + ke2 + pe3 + ke3)

					energy_string = append(energy_string, strconv.FormatFloat(se, 'f', -1, 64))

					// energy_string0 = append(energy_string, strconv.FormatFloat(se0, 'f', -1, 64))
					// energy_string1 = append(energy_string, strconv.FormatFloat(se1, 'f', -1, 64))
					// energy_string2 = append(energy_string, strconv.FormatFloat(se2, 'f', -1, 64))

					x = arr_a(x, arr_m(v, c1*dt))

					v = arr_a(v, arr_m(get_acceleration(x), dt*d1))

					x = arr_a(x, arr_m(v, c2*dt))

					v = arr_a(v, arr_m(get_acceleration(x), dt*d2))

					x = arr_a(x, arr_m(v, c3*dt))

					v = arr_a(v, arr_m(get_acceleration(x), dt*d3))

					x = arr_a(x, arr_m(v, c4*dt))

					rel = math.Sqrt(math.Pow(x[0]-x0[0], 2)+math.Pow(x[1]-x0[1], 2)) + math.Sqrt(math.Pow(x[2]-x0[2], 2)+math.Pow(x[3]-x0[3], 2)) + math.Sqrt(math.Pow(x[4]-x0[4], 2)+math.Pow(x[5]-x0[5], 2))

					relative_distance = append(relative_distance, strconv.FormatFloat(1.0/rel, 'f', -1, 64))

					if rel > 100 {
						break
					}
					if rel > 0.1 {
						start = true
					}
					if rel < 10 && start {
						target = true
					}

					// NOW CALCULATE PERIOD

					// }

				}
				if target {
					all_rel = append(all_rel, relative_distance)
					all_energy_string = append(all_energy_string, energy_string)
				} else {
					all_rel = append(all_rel, []string{"0.0"})
					all_energy_string = append(all_energy_string, []string{"0.0"})
				}
			} else {
				all_rel = append(all_rel, []string{"0.0"})
				all_energy_string = append(all_energy_string, []string{"0.0"})
			}

		}
		bar.Add(1)
		save_to_csv(all_rel, strconv.FormatFloat(float64(v1), 'f', -1, 64))
		save_to_csv(all_energy_string, strconv.FormatFloat(float64(v1)+0.5, 'f', -1, 64))
	}

}
