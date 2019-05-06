package main

import "fmt"
import "os"

// 需要注意的是 defer 语句的执行顺序和代码编写的顺序是反过来的，也就是说最先 defer 的语句最后执行
func main() {
    fsrc, err := os.Open("source.txt")
    if err != nil {
        fmt.Println("open source file failed")
        return
    }
    defer func() {
        fmt.Println("close source file")
        fsrc.Close()
    }()

    fdes, err := os.Open("target.txt")
    if err != nil {
        fmt.Println("open target file failed")
        return
    }
    defer func() {
        fmt.Println("close target file")
        fdes.Close()
    }()
    fmt.Println("do something here")
    // do something here
    // close target file
    // close source file
}
