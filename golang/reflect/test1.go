package main

import "reflect"
import "fmt"

/*
type Value struct {
  typ *rtype  // 变量的类型结构体
  ptr unsafe.Pointer // 数据指针
  flag uintptr // 标志位
}
*/

func main() {
    type SomeInt int
    var s SomeInt = 42
    var t = reflect.TypeOf(s)
    var v = reflect.ValueOf(s)
    // reflect.ValueOf(s).Type() 等价于 reflect.TypeOf(s)
    // Value 结构体的 Type() 方法也可以返回变量的类型信息
    fmt.Println(t == v.Type())
    fmt.Println(v.Kind() == reflect.Int) // 元类型
    // 通过 Value 结构体提供的 Interface() 方法可以将 Value 还原成原来的变量值。
    // 将 Value 还原成原来的变量
    var is = v.Interface()
    fmt.Println(is.(SomeInt))
}

/*
 func (v Value) SetLen(n int)  // 修改切片的 len 属性
 func (v Value) SetCap(n int) // 修改切片的 cap 属性
 func (v Value) SetMapIndex(key, val Value) // 修改字典 kv
 func (v Value) Send(x Value) // 向通道发送一个值
 func (v Value) Recv() (x Value, ok bool) // 从通道接受一个值
 // Send 和 Recv 的非阻塞版本
 func (v Value) TryRecv() (x Value, ok bool)
 func (v Value) TrySend(x Value) bool

 // 获取切片、字符串、数组的具体位置的值进行读写
 func (v Value) Index(i int) Value
 // 根据名称获取结构体的内部字段值进行读写
 func (v Value) FieldByName(name string) Value
 // 将接口变量装成数组，一个是类型指针，一个是数据指针
 func (v Value) InterfaceData() [2]uintptr
 // 根据名称获取结构体的方法进行调用
 // Value 结构体的数据指针 ptr 可以指向方法体
 func (v Value) MethodByName(name string) Value
 ...
*/
