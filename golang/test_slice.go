package main

import "fmt"

func main() {
    // 切片的创建
    // 切片的「域」就是组成切片变量的三个部分，分别是底层数组的指针、切片的长度和切片的容量 也叫 切片变量
    // 零值切片: 使用 make 函数创建的切片内容是「零值切片」
    var s1 []int = make([]int, 5, 8)
    var s2 []int = make([]int, 8) // 满容切片
    fmt.Println(s1)
    fmt.Println(s2)

    // 使用类型自动推导
    var s3 = make([]int, 5, 8)
    s4 := make([]int, 8)
    fmt.Println(s3)
    fmt.Println(s4)

    // 切片的初始化
    var s []int = []int{1,2,3,4,5}  // 满容的
    fmt.Println(s, len(s), cap(s))

    // 空切片：容量和长度都是零的切
    var s5 []int // 也叫 nil 切片
    var s6 []int = []int{}
    var s7 []int = make([]int, 0)
    fmt.Println(s5, s6, s7)
    fmt.Println(len(s5), len(s6), len(s7))
    fmt.Println(cap(s5), cap(s6), cap(s7))

    // 切片的赋值
    var s8 = make([]int, 5, 8)
    // 切片的访问和数组差不多
    for i := 0; i < len(s8); i++ {
     s8[i] = i + 1
    }
    var s9 = s8
    fmt.Println(s8, len(s8), cap(s8))
    fmt.Println(s9, len(s9), cap(s9))

    // 尝试修改切片内容
    s9[0] = 255
    fmt.Println(s8)
    fmt.Println(s9)

    // 切片的遍历
    fmt.Println("切片的遍历")
    var a = []int{1,2,3,4,5}
    for index := range a {
        fmt.Println(index, a[index])
    }
    for index, value := range a {
        fmt.Println(index, value)
    }

    // 切片的追加
    fmt.Println("切片的追加")
    var a1 = []int{1,2,3,4,5}
    fmt.Println(a1, len(a1), cap(a1))

    // 对满容的切片进行追加会分离底层数组
    var a2 = append(a1, 6)
    fmt.Println(a1, len(a1), cap(a1))
    fmt.Println(a2, len(a2), cap(a2)) // 切片的 cap 变成 10 了

    // 对非满容的切片进行追加会共享底层数组
    var a3 = append(a2, 7)
    fmt.Println(a2, len(a2), cap(a2))
    fmt.Println(a3, len(a3), cap(a3))

    // 下划线变量是 Go 语言特殊的内置变量，它就像一个黑洞，
    // 可以将任意变量赋值给它，但是却不能读取这个特殊变量
    _ = append(a1, 6)

    // 切割切割
    fmt.Println("切割切割")
    var a4 = []int{1,2,3,4,5,6,7}
    // start_index 和 end_index，不包含 end_index
    // [start_index, end_index)
    var a5 = a4[2:5]
    fmt.Println(a4, len(a4), cap(a4))
    fmt.Println(a5, len(a5), cap(a5))

    var b1 = []int{1, 2, 3, 4, 5, 6, 7}
    var b2 = b1[:5]
    var b3 = b1[3:]
    var b4 = b1[:]
    fmt.Println(b1, len(b1), cap(b1))
    fmt.Println(b2, len(b2), cap(b2))
    fmt.Println(b3, len(b3), cap(b3))
    fmt.Println(b4, len(b4), cap(b4))

    // 数组变切片
    fmt.Println("数组变切片")
    var m = [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    var n = m[2:6]
    fmt.Println(n)
    m[4] = 100
    fmt.Println(n)

    // copy
    // 拷贝的量是原切片和目标切片长度的较小值 —— min(len(src), len(dst))
    fmt.Println("copy")
    var d = make([]int, 2, 6)
    var e = copy(d, s) // copy 函数返回的是拷贝的实际长度
    fmt.Println(e, d)
    d[1] = 10
    fmt.Println(s)
    fmt.Println(d)

    // 切片的扩容点
    // 当比较短的切片扩容时，系统会多分配 100% 的空间
    // 但切片长度超过1024时，扩容策略调整为多分配 25% 的空间
    fmt.Println("切片的扩容点")
    f1 := make([]int, 6)
    f2 := make([]int, 1024)
    f1 = append(f1, 1)
    f2 = append(f2, 2)
    fmt.Println(len(f1), cap(f1))
    fmt.Println(len(f2), cap(f2))
}

