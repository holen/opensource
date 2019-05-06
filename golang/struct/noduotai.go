// Go 语言的结构体没有多态性
package main

import "fmt"

type Fruit struct {}

func (f Fruit) eat() {
    fmt.Println("eat fruit")
}

func (f Fruit) enjoy() {
    fmt.Println("smell first")
    // 调用的 eat 方法还是 Fruit 自己的 eat 方法，它没能被外面的结构体方法覆盖掉
    f.eat()
    fmt.Println("clean finally")
}

type Apple struct {
    Fruit
}

func (a Apple) eat() {
    fmt.Println("eat apple")
}

type Banana struct {
    Fruit
}

func (b Banana) eat() {
    fmt.Println("eat banana")
}

func main() {
    var apple = Apple {}
    var banana = Banana {}
    apple.enjoy()
    banana.enjoy()
    apple.eat()
    banana.eat()
}
// Go 语言的结构体明确不支持这种形式的多态，外结构体的方法不能覆盖内部结构体的方法。

// smell first
// eat fruit
// clean finally
// smell first
// eat fruit
// clean finally
