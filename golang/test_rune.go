package main

import "fmt"

func main() {
    // 按字节遍历
    var s = "嘻哈china"
    fmt.Printf("按字节遍历\n")
    for i:=0;i<len(s);i++ {
        // 可以通过下标来访问内部字节数组具体位置上的字节，字节是 byte 类型
        fmt.Printf("%x ", s[i])
    }
    fmt.Printf("\n")
    // e5 98 bb e5 93 88 63 68 69 6e 61 

    // 按字符 rune 遍历
    fmt.Printf("按字符 rune 遍历\n")
    for codepoint, runeValue := range s {
        // 每次迭代出两个变量 codepoint 和 runeValue。
        // codepoint 表示字符起始位置，runeValue 表示对应的 unicode 编码（类型是 rune）
        fmt.Printf("%d %d ", codepoint, int32(runeValue))
	// 0 22075 3 21704 6 99 7 104 8 105 9 110 10 97 
    }
    fmt.Printf("\n")

    for codepoint, runeValue := range s {
        fmt.Printf("%d %s ", codepoint, string(runeValue))
	// 0 嘻 3 哈 6 c 7 h 8 i 9 n 10 a 
    }
    fmt.Printf("\n")

    // 字节串的内存表示
    var a1 = "hello" // 静态字面量
    var a2 = ""
    for i:=0;i<10;i++ {
      a2 += a1 // 动态构造
    }
    fmt.Println(a1)
    fmt.Println(len(a1)) // 5
    fmt.Println(a2)
    fmt.Println(len(a2)) // 50

    // 字符串是只读的
    // s[0] = 'H' // 会报错

    // 切割
    fmt.Println("切割")
    var b1 = "hello world"
    var b2 = b1[3:8]
    fmt.Println(b2) // lo wo

    // 字节切片和字符串的相互转换
    fmt.Println("字节切片和字符串的相互转换")
    var s1 = "hello world"
    var b = []byte(s1)  // 字符串转字节切片
    var s2 = string(b)  // 字节切片转字符串
    fmt.Println(b)
    fmt.Println(s2)
    // [104 101 108 108 111 32 119 111 114 108 100]
    // hello world

}
