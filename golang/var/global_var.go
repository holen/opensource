package main

import "fmt"

// 如果全局变量的首字母大写，那么它就是公开的全局变量。如果全局变量的首字母小写，那么它就是内部的全局变量。
// 内部的全局变量只有当前包内的代码可以访问，外面包的代码是不能看见的
var globali int = 24

func main() {
    var locali int = 42
    fmt.Println(globali, locali)
    // 24 42
}
