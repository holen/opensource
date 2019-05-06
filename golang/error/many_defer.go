package main

import "fmt"
import "os"

func main() {
    fsrc, err := os.Open("source.txt")
    if err != nil {
        fmt.Println("open source file failed")
        return
    }
    defer fsrc.Close()
    fdes, err := os.Open("target.txt")
    if err != nil {
        fmt.Println("open target file failed")
        return
    }
    defer fdes.Close()
    fmt.Println("do something here")
}
