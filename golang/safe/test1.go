package main

import "fmt"

func write(d map[string]int) {
    d["fruit"] = 2
}

func read(d map[string]int) {
    fmt.Println(d["fruit"])
}

func main() {
    d := map[string]int{}
    go read(d)
    write(d)
}

//  go run -race test1.go 
