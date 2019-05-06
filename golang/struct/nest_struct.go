package main

import "fmt"

type Point struct {
    x int
    y int
}

func (p Point) show() {
    fmt.Println(p.x, p.y)
}

type Circle struct {
    loc Point
    Radius int
}

type Circle2 struct {
    // 内嵌的结构体不提供名称
    Point
    Radius int
}

func main() {
    // 内嵌结构体
    var c = Circle {
        loc: Point {
            x: 100,
            y: 100,
        },
        Radius: 50,
    }
    fmt.Printf("%+v\n", c)
    fmt.Printf("%+v\n", c.loc)
    fmt.Printf("%d %d\n", c.loc.x, c.loc.y)
    c.loc.show()
    // {loc:{x:100 y:100} Radius:50}
    // {x:100 y:100}
    // 100 100
    // 100 100

    // 匿名内嵌结构体
    // 匿名的结构体字段将会自动获得以结构体类型的名字命名的字段名称
    var c1 = Circle2 {
        Point: Point {
            x: 100,
            y: 100,
        },
        Radius: 50,
    }
    fmt.Printf("%+v\n", c1)
    fmt.Printf("%+v\n", c1.Point)
    fmt.Printf("%d %d\n", c1.x, c1.y) // 继承了字段
    fmt.Printf("%d %d\n", c1.Point.x, c1.Point.y)
    c1.show() // 继承了方法
    c1.Point.show()
    // {Point:{x:100 y:100} Radius:50}
    // {x:100 y:100}
    // 100 100
    // 100 100
    // 100 100
    // 100 100
}

