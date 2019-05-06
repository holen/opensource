package main

import "fmt"
import "unsafe"

/*
uintptr可以转换为unsafe.Pointer
unsafe.Pointer可以转换为uintptr
主要用于 *T1 和 *T2 两个指针类型之间的转换，我们都知道 *T 是不能计算偏移量的，也不能进行计算，但是 uintptr 可以，
所以我们可以把指针转为uintptr再进行偏移计算，这样我们就可以访问特定的内存了，达到对不同的内存读写的目的
*/

func main() {
	u:=new(user)
	fmt.Println(*u)
	// 因为name是第一个字段，所以不用偏移
	pName:=(*string)(unsafe.Pointer(u))
	*pName="张三"
	// 我们要先把user的指针地址转为uintptr，然后我们再通过unsafe.Offsetof(u.age)获取需要偏移的值，进行地址运算(+)偏移即可
	pAge:=(*int)(unsafe.Pointer(uintptr(unsafe.Pointer(u))+unsafe.Offsetof(u.age)))
	*pAge = 20

	fmt.Println(*u)
}

type user struct {
	name string
	age int
}
