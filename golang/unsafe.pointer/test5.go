package main

import "fmt"
import "unsafe"

type Areable interface {
    Area() int
}

type Rect struct {
    Width int
    Height int
}

func (r Rect) Area() int {
    return r.Width * r.Height
}

func main() {
    // {typeptr, dataptr}
    var s interface{} = Rect{50, 50}
    var r Rect = s.(Rect)

    var sptrs = *(*[2]*Rect)(unsafe.Pointer(&s))
    var sdataptr = sptrs[1]

    // 修改原对象
    sdataptr.Width = 100
    // 再对比一下原对象和目标对象
    fmt.Println(sdataptr.Width, sdataptr.Height)
    fmt.Println(r.Width, r.Height)
}
