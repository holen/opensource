package main

import "fmt"

func main() {
    fmt.Println(sign(max(min(24, 42), max(24, 42))))
}

func max(a int, b int) int {
    if a > b {
        return a
    }
    return b
}

func min(a int, b int) int {
    if a < b {
        return a
    }
    return b
}

func sign(a int) int {
    if a > 0 {
        return 1
    } else if a < 0 {
        return -1
    } else {
        return 0
    }
}
