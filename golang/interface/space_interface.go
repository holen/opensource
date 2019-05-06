package main

import "fmt"

func main() {
    // 连续两个大括号，是不是看起来很别扭
    // interface {} 就是 空接口
    var user = map[string]interface{}{
        "age": 30,
        "address": "Beijing Tongzhou",
        "married": true,
    }
    fmt.Println(user)
    // 类型转换语法来了
    var age = user["age"].(int)
    var address = user["address"].(string)
    var married = user["married"].(bool)
    fmt.Println(age, address, married)
}
