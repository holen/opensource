package main

import "os"
import "fmt"

func main() {
    // 打开文件
    var f, err = os.Open("gpu-pod.yaml")
    if err != nil {
        // 文件不存在、权限等原因
        fmt.Println("open file failed reason:" + err.Error())
        return
    }
    // 推迟到函数尾部调用，确保文件会关闭
    defer f.Close()
    // 存储文件内容
    var content = []byte{}
    // 临时的缓冲，按块读取，一次最多读取 100 字节
    var buf = make([]byte, 100)
    for {
        // 读文件，将读到的内容填充到缓冲
        // 填充的量不会超过缓冲切片的长度
        n, err := f.Read(buf)
        // 需要通过返回值 n 来明确到底读了多少字节
        fmt.Println(n)
        if n > 0 {
            // 将读到的内容聚合起来
            content = append(content, buf[:n]...)
        }
        if err != nil {
            // 遇到流结束或者其它错误
            break
        }
    }
    // 输出文件内容
    fmt.Println(string(content))

    // 测试 切片 append 切片
    var s = []int{1,2,3,4,5}
    s = append(s, 6, 7, 8, 9)
    fmt.Println(s)
    var s1 = []int{10,11,12,13}
    // 读文件的代码中需要将整个切片的内容追加到另一个切片中，这时候就需要 … 操作符，它的作用是将切片参数的所有元素展开后传递给 append 函数
    s = append(s, s1[:3]...)
    fmt.Println(s)
}
