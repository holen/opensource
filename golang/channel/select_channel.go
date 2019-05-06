package main

import "fmt"
import "time"

func send(ch chan int, gap time.Duration) {
    i := 0
    for {
        i++
        ch <- i
        time.Sleep(gap)
    }
}

func recv(ch1 chan int, ch2 chan int) {
    for {
        /*
	Go 语言为这种使用场景带来了「多路复用」语法糖，也就是下面要讲的 select 语句，它可以同时管理多个通道读写，
	如果所有通道都不能读写，它就整体阻塞，只要有一个通道可以读写，它就会继续。
	*/
        select {
            case v := <- ch1:
                fmt.Printf("recv %d from ch1\n", v)
            case v := <- ch2:
                fmt.Printf("recv %d from ch2\n", v)
        }
    }
}

func main() {
    var ch1 = make(chan int)
    var ch2 = make(chan int)
    go send(ch1, time.Second)
    go send(ch2, 2 * time.Second)
    recv(ch1, ch2)

    /*
    多路利用的 写通道形式 
    select {
      case ch1 <- v:
          fmt.Println("send to ch1")
      case ch2 <- v:
          fmt.Println("send to ch2")
    }
    */
}
