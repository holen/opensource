// 结构体中的数组和切片
package main

import "fmt"
import "unsafe"

type ArrayStruct struct {
    value [10]int
}

type SliceStruct struct {
    value []int
}

func main() {
    // 注意下行代码中的数组初始化使用了 […] 语法糖，表示让编译器自动推导数组的长度
    var as = ArrayStruct{[...]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}}
    var ss = SliceStruct{[]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}}
    fmt.Println(unsafe.Sizeof(as), unsafe.Sizeof(ss))
    // 80 24
    // 数组长度为10，value 为 int 类型占 8 字节，共 80 
    // 切片的头部和内容体是分离的，使用指针关联起来。切片头部只有三个 int 类型的变量，占 24 
}
