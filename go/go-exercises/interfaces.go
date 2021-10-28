package main

import (
	"fmt"
	"strconv"
)

type circle struct {
	radius float64
}
type square struct {
	length float64
}

func (c circle) area() float64 {
	return (3.714 * (c.radius * c.radius))
}

func (s square) area() float64 {
	return (s.length * s.length)
}

type shape interface {
	area() float64
}

func info(ii shape) {
	f := ii.area()
	switch ii.(type) {
	case circle:
		fmt.Println("Circle it is ...")
		fmt.Printf("Type is %T, return is %v\n", ii, f)
	case square:
		fmt.Println("Square it is...")
		fmt.Printf("Type is %T, return is %v\n", ii, f)
	default:
		fmt.Println("Don't know what type this is...")
	}

}

func interfaceStuff() {
	c1 := circle{
		radius: 10.0,
	}
	sq1 := square{
		length: 12.0,
	}
	fmt.Printf("%T, %T\n", c1, sq1)
	fmt.Println("Area of Circle is : \n", c1.area())
	fmt.Println("Area of Square is : \n", sq1.area())

	info(c1)
	info(sq1)

}
