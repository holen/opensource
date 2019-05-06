package main

import "fmt"
import "time"

func main() {
    fmt.Println("run in main goroutine") 
    // 协程的启动, go 关键词加上一个函数调用就可以了
    go func() { // 主协程
        fmt.Println("run in child goroutine")
        go func() {
            fmt.Println("run in grand child goroutine")
            go func() {
                fmt.Println("run in grand grand child goroutine")
            }()
        }()
    }()
    // 主协程运行结束，其它协程就会立即消亡，不管它们是否已经开始运行
    time.Sleep(time.Second)
    fmt.Println("main goroutine will quit")
}
