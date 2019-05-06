package main

import "fmt"
import "time"
import "math/rand"

/*
通道满了，写操作就会阻塞，协程就会进入休眠，直到有其它协程读通道挪出了空间，协程才会被唤醒。如果有多个协程的写操作都阻塞了，一个读操作只会唤醒一个协程。

通道空了，读操作就会阻塞，协程也会进入睡眠，直到有其它协程写通道装进了数据才会被唤醒。如果有多个协程的读操作阻塞了，一个写操作也只会唤醒一个协程。
*/
func send(ch chan int) {
    for {
        var value = rand.Intn(100)
        ch <- value
        fmt.Printf("send %d\n", value)
    }
}

func recv(ch chan int) {
    for {
        value := <- ch
        fmt.Printf("recv %d\n", value)
        time.Sleep(time.Second)
    }
}

func main() {
    var ch = make(chan int, 1)
    // 子协程循环读
    go recv(ch)
    // 主协程循环写
    send(ch)
}
