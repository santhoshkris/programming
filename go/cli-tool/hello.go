package main

import (
	"fmt"
)

func main() {
	//fmt.Println("Hello, World")
	//fmt.Printf("%T\n", 42)
	//fmt.Println(strings.Repeat("*",20))
	//fmt.Println(strconv.Itoa(42))
	//fmt.Println(string(42))
	//fmt.Println(7 << 3)
	//fmt.Println(125 >> 3)
	//s := "how are you doing ?"
	//for c := range s {
	//	fmt.Println(c)
	//}
	abc := [...]int{1,2,3,4}
	fmt.Printf("%v, %T\n",abc,abc)
	nums := abc[:]
	fmt.Printf("%v, %T\n",nums,nums)
}
