package main

import (
	"fmt"
)

type newPerson struct {
	first   string
	last    string
	address string
}

func changeMe(p *newPerson) {
	//fmt.Println(*p)
	(*p).address = "Bangalore, India"
}
func pointerStuff() {

	p1 := newPerson{
		first:   "James",
		last:    "Bond",
		address: "Buckingham Palace, London",
	}

	fmt.Println("Person")
	fmt.Println("\tName:\t ", p1.first, p1.last)
	fmt.Println("\tAddress: ", p1.address)

	changeMe(&p1)

	fmt.Println("\tAddress: ", p1.address)

}
