package main

import "fmt"
import "time"

var (
    domainSyncChan = make(chan int, 10)
)

func domainPut(num int) {
    defer func() {
        err := recover()
        if err != nil {
            fmt.Println("error to chan put.")
        }
    }()
    domainSyncChan <- num

    panic("error....")
}

func main() {
    for i := 0; i < 10; i++ {
        domainName := i
        fmt.Println(i)
        go domainPut(domainName)
    }
    time.Sleep(time.Second * 2)
}
