package main

import "fmt"

func main() {
    // 数组变量的定义
    var a = [9]int{1, 2, 3, 4, 5, 6, 7, 8, 9}
    var b [10]int = [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    c := [8]int{1, 2, 3, 4, 5, 6, 7, 8}
    var d [9]int
    fmt.Println(a)
    fmt.Println(b)
    fmt.Println(c)
    fmt.Println(d)

    // 数组的访问
    var squares [9]int
    for i := 0; i < len(squares); i++ {
        squares[i] = (i + 1) * (i + 1)
    }
    fmt.Println(squares)

    // 数组赋值
    // 同样的子元素类型并且是同样长度的数组才可以相互赋值
    // 数组的赋值本质上是一种浅拷贝操作，赋值的两个数组变量的值不会共享
    var e = [9]int{1, 2, 3, 4, 5, 6, 7, 8, 9}
    var f [9]int
    f = e
    e[0] = 12345
    fmt.Println(e)
    fmt.Println(f)
    // [12345 2 3 4 5 6 7 8 9]
    // [1 2 3 4 5 6 7 8 9]

    // 数组的下标越界检查（高阶知识）
    var aa = [5]int{1,2,3,4,5}
    // 下标越界报错
    // aa[101] = 255
    fmt.Println(aa)
    // 下标是变量时，Go 会在编译后的代码中插入下标越界检查的逻辑，所以数组的下标访问效率是要打折扣的，比不得 C 语言的数组访问性能
    var ab = [5]int{1,2,3,4,5}
    // 变量要有使用，否则会报错
    // var bb = 101
    // 越界了
    // a[bb] = 255
    fmt.Println(ab)

    // 数组的遍历
    var ac = [5]int{1,2,3,4,5}
    for index := range ac {
        fmt.Println(index, ac[index])
    }
    for index, value := range ac {
        fmt.Println(index, value)
    }
}
