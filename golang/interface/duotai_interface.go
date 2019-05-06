package main

import "fmt"

type Fruitable interface {
    eat()
}

// 模拟多态本质上是通过组合属性变量（Name）和接口变量（Fruitable）来做到的，属性变量是对象的数据，而接口变量是对象的功能，将它们组合到一块就形成了一个完整的多态性的结构体。
type Fruit struct {
    Name string  // 属性变量
    Fruitable  // 匿名内嵌接口变量
}

func (f Fruit) want() {
    fmt.Printf("I like ")
    f.eat() // 外结构体会自动继承匿名内嵌变量的方法
}

type Apple struct {}

func (a Apple) eat() {
    fmt.Println("eating apple")
}

type Banana struct {}

func (b Banana) eat() {
    fmt.Println("eating banana")
}

func main() {
    var f1 = Fruit{"Apple", Apple{}}
    var f2 = Fruit{"Banana", Banana{}}
    println(f1.Name)
    f1.want()
    println(f2.Name)
    f2.want()
    // Apple
    // I like eating apple
    // Banana
    // I like eating banana
}

