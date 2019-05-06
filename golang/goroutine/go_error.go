package main

import "fmt"
import "time"

var negErr = fmt.Errorf("wtf")

// 子协程异常退出
func main() {
    fmt.Println("run in main goroutine")
    go func() {
        fmt.Println("run in child goroutine")
        go func() {
            fmt.Println("run in grand child goroutine")
            go func() {
                fmt.Println("run in grand grand child goroutine")
		// 子协程的异常退出会将异常传播到主协程，直接会导致主协程也跟着挂掉，然后整个程序就崩溃了
                panic(negErr)
            }()
        }()
    }()
    time.Sleep(time.Second)
    fmt.Println("main goroutine will quit")
}
