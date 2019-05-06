package main

import "fmt"
import "unsafe"

func main() {
    // head = {address, 10, 10}
    // body = [1,2,3,4,5,6,7,8,9,10]
    var s = []int{1,2,3,4,5,6,7,8,9,10}
    // address 是二级指针
    // 切片分为切片头和内部数组两部分, &s 是一个指向 切片s 头部指针 的地址
    var address = (**[10]int)(unsafe.Pointer(&s))
    var len1 = (*int)(unsafe.Pointer(uintptr(unsafe.Pointer(&s)) + uintptr(8)))
    var cap1 = (*int)(unsafe.Pointer(uintptr(unsafe.Pointer(&s)) + uintptr(16)))
    fmt.Println(address, *len1, *cap1)
    var body = **address
    for i:=0; i< len(body); i++ {
        fmt.Printf("%d ", body[i])
    }
}
