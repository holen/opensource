package main

import "fmt"
import "unsafe"

func main() {
    fmt.Println(bytes2str(str2bytes("hello")))
}

func str2bytes(s string) []byte {
    // 字符串和字节切片的不同点在于头部，字符串的头部 2 个 int 字节(addr, len)，切片的头部 3 个 int 字节(add, len, cap)
    var strhead = *(*[2]int)(unsafe.Pointer(&s))
    var slicehead [3]int
    slicehead[0] = strhead[0]
    slicehead[1] = strhead[1]
    slicehead[2] = strhead[1]
    return *(*[]byte)(unsafe.Pointer(&slicehead))
}

func bytes2str(bs []byte) string {
    return *(*string)(unsafe.Pointer(&bs))
}
