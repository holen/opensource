package main

import "fmt"
import "time"

// 每隔一会生产一个数
func send(ch chan int, gap time.Duration) {
    i := 0
    for {
        i++
        ch <- i
        time.Sleep(gap)
    }
}

// 将多个原通道内容拷贝到单一的目标通道
func collect(source chan int, target chan int) {
    for v := range source {
        target <- v
    }
}

// 从目标通道消费数据
func recv(ch chan int) {
    for v := range ch {
        fmt.Printf("receive %d\n", v)
    }
}


func main() {
    var ch1 = make(chan int)
    var ch2 = make(chan int)
    var ch3 = make(chan int)
    go send(ch1, time.Second)
    go send(ch2, 2 * time.Second)
    go collect(ch1, ch3)
    go collect(ch2, ch3)
    recv(ch3)
}

