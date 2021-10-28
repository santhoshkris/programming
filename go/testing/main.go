package main

import (
	"errors"
	"fmt"
)

func main() {

	result, err := divide(100.0, 10.0)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(result)
}

func divide(x, y float32) (float32, error) {
	if y == 0 {
		return 0, errors.New("Cannot divide by 0")
	}
	return x / y, nil
}
