package main

import (
	"fmt"
)

func main() {
	evens := make(chan int)
	go func(e chan int) {
		for i := 0; i <= 10; i++ {
			if i%2 == 0 {
				e <- i
			}
		}
		close(e)
	}(evens)
	for v := range evens {
		fmt.Println(v)
	}
}
