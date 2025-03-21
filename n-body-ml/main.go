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

func get_acceleration4(y []float64) (out []float64) {

	out = []float64{}

	m1, m2, m3, m4 := 1.0, 1.0, 1.0, 1.0
	G := 1.0

	r1x, r1y := y[0], y[1]
	r2x, r2y := y[2], y[3]
	r3x, r3y := y[4], y[5]
	r4x, r4y := y[6], y[7]

	// r12 := math.Sqrt(math.Pow(r1x-r2x, 2) + math.Pow(r1y-r2y, 2))

	r12 := math.Pow(math.Sqrt(math.Pow(r1x-r2x, 2)+math.Pow(r1y-r2y, 2)), 3)
	r13 := math.Pow(math.Sqrt(math.Pow(r1x-r3x, 2)+math.Pow(r1y-r3y, 2)), 3)
	r14 := math.Pow(math.Sqrt(math.Pow(r1x-r4x, 2)+math.Pow(r1y-r4y, 2)), 3)
	r23 := math.Pow(math.Sqrt(math.Pow(r2x-r3x, 2)+math.Pow(r2y-r3y, 2)), 3)
	r24 := math.Pow(math.Sqrt(math.Pow(r2x-r4x, 2)+math.Pow(r2y-r4y, 2)), 3)
	r34 := math.Pow(math.Sqrt(math.Pow(r3x-r4x, 2)+math.Pow(r3y-r4y, 2)), 3)

	if r12 == 0 {
		r12 = 1.0
	}
	if r13 == 0 {
		r13 = 1.0
	}
	if r14 == 0 {
		r14 = 1.0
	}
	if r23 == 0 {
		r23 = 1.0
	}
	if r24 == 0 {
		r24 = 1.0
	}
	if r34 == 0 {
		r34 = 1.0
	}

	f1x := -G*m2*(r1x-r2x)/r12 + -G*m3*(r1x-r3x)/r13 + -G*m4*(r1x-r4x)/r14
	f1y := -G*m2*(r1y-r2y)/r12 + -G*m3*(r1y-r3y)/r13 + -G*m4*(r1y-r4y)/r14
	f2x := -G*m1*(r2x-r1x)/r12 + -G*m3*(r2x-r3x)/r23 + -G*m4*(r2x-r4x)/r24
	f2y := -G*m1*(r2y-r1y)/r12 + -G*m3*(r2y-r3y)/r23 + -G*m4*(r2y-r4y)/r24
	f3x := -G*m1*(r3x-r1x)/r13 + -G*m2*(r3x-r2x)/r23 + -G*m4*(r3x-r4x)/r34
	f3y := -G*m1*(r3y-r1y)/r13 + -G*m2*(r3y-r2y)/r23 + -G*m4*(r3y-r4y)/r34
	f4x := -G*m1*(r4x-r1x)/r14 + -G*m2*(r4x-r2x)/r24 + -G*m3*(r3x-r4x)/r34
	f4y := -G*m1*(r4y-r1y)/r14 + -G*m2*(r4y-r2y)/r24 + -G*m3*(r3y-r4y)/r34

	out = append(out, f1x)
	out = append(out, f1y)
	out = append(out, f2x)
	out = append(out, f2y)
	out = append(out, f3x)
	out = append(out, f3y)
	out = append(out, f4x)
	out = append(out, f4y)

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

func save_to_csv(data_2d [][]string, v1 float64, v2 float64) {
	number1 := strconv.FormatFloat(float64(v1), 'f', -1, 64)
	number2 := strconv.FormatFloat(float64(v2), 'f', -1, 64)
	// Save data to csv
	file, _ := os.Create("data/" + number1 + "_" + number2 + ".csv")
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

	total_num := 200

	bar := progressbar.Default(2 * int64(total_num) * 2 * int64(total_num))

	var v_1 float64
	var v_2 float64

	var x0 []float64
	var v0 []float64
	var x []float64
	var v []float64

	dt := 0.001

	var v1 int
	var v2 int
	var i int
	var j int

	var y_string []string
	var all_values [][]string

	c1 := 0.6756
	c2 := -0.1756
	c3 := -0.1756
	c4 := 0.6756

	d1 := 1.3512
	d2 := -1.7024
	d3 := 1.3512

	// sqrt3 := math.Sqrt(3.0)

	for v1 = -total_num; v1 <= total_num; v1++ {
		for v2 = -total_num; v2 <= total_num; v2++ {

			all_values = [][]string{}

			v_1 = 2.0 * float64(v1) / float64(total_num)
			v_2 = 2.0 * float64(v2) / float64(total_num)

			// Line configuration - remember get_accerelation function
			// x0 = []float64{-1.0, 0.0, 1.0, 0.0, 0.0, 0.0}
			// v0 = []float64{v_1, v_2, v_1, v_2, -2.0 * v_1 / 1.0, -2.0 * v_2 / 1.0}

			// Triangle configuration - remember get_accerelation function
			// x0 = []float64{-sqrt3 / 2.0, -0.5, sqrt3 / 2.0, -0.5, 0.0, 1.0}
			// v0 = []float64{v_1 * 1.0 / 2.0, v_2 * (-sqrt3) / 2.0, v_1 / 2.0, v_2 * sqrt3 / 2.0, v_1 * (-1.0), 0.0}

			// Square
			x0 = []float64{-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5}
			v0 = []float64{-v_1, -v_2, -v_1, v_2, v_1, v_2, v_1, -v_2}

			// N-bodies configuration
			// x = r*cos(pi/2 + 2*pi*i/n)
			// y = r*sin(pi/2 + 2*pi*i/n)
			// Where r is radius of orbit, i is body number, and n is number of bodies

			x = x0
			v = v0

			y_string = []string{}

			for j = 0; j < len(x); j++ {
				y_string = append(y_string, strconv.FormatFloat(x[j], 'f', -1, 64))
			}

			all_values = append(all_values, y_string)

			for i = 1; i < 3000; i++ {

				x = arr_a(x, arr_m(v, c1*dt))
				v = arr_a(v, arr_m(get_acceleration4(x), dt*d1))
				x = arr_a(x, arr_m(v, c2*dt))
				v = arr_a(v, arr_m(get_acceleration4(x), dt*d2))
				x = arr_a(x, arr_m(v, c3*dt))
				v = arr_a(v, arr_m(get_acceleration4(x), dt*d3))
				x = arr_a(x, arr_m(v, c4*dt))

				y_string = []string{}
				for j = 0; j < len(x); j++ {
					y_string = append(y_string, strconv.FormatFloat(x[j], 'f', -1, 64))
				}

				all_values = append(all_values, y_string)
			}
			save_to_csv(all_values, v_1, v_2)
			bar.Add(1)
		}
	}
}
