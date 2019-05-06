package main

import "fmt"
import "time"
import "runtime"

/*
一个进程内部可以运行多个线程，而每个线程又可以运行很多协程。
线程要负责对协程进行调度，保证每个协程都有机会得到执行。
当一个协程睡眠时，它要将线程的运行权让给其它的协程来运行，而不能持续霸占这个线程。
同一个线程内部最多只会有一个协程正在运行。

线程的调度是由操作系统负责的，调度算法运行在内核态，而协程的调用是由 Go 语言的运行时负责的，调度算法运行在用户态。
*/

// 设置线程数
func main() {
    // 读取默认的线程数
    fmt.Println(runtime.GOMAXPROCS(0)) // 4
    // 设置线程数为 10
    runtime.GOMAXPROCS(10)
    // 读取当前的线程数
    fmt.Println(runtime.GOMAXPROCS(0)) // 10

    // 
    fmt.Println(runtime.NumGoroutine()) // 1
    for i:=0;i<10;i++ {
        go func(){
            for {
                time.Sleep(time.Second)
            }
        }()
    }
    fmt.Println(runtime.NumGoroutine()) // 11

    // 协程死循环
    fmt.Println("run in main goroutine")
    n := 3
    for i:=0; i<n; i++ {
        go func() {
            fmt.Println("dead loop goroutine start")
            for {}  // 死循环
        }()
    }
    for {
        time.Sleep(time.Second)
        fmt.Println("main goroutine running")
    }


    // 启动百万协程
    fmt.Println("run in main goroutine")
    i := 1
    for {
        go func() {
            for {
                time.Sleep(time.Second)
            }
        }()
        if i % 10000 == 0 {
            fmt.Printf("%d goroutine started\n", i)
        }
        i++
    }
}

