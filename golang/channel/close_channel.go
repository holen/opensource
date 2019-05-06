package main

import "fmt"

func send(ch chan int) {
 ch <- 1
 ch <- 2
 ch <- 3
 ch <- 4
 close(ch)
}

func recv(ch chan int) {
 for v := range ch {
  fmt.Println(v)
 }
}

func main() {
    var ch = make(chan int, 4)
    ch <- 1
    ch <- 2
    close(ch)

    value := <- ch
    fmt.Println(value)
    value = <- ch
    fmt.Println(value)
    value = <- ch
    fmt.Println(value)
    /*
    1
    2
    0
    */
    var ch1 = make(chan int, 4)
    ch1 <- 3
    ch1 <- 4
    close(ch1)
    // for range 遍历通道
    for value := range ch1 {
        fmt.Println(value)
    }

    // 确保通道写安全的最好方式是由负责写通道的协程自己来关闭通道，读通道的协程不要去关闭通道
    var ch2 = make(chan int, 1)
    go send(ch2)
    recv(ch2)
}
