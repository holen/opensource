package main

import "fmt"
import "unsafe"
import "reflect"

/* 定义接口 */
/*
type interface_name interface {
   method_name1 [return_type]
   method_name2 [return_type]
   method_name3 [return_type]
   ...
   method_namen [return_type]
}

// 定义结构体
type struct_name struct {
   // variables
}

// 实现接口方法
func (struct_name_variable struct_name) method_name1() [return_type] {
   // 方法实现 
}
...
func (struct_name_variable struct_name) method_namen() [return_type] {
   // 方法实现
}
*/

// 接口
// 可以闻
type Smellable interface {
  smell()
}

// 可以吃
type Eatable interface {
  eat()
}

// 苹果既可能闻又能吃
type Apple struct {}

func (a Apple) smell() {
  fmt.Println("apple can smell")
}

func (a Apple) eat() {
  fmt.Println("apple can eat")
}

// 花只可以闻
type Flower struct {}

func (f Flower) smell() {
  fmt.Println("flower can smell")
}

type Rect struct {
    Width int
    Height int
}

func main() {
    var s1 Smellable
    var s2 Eatable
    var apple = Apple{}
    var flower = Flower{}
    // Go 语言的接口是隐式的，只要结构体上定义的方法在形式上（名称、参数和返回值）和接口定义的一样，那么这个结构体就自动实现了这个接口
    // 我们就可以使用这个接口变量来指向这个结构体对象
    s1 = apple
    s1.smell()
    s1 = flower
    s1.smell()
    s2 = apple
    s2.eat()

    // 接口变量只包含两个指针字段，那么它的内存占用应该是 2 个机器字
    // 接口变量也是由结构体来定义的，这个结构体包含两个指针字段，一个字段指向被容纳的对象内存，
    // 另一个字段指向一个特殊的结构体 itab，这个特殊的结构体包含了接口的类型信息和被容纳对象的数据类型信息。
    var s interface{}
    fmt.Println(unsafe.Sizeof(s)) // 16
    var arr = [10]int {1,2,3,4,5,6,7,8,9,10}
    fmt.Println(unsafe.Sizeof(arr)) // 80
    s = arr
    fmt.Println(unsafe.Sizeof(s)) // 16

    // 接口变量的赋值
    // 变量赋值本质上是一次内存浅拷贝，切片的赋值是拷贝了切片头，字符串的赋值是拷贝了字符串的头部，而数组的赋值呢是直接拷贝整个数组。
    var a interface {}
    var r = Rect{50, 50}
    a = r

    var rx = a.(Rect) // 类型转换，将 a 转换成 Rect 结构体
    r.Width = 100
    r.Height = 100
    fmt.Println(a) // {50 50}
    fmt.Println(r) // {100 100}
    fmt.Println(rx) // {50 50}
    fmt.Println(reflect.TypeOf(a), reflect.ValueOf(a).Kind()) // main.Rect struct
    fmt.Println(reflect.TypeOf(r), reflect.ValueOf(r).Kind()) // main.Rect struct
    fmt.Println(reflect.TypeOf(rx), reflect.ValueOf(rx).Kind()) // main.Rect struct
    rx.Width = 100
    rx.Height = 100
    fmt.Println(a) // {50 50}
    fmt.Println(rx) // {100 100}

    // 指向指针的接口变量
    var b interface {}
    b = &r // 指向了结构体指针

    var rp = b.(*Rect) // 转换成指针类型
    r.Width = 100
    r.Height = 100
    fmt.Println(rp) // &{100 100}
}
