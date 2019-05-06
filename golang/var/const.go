package main

import "fmt"

const globali int = 24

func main() {
    const locali int = 40
    fmt.Println(globali, locali)
    // 24 40
}
