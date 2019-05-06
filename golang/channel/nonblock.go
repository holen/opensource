package main

import "fmt"
import "time"

func send(ch1 chan int, ch2 chan int) {
    i := 0
    for {
        i++
        // 非阻塞读写需要依靠 select 语句的 default 分支。当 select 语句所有通道都不可读写时，如果定义了 default 分支，那就会执行 default 分支逻辑，这样就起到了不阻塞的效果。
        // select 语句的 default 分支非常关键，它是决定通道读写操作阻塞与否的关键
        select {
            case ch1 <- i:
                fmt.Printf("send ch1 %d\n", i)
            case ch2 <- i:
                fmt.Printf("send ch2 %d\n", i)
            // 如果将 select 语句里面的 default 分支干掉，消费者读到的数据都连续了，但是每个数据只给了一个消费者
            default:
        }
    }
}

func recv(ch chan int, gap time.Duration, name string) {
    for v := range ch {
        fmt.Printf("receive %s %d\n", name, v)
        time.Sleep(gap)
    }
}

func main() {
    // 无缓冲通道
    var ch1 = make(chan int)
    var ch2 = make(chan int)
    // 两个消费者的休眠时间不一样，名称不一样
    go recv(ch1, time.Second, "ch1")
    go recv(ch2, 2 * time.Second, "ch2")
    send(ch1, ch2)
}
