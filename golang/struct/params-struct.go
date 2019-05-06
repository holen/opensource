package main

import "fmt"

type Circle struct {
    x int
    y int
    Radius int
}

func expandByValue(c Circle) {
    c.Radius *= 2
}

func expandByPointer(c *Circle) {
    c.Radius *= 2
}

func main() {
    var c = Circle {Radius: 50}
    expandByValue(c)
    // 值传递涉及到结构体字段的浅拷贝
    fmt.Println(c) // {0 0 50}
    expandByPointer(&c)
    // 指针传递会共享结构体内容，只会拷贝指针地址，规则上和赋值是等价的
    fmt.Println(c) // {0 0 100}
}

