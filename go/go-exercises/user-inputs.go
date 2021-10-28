package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main()  {

	reader := bufio.NewReader(os.Stdin)
	fmt.Printf("Enter your name: ")
	name,_ := reader.ReadString('\n')
	name = strings.TrimRight(name,"\n")
	fmt.Printf("Enter your age: ")
	ageStr,_ := reader.ReadString('\n')
	age,err:= strconv.Atoi(ageStr[:len(ageStr)-1])
	if err != nil {
		fmt.Println(err.Error())
	}
	fmt.Printf("Hello %s, you are %d years old\n", name,age)
}