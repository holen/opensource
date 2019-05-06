package main

import "fmt"
import "unsafe"
import "reflect"

/*
unsafe包含以下资源：

三个函数：

func Alignof（variable ArbitraryType）uintptr
func Offsetof（selector ArbitraryType）uintptr
func Sizeof（variable ArbitraryType）uintptr

和一种类型：

类型 Pointer * ArbitraryType
*/

type Rect struct {
    Width int
    Height int
}

func main() {
    var r = Rect {50, 50}
    // Pointer 代表着变量的内存地址，可以将任意变量的地址转换成 Pointer 类型，也可以将 Pointer 类型转换成任意的指针类型，它是不同指针类型之间互转的中间类型
    // *Rect => Pointer => *int => int
    fmt.Println(unsafe.Pointer(&r))	// 0xc0000160d0
    fmt.Println(reflect.TypeOf(unsafe.Pointer(&r))) // unsafe.Pointer
    fmt.Println((*int)(unsafe.Pointer(&r)))	// 0xc0000160d0
    fmt.Println(reflect.TypeOf((*int)(unsafe.Pointer(&r)))) // *int
    var width = *(*int)(unsafe.Pointer(&r))
    // *Rect => Pointer => uintptr => Pointer => *int => int
    // var height = *(*int)(unsafe.Pointer(uintptr(unsafe.Pointer(&r)) + uintptr(8)))
    var height = *(*int)(unsafe.Pointer(uintptr(unsafe.Pointer(&r)) + unsafe.Offsetof(r.Height)))
    fmt.Println(width, height)
    /*
    0xc0000160d0
    0xc0000160d0
    50 50
    */

    // var pw *int
    var pw = (*int)(unsafe.Pointer(&r))
    // var ph *int
    var ph = (*int)(unsafe.Pointer(uintptr(unsafe.Pointer(&r)) + uintptr(8)))
    *pw = 100
    *ph = 100
    fmt.Println(r.Width, r.Height) // 100 100
}

