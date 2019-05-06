package main

import "fmt"

func main() {
    /* 创建通道
     第一个类型参数限定通道可以容纳的数据类型，再提供第二个整数参数作为通道的容器大小
    */
    // 缓冲型通道，里面只能放整数
    // var bufferedChannel = make(chan int, 1024)
    // 非缓冲型通道
    // 非缓冲型通道必须确保有协程正在尝试读取当前通道，否则写操作就会阻塞直到有其它协程来从通道中读东西
    // var unbufferedChannel = make(chan int)

    var ch chan int = make(chan int, 4)
    // 使用 cap() 和 len() 全局函数获得通道的容量和当前内部的元素个数
    for i:=0; i<cap(ch); i++ {
        ch <- i   // 写通道
    }
    for len(ch) > 0 {
        var value int = <- ch  // 读通道
        fmt.Println(value)
    }
}
