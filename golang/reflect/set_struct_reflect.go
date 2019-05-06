package main

import "fmt"
import "reflect"

type Rect struct {
    Width int
    Height int
}

func SetRectAttr(r *Rect, name string, value int) {
    var v = reflect.ValueOf(r)
    var field = v.Elem().FieldByName(name)
    field.SetInt(int64(value))
}

func main() {
    var r = Rect{50, 100}
    SetRectAttr(&r, "Width", 100)
    SetRectAttr(&r, "Height", 200)
    fmt.Println(r)
}
