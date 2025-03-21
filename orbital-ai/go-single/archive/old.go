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

func step2(dt float64, y []float64) (out []float64) {

	m1, m2, m3 := 1.0, 1.0, 1.0
	G := 1.0

	// out = append(out, y[6:]...)
	out = append(out, dt*y[6])
	out = append(out, dt*y[7])
	out = append(out, dt*y[8])
	out = append(out, dt*y[9])
	out = append(out, dt*y[10])
	out = append(out, dt*y[11])

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

	out = append(out, dt*f1x)
	out = append(out, dt*f1y)
	out = append(out, dt*f2x)
	out = append(out, dt*f2y)
	out = append(out, dt*f3x)
	out = append(out, dt*f3y)

	return out
}

func arr_m2(y []float64, multiplier float64) (z []float64) {
	var i int
	for i = 0; i < len(y); i++ {
		z = append(z, y[i]*multiplier)
	}
	return z
}

func arr_a2(x []float64, y []float64) (z []float64) {
	var i int
	for i = 0; i < len(x); i++ {
		z = append(z, x[i]+y[i])
	}
	return z
}

func save_to_csv2(data_2d [][]string, number string) {
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

func calc_for_inputs2(v_1 float64, v_2 float64, dt float64, id int) {

	var k1 []float64
	var k2 []float64
	var k3 []float64
	var k4 []float64

	var y0 []float64
	var y []float64

	var y_string []string
	var all_values [][]string

	var i int
	var j int

	y0 = []float64{-1.0, 0.0, 1.0, 0.0, 0.0, 0.0, v_1, v_2, v_1, v_2, -2.0 * v_1 / 1.0, -2.0 * v_2 / 1.0}

	y = y0

	for i = 0; i < 1000000; i++ {

		y_string = []string{}

		for j = 0; j < len(y); j++ {
			y_string = append(y_string, strconv.FormatFloat(y[j], 'f', -1, 64))
		}
		all_values = append(all_values, y_string)

		k1 = step(dt, y)
		k2 = step(dt, arr_a(y, arr_m(k1, 0.5)))
		k3 = step(dt, arr_a(y, arr_m(k2, 0.5)))
		k4 = step(dt, arr_a(y, k3))

		y = arr_a(y, arr_m(arr_a(arr_a(k1, arr_m(k2, 2)), arr_a(arr_m(k3, 2), k4)), 1.0/6.0))
	}

	save_to_csv(all_values, strconv.FormatFloat(float64(id), 'f', -1, 64))
}

func main2() {
	fmt.Println("Hi")

	dt := 0.00001

	v_1 := 0.3471128135672417
	v_2 := 0.532726851767674

	calc_for_inputs(v_1, v_2, dt, 0)

	v_1 = 0.105527638
	v_2 = 0.708542714

	calc_for_inputs(v_1, v_2, dt, 1)

	v_1 = 0.3
	v_2 = 0.5

	calc_for_inputs(v_1, v_2, dt, 2)

}
