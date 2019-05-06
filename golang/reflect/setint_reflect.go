package main

import "fmt"
import "reflect"

func main() {
    var s int = 42
    // 反射指针类型
    var v = reflect.ValueOf(&s)
    // 修改的是指针指向的值
    // 要拿出指针指向的元素进行修改
    // 如果不使用 Elem() 方法进行修改也会抛出一样的异常
    v.Elem().SetInt(43)
    fmt.Println(s)
}

