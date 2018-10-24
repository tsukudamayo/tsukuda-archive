package main

import (
	"fmt"
	"log"
	"os"
	// "math/rand"
	"flag"
	"strconv"
	"strings"
	"time"
)

type ProgressBar struct {
	max      int
	progress int
	percent  float64
}

func genereateProgressBar(progress int, max int, percent float64, roundpercent int) {
	// time
	fmt.Printf(" %d / %d", progress, max)

	if progress > max {
		progress -= (progress - max)
		fmt.Printf("progress %d", progress)
	}

	// percent and progress bar
	fmt.Print(fmt.Sprintf(" %5.1f%% [%s>%s] %d \r",
		percent,
		strings.Repeat("=", roundpercent/2),      // diveided by 2 to fit console
		strings.Repeat(" ", (99-roundpercent)/2), // divided by 2 to fit console
		progress,
	))

	return

}

func genereateLogging(timestrings string, task string, finishtime int) {
	filename := timestrings + "_log.csv"

	file, err := os.OpenFile(
		filename, os.O_CREATE|os.O_RDWR|os.O_APPEND, 0666,
	)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	fmt.Fprintf(file, "%s,%d\n", task, finishtime)

	return
}

func main() {
	// to parse commandline argument
	flag.Parse()
	fmt.Println(flag.Arg(0))

	finishtime, _ := strconv.Atoi(flag.Arg(0))
	progressBar := ProgressBar{
		max:      finishtime,
		progress: 0,
	}

	for {
		progressBar.progress += 1

		// percent
		progressBar.percent =
			(float64(progressBar.progress) / float64(progressBar.max)) * 100
		roundPercent := int(progressBar.percent)

		if roundPercent > 0 {
			roundPercent -= 1
		}

		// --------------------
		// console output
		// --------------------
		genereateProgressBar(
			progressBar.progress,
			progressBar.max,
			progressBar.percent,
			roundPercent,
		)

		// finish
		if progressBar.progress == progressBar.max {
			fmt.Println("")
			break
		}

		time.Sleep(1 * time.Second)
	}
	// --------------------
	// log output
	// --------------------
	// time
	const layout = "2006-01-02"
	timestrings := time.Now().Format(layout)
	// timestrings := t.String()
	task := flag.Arg(1)
	genereateLogging(timestrings, task, finishtime)
}
