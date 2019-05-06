package main

import "fmt"
import "unsafe"

type Rect struct {
    Width int
    Height int
}

func main() {
    var r = Rect{50, 50}
    // {typeptr, dataptr}
    var s interface{} = r

    var sptrs = *(*[2]*Rect)(unsafe.Pointer(&s))
    // var dataptr *Rect
    var sdataptr = sptrs[1]
    fmt.Println(sdataptr.Width, sdataptr.Height)

    // 修改原对象，看看接口指向的对象是否受到影响
    r.Width = 100
    fmt.Println(sdataptr.Width, sdataptr.Height)
}

