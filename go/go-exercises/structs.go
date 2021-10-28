package main

import (
	"fmt"
)

type person struct {
	first       string
	last        string
	iceFlavours []string
}

func structExamples() {
	p1 := person{
		first: "James",
		last:  "Bond",
		iceFlavours: []string{
			"Hazelnut",
			"Strawberry",
			"Bubblegum",
		},
	}
	p2 := person{
		first: "Miss",
		last:  "Moneypenny",
		iceFlavours: []string{
			"Vanilla",
			"Strawberry",
			"Capuccino",
		},
	}

	fmt.Println("Person 1 :")
	fmt.Println("\tName: ", p1.first, p1.last)
	fmt.Println("\tIce cream flavours : ")
	for _, v := range p1.iceFlavours {
		fmt.Printf("\t\t%v\n", v)
	}

	fmt.Println("Person 2 :")
	fmt.Println("\tName: ", p2.first, p2.last)
	fmt.Println("\tIce cream flavours : ")
	for _, v := range p2.iceFlavours {
		fmt.Printf("\t\t%v\n", v)
	}

	mm := make(map[string]person, 3)

	mm[p1.last] = p1
	mm[p2.last] = p2

	fmt.Println(mm)

	xs := struct {
		dict map[string]string
		aa   []string
		t    int
	}{
		dict: map[string]string{
			"deer":  "mammal",
			"viper": "reptile",
		},
		aa: []string{"Hello", "World"},
		t:  10,
	}
	fmt.Println(xs)
}
