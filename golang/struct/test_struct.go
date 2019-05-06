package main

import "fmt"
import "unsafe"

// 结构体类型的定义
type Circle struct {
    // 首字母大写是公开变量 Public，首字母小写是内部变量 Private
    // 内部变量只有属于同一个 package（简单理解就是同一个目录）的代码才能直接访问
    x int
    y int
    Radius int
}

func main() {
    // 结构体变量的创建
    var c Circle = Circle {
        x: 100,
        y: 100,
        Radius: 50,  // 注意这里的逗号不能少
    }
    fmt.Printf("%+v\n", c)
    // {x:100 y:100 Radius:50}

    // 结构体的内存大小
    // Circle 结构体在我的 64位机器上占用了 24 个字节，因为每个 int 类型都是 8 字节。
    // 在 32 位机器上，Circle 结构体只会占用 12 个字节。
    fmt.Println(unsafe.Sizeof(c)) // 24

    var c1 Circle = Circle {
        Radius: 50,
    }
    var c2 Circle = Circle {}
    fmt.Printf("%+v\n", c1)
    fmt.Printf("%+v\n", c2)
    // {x:0 y:0 Radius:50}
    // {x:0 y:0 Radius:0}

    var c3 Circle = Circle {100, 100, 50}
    fmt.Printf("%+v\n", c3)
    // {x:100 y:100 Radius:50}

    // 结构体变量和普通变量都有指针形式，使用取地址符就可以得到结构体的指针类型
    var c4 *Circle = &Circle {100, 100, 50}
    fmt.Printf("%+v\n", c4)
    // &{x:100 y:100 Radius:50}
    // 注意上面的输出，指针形式多了一个地址符 &，表示打印的对象是一个指针类型

    // 使用全局的 new() 函数来创建一个「零值」结构体
    var c5 *Circle = new(Circle)
    fmt.Printf("%+v\n", c5)

    var c6 Circle
    fmt.Printf("%+v\n", c6)

    // nil 结构体是指结构体指针变量没有指向一个实际存在的内存。
    // 这样的指针变量只会占用 1 个指针的存储空间，也就是一个机器字的内存大小。
    // var c7 *Circle = nil

    // 结构体的拷贝
    fmt.Println("结构体的拷贝")
    var a1 Circle = Circle {Radius: 50}
    var a2 Circle = a1
    fmt.Printf("%+v\n", a1)
    fmt.Printf("%+v\n", a2)
    // {x:0 y:0 Radius:50}
    // {x:0 y:0 Radius:50}
    a1.Radius = 100
    fmt.Printf("%+v\n", a1)
    fmt.Printf("%+v\n", a2)
    // {x:0 y:0 Radius:100}
    // {x:0 y:0 Radius:50}

    var a3 *Circle = &Circle {Radius: 50}
    var a4 *Circle = a3
    fmt.Printf("%+v\n", a3)
    fmt.Printf("%+v\n", a4)
    // &{x:0 y:0 Radius:50}
    // &{x:0 y:0 Radius:50}
    a3.Radius = 100
    fmt.Printf("%+v\n", a3)
    fmt.Printf("%+v\n", a4)
    // &{x:0 y:0 Radius:100}
    // &{x:0 y:0 Radius:100}
}
