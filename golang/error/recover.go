package main

import "fmt"

// 虽然 error 捕获成功了，程序不再崩溃，异常点后面的逻辑也不会再继续执行了
var negErr = fmt.Errorf("non positive number")

// panic 抛出的对象未必是错误对象，而 recover() 返回的对象正是 panic 抛出来的对象，所以它也不一定是错误对象
func main() {
    // 匿名函数 func() {…}
    defer func() {
        if err := recover(); err != nil {
            // fmt.Println("error catched"， err)
            // 对 recover() 返回的结果进行判断，以挑选出我们愿意处理的异常对象类型，对于那些不愿意处理的，可以选择再次抛出来，让上层来处理
            if err == negErr {
                fmt.Println("error catched", err)
            } else {
                panic(err)  // rethrow
            }
        }
    }() // 括号 表示对匿名函数进行了调用
    fmt.Println(fact(10))
    fmt.Println(fact(5))
    fmt.Println(fact(-5))
    fmt.Println(fact(15))
}

func fact(a int) int{
    if a <= 0 {
        panic(negErr)
    }
    var r = 1
    for i :=1;i<=a;i++ {
        r *= i
    }
    return r
}
