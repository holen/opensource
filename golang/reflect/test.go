package main

import "fmt"
import "reflect"

/*
反射的目标之一是获取变量的类型信息，例如这个类型的名称、占用字节数、所有的方法列表、所有的内部字段结构、它的底层存储类型等等。

反射的目标之二是动态的修改变量内部字段值。比如 json 的反序列化，你有的是对象内部字段的名称和相应的值，你需要把这些字段的值循环填充到对象相应的字段里。
*/

/*
type Type interface {
  ...
  Method(i int) Method  // 获取挂在类型上的第 i'th 个方法
  ...
  NumMethod() int  // 该类型上总共挂了几个方法
  Name() string // 类型的名称
  PkgPath() string // 所在包的名称
  Size() uintptr // 占用字节数
  String() string // 该类型的字符串形式
  Kind() Kind // 元类型
  ...
  Bits() // 占用多少位
  ChanDir() // 通道的方向
  ...
  Elem() Type // 数组，切片，通道，指针，字典(key)的内部子元素类型
  Field(i int) StructField // 获取结构体的第 i'th 个字段
  ...
  In(i int) Type  // 获取函数第 i'th 个参数类型
  Key() Type // 字典的 key 类型
  Len() int // 数组的长度
  NumIn() int // 函数的参数个数
  NumOut() int // 函数的返回值个数
  Out(i int) Type // 获取函数 第 i'th 个返回值类型
  common() *rtype // 获取类型结构体的共同部分
  uncommon() *uncommonType // 获取类型结构体的不同部分
}
*/

func main() {
    var s int = 42
    // TypeOf(), ValueOf() 这两个方法的参数是 interface{} 类型，意味着调用时编译器首先会将目标变量转换成 interface{} 类型。
    // TypeOf() 方法返回变量的类型信息得到的是一个类型为 reflect.Type 的变量，
    fmt.Println(reflect.TypeOf(s)) // int
    // ValueOf() 方法返回变量的值信息得到的是一个类型为 reflect.Value 的变量
    fmt.Println(reflect.ValueOf(s)) // 42
}

