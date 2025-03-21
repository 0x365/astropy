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
)

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

func calc_for_inputs(v_1 float64, v_2 float64, dt float64, id int) {

	sqrt3 := math.Sqrt(3.0)

	var y_string []string
	var all_values [][]string

	var energy []float64
	var energy_string []string
	var all_energy_string [][]string

	var i int
	var j int

	// Line configuration
	// x0 := []float64{-1.0, 0.0, 1.0, 0.0, 0.0, 0.0}
	// v0 := []float64{v_1, v_2, v_1, v_2, -2.0 * v_1 / 1.0, -2.0 * v_2 / 1.0}

	// Triangle configuration
	x0 := []float64{-sqrt3 / 2.0, -0.5, sqrt3 / 2.0, -0.5, 0.0, 1.0}
	v0 := []float64{v_1 * 1.0 / 2.0, v_2 * (-sqrt3) / 2.0, v_1 / 2.0, v_2 * sqrt3 / 2.0, v_1 * (-1.0), 0.0}
	// v0 := []float64{v_1 * 1.0 / 2.0, v_2 * (-sqrt3) / 2.0, 0.0, 0.0, 0.0, 0.0}
	// N-bodies configuration
	// x = r*cos(pi/2 + 2*pi*i/n)
	// y = r*sin(pi/2 + 2*pi*i/n)
	// Where r is radius of orbit, i is body number, and n is number of bodies

	x := x0
	v := v0

	c1 := 0.6756
	c2 := -0.1756
	c3 := -0.1756
	c4 := 0.6756

	d1 := 1.3512
	d2 := -1.7024
	d3 := 1.3512

	for i = 0; i < 50000; i++ {

		y_string = []string{}

		for j = 0; j < len(x); j++ {
			y_string = append(y_string, strconv.FormatFloat(x[j], 'f', -1, 64))
		}
		all_values = append(all_values, y_string)

		energy = []float64{}
		energy_string = []string{}

		r1x, r1y := x[0], x[1]
		r2x, r2y := x[2], x[3]
		r3x, r3y := x[4], x[5]

		r12 := math.Pow(math.Sqrt(math.Pow(r1x-r2x, 2)+math.Pow(r1y-r2y, 2)), 3)
		r13 := math.Pow(math.Sqrt(math.Pow(r1x-r3x, 2)+math.Pow(r1y-r3y, 2)), 3)
		r23 := math.Pow(math.Sqrt(math.Pow(r2x-r3x, 2)+math.Pow(r2y-r3y, 2)), 3)

		energy = append(energy, 2/r12+2/r13)
		energy = append(energy, 0.5*(math.Pow(v[0], 2)+math.Pow(v[1], 2)))
		energy = append(energy, 2/r12+2/r23)
		energy = append(energy, 0.5*(math.Pow(v[2], 2)+math.Pow(v[3], 2)))
		energy = append(energy, 2/r13+2/r23)
		energy = append(energy, 0.5*(math.Pow(v[4], 2)+math.Pow(v[5], 2)))

		// energy = append(energy, math.Sqrt(math.Pow(x[0]-(x[0]+x[2]+x[4])/3, 2)+math.Pow(x[1]-(x[1]+x[3]+x[5])/3, 2)))
		// energy = append(energy, 0.5*(math.Pow(v[0], 2)+math.Pow(v[1], 2)))
		// energy = append(energy, math.Sqrt(math.Pow(x[2]-(x[0]+x[2]+x[4])/3, 2)+math.Pow(x[3]-(x[1]+x[3]+x[5])/3, 2)))
		// energy = append(energy, 0.5*(math.Pow(v[2], 2)+math.Pow(v[3], 2)))
		// energy = append(energy, math.Sqrt(math.Pow(x[4]-(x[0]+x[2]+x[4])/3, 2)+math.Pow(x[5]-(x[1]+x[3]+x[5])/3, 2)))
		// energy = append(energy, 0.5*(math.Pow(v[4], 2)+math.Pow(v[5], 2)))

		for j = 0; j < len(energy); j++ {
			energy_string = append(energy_string, strconv.FormatFloat(energy[j], 'f', -1, 64))
		}
		all_energy_string = append(all_energy_string, energy_string)

		// 4th order sympletic solver

		x = arr_a(x, arr_m(v, c1*dt))

		v = arr_a(v, arr_m(get_acceleration(x), dt*d1))

		x = arr_a(x, arr_m(v, c2*dt))

		v = arr_a(v, arr_m(get_acceleration(x), dt*d2))

		x = arr_a(x, arr_m(v, c3*dt))

		v = arr_a(v, arr_m(get_acceleration(x), dt*d3))

		x = arr_a(x, arr_m(v, c4*dt))

		// Center of mass is always at zero
		// fmt.Println("Center of mass pos", (x[0]+x[2]+x[4])/3, (x[1]+x[3]+x[5])/3)

		// 2nd order sympletic solver

		// v = arr_a(v, arr_m(get_acceleration(x), dt/2.0))

		// x = arr_a(x, arr_m(v, dt))

		// v = arr_a(v, arr_m(get_acceleration(x), dt/2.0))

	}

	save_to_csv(all_values, strconv.FormatFloat(float64(id), 'f', -1, 64))
	save_to_csv(all_energy_string, strconv.FormatFloat(float64(id)+0.5, 'f', -1, 64))
}

func main() {
	fmt.Println("Hi")

	dt := 0.001

	v_1 := 0.3471128135672417
	v_2 := 0.532726851767674

	calc_for_inputs(v_1, v_2, dt, 0)

	v_1 = -0.9545
	v_2 = 0.439393

	calc_for_inputs(v_1, v_2, dt, 1)

	v_1 = 0.34
	v_2 = 0.532726851767674

	calc_for_inputs(v_1, v_2, dt, 2)

}
