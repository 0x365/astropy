package main

import (
	"bufio"
	"bytes"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/joshuaferrara/go-satellite"
)

func generateSimSats(INC float64, RAAN float64, ECC float64, ARGP float64, ANOM float64, MOTION float64) (all_coords []Coord) {
	_, err := os.Stat("./TLE.txt")
	if errors.Is(err, os.ErrNotExist) {
		fmt.Println("Downloading current TLE data")
		out, _ := os.Create("TLE.txt")
		defer out.Close()
		resp, err := http.Get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")
		check(err)
		defer resp.Body.Close()
		io.Copy(out, resp.Body)
	}
	// } else {
	// fmt.Println("TLE data already exists")
	// }

	file, err := os.Open("TLE.txt")
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)

	var temp []string
	c0 := 0
	var example_TLE TLE
	for scanner.Scan() {
		temp = append(temp, string(scanner.Text()))
		if c0 == 2 {
			example_TLE = TLE{temp[0], temp[1], temp[2]}
			break
		}
		c0 += 1
	}

	os.Mkdir("data", 0755)
	os.Mkdir("data/pos_sim", 0755)

	inc := fmt.Sprintf("%08.4f", float64(INC))
	raan := fmt.Sprintf("%08.4f", float64(RAAN))
	ecc := fmt.Sprintf("%07.0f", float64(ECC))
	argp := fmt.Sprintf("%08.4f", float64(ARGP))
	anom := fmt.Sprintf("%08.4f", float64(ANOM))
	motion := fmt.Sprintf("%10.8f", float64(MOTION))

	var sb bytes.Buffer
	sb.WriteString(string(example_TLE.l2[0:7]))
	sb.WriteString(" ")
	sb.WriteString(string(inc))
	sb.WriteString(" ")
	sb.WriteString(string(raan))
	sb.WriteString(" ")
	sb.WriteString(string(ecc))
	sb.WriteString(" ")
	sb.WriteString(string(argp))
	sb.WriteString(" ")
	sb.WriteString(string(anom))
	sb.WriteString(" ")
	sb.WriteString(string(motion))
	sb.WriteString(string(example_TLE.l2[63:68]))

	bytes_string := sb.Bytes()

	// Checksum
	var sum int
	var stringer string
	var numb int
	for i := 0; i < len(bytes_string); i++ {
		stringer = string(bytes_string[i])
		if stringer != " " && stringer != "." {
			numb, _ = strconv.Atoi(stringer)
			sum += numb
		}
	}
	sb.WriteString(strconv.Itoa(sum % 10))

	s := satellite.TLEToSat(
		example_TLE.l1,
		sb.String(),
		"wgs84",
	)

	start_t := time.Unix(START_TIME, 0)
	t := start_t
	t = start_t
	var all_pos [][]string
	for i := 0; i < ITERATIONS; i++ {
		pos, _ := satellite.Propagate(s, t.Year(), int(t.Month()), t.Day(), t.Hour(), t.Minute(), t.Second())
		t = t.Add(time.Second * 30)
		temp = nil
		temp = append(temp, fmt.Sprintf("%f", pos.X))
		temp = append(temp, fmt.Sprintf("%f", pos.Y))
		temp = append(temp, fmt.Sprintf("%f", pos.Z))

		all_pos = append(all_pos, temp)

		all_coords = append(all_coords, Coord{pos.X, pos.Y, pos.Z})
	}

	writeFile2D(all_pos, "./data/pos_sim/temp.csv")

	return all_coords
}
