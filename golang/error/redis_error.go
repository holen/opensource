package main

import "fmt"
import "strconv"
import "github.com/go-redis/redis"

func main() {
    // 定义客户端对象，内部包含一个连接池
    var client = redis.NewClient(&redis.Options {
        Addr: "localhost:6379",
    })

    // 定义三个重要的整数变量值，默认都是零
    var val1, val2, val3 int

    // 获取第一个值
    valstr1, err := client.Get("value1").Result()
    if err == nil {
        val1, err = strconv.Atoi(valstr1)
        if err != nil {
            fmt.Println("value1 not a valid integer")
            return
        }
    } else if err != redis.Nil {
        fmt.Println("redis access error reason:" + err.Error())
        return
    }

    // 获取第二个值
    valstr2, err := client.Get("value2").Result()
    if err == nil {
        val2, err = strconv.Atoi(valstr2)
        if err != nil {
            fmt.Println("value1 not a valid integer")
            return
        }
    } else if err != redis.Nil {
        fmt.Println("redis access error reason:" + err.Error())
        return
    }

    // 保存第三个值
    val3 = val1 * val2
    ok, err := client.Set("value3",val3, 0).Result()
    if err != nil {
        fmt.Println("set value error reason:" + err.Error())
        return
    }
    fmt.Println(ok)
}
