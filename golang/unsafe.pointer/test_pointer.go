package main

import "fmt"
import "unsafe"

/*
type ArbitraryType int

type Pointer *ArbitraryType

可以看到unsafe.Pointer其实就是一个*int,一个通用型的指针
*/
func main() {
	i:= 10
	ip:=&i

	var fp *float64 = (*float64)(unsafe.Pointer(ip))

	*fp = *fp * 3

	fmt.Println(i)
}
