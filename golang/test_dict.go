package main

import "fmt"
import "unsafe"

func main() {
    // 字典的创建
    var m map[int]string = make(map[int]string)
    fmt.Println(m, len(m))
    // map[] 0

    var a map[int]string = map[int]string{
        90: "优秀",
        80: "良好",
        60: "及格",  // 注意这里逗号不可缺少，否则会报语法错误
    }
    fmt.Println(a, len(a))
    // map[60:及格 80:良好 90:优秀] 3

    var fruits = map[string]int {
           "apple": 2,
           "banana": 5,
           "orange": 8,
    }
    // 读取元素
    var price = fruits["banana"]
    fmt.Println(price)
    // 5

    // 增加或修改元素
    fruits["pear"] = 3
    fmt.Println(fruits)
    // map[apple:2 banana:5 orange:8 pear:3]

    // 删除元素
    delete(fruits, "pear")
    fmt.Println(fruits)
    // map[apple:2 banana:5 orange:8]

    // 判断字典 key 是否存在
    // 字典的下标读取可以返回两个值，使用第二个返回值都表示对应的 key 是否存在
    fmt.Println("字典 key 是否存在")
    var score, ok = fruits["durin"]
    if ok {
        fmt.Println(score)
    } else {
        fmt.Println("durin not exists")
    }

    fruits["durin"] = 0
    score, ok = fruits["durin"]
    if ok {
        fmt.Println("durin exists, and score is: ", score)
    } else {
        fmt.Println("durin still not exists")
    }
    // durin not exists
    // durin exists, and score is:  0

    // 字典的遍历
    fmt.Println("字典的遍历")
    for name, score := range fruits {
        fmt.Println(name, score)
    }

    for name := range fruits {
        fmt.Println(name)
    }
    // orange 8
    // durin 0
    // apple 2
    // banana 5
    // durin
    // apple
    // banana
    // orange

    // 获取字典的 keys 
    fmt.Println("获取字典的 keys")

    var names = make([]string, 0, len(fruits))
    var scores = make([]int, 0, len(fruits))

    for name, score := range fruits {
        names = append(names, name)
        scores = append(scores, score)
    }

    fmt.Println(names, scores)
    // [apple banana orange durin] [2 5 8 0]

    var aas = make([]string, len(fruits))
    var bbs = make([]int, len(fruits))
    for name, score := range fruits {
        aas = append(aas, name)
        bbs = append(bbs, score)
    }

    fmt.Println(aas, bbs)
    // [    banana orange durin apple] [0 0 0 0 5 8 0 2]

    // 字典变量里存的只是一个地址指针，这个指针指向字典的头部对象。
    // 所以字典变量占用的空间是一个字，也就是一个指针的大小，64 位机器是 8 字节，32 位机器是 4 字节
    fmt.Println(unsafe.Sizeof(fruits))
    // 8
}

