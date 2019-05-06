package main

import "fmt"
import "math"

type Circle struct {
    x int
    y int
    Radius int
}

/*
func function_name( [parameter list] ) [return_types] {
    函数体
}
*/
// Go 语言的方法名称也分首字母大小写，它的权限规则和字段一样，首字母大写就是公开方法，首字母小写就是内部方法，只能归属于同一个包的代码才可以访问内部方法。
// 面积
func (c Circle) Area() float64 {
    // Go 语言不喜欢类型的隐式转换，所以需要将整形显示转换成浮点型
    return math.Pi * float64(c.Radius) * float64(c.Radius)
}

// Go 语言的结构体方法里面没有 self 和 this 这样的关键字来指代当前的对象，它是用户自己定义的变量名称，通常我们都使用单个字母来表示 如下例的 c。
// 周长
func (c Circle) Circumference() float64 {
    return 2 * math.Pi * float64(c.Radius)
}

// 通过指针访问内部的字段需要 2 次内存读取操作，第一步是取得指针地址，第二部是读取地址的内容，它比值访问要慢。
// 但是在方法调用时，指针传递可以避免结构体的拷贝操作，结构体比较大时，这种性能的差距就会比较明显
// 半径变长
func (c *Circle) expand() {
    c.Radius *= 2
}

func (c Circle) expand2() {
    // 只不过是把函数的第一个参数挪了位置而已，参数传递时会 复制了一份结构体内容 ，起不到扩大半径的效果
    c.Radius *= 2
    // 复制了一份结构体
    fmt.Println(c.Radius)
}

func main() {
    var c = Circle {Radius: 50}
    fmt.Println(c.Area(), c.Circumference())
    // 7853.981633974483 314.1592653589793
    // 指针变量调用方法形式上是一样的
    var pc = &c
    fmt.Println(pc.Area(), pc.Circumference())
    // 7853.981633974483 314.1592653589793
    c.expand2()
    fmt.Println(c.Radius, c.Area(), c.Circumference())
    // 7853.981633974483 314.1592653589793
    c.expand()
    fmt.Println(c.Radius, c.Area(), c.Circumference())
    // 31415.926535897932 628.3185307179587
}
