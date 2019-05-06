package main


import "fmt"


func main() {
    // 指针符号 * 和取地址符 &
    // Go 语言的取地址符是 &，放到一个变量前使用就会返回相应变量的内存地址。
    // 指针变量本质上就是一个整型变量，里面存储的值是另一个变量内存的地址
    // * 操作符存在两次内存读写，第一次获取指针变量的值，也就是内存地址，然后再去拿这个内存地址所在的变量内容。
    var value int = 42
    var p1 *int = &value
    var p2 **int = &p1
    var p3 ***int = &p2
    fmt.Println(p1, p2, p3)
    fmt.Println(*p1, **p2, ***p3)
    // 输出
    // 0xc000084010 0xc00008e018 0xc00008e020
    // 42 42 42
}

