package main

import (
	"fmt"
	"sort"
)

type Person struct {
	Name string
	Age  int
}

type ByName []Person

func (p ByName) Len() int           { return len(p) }
func (p ByName) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }
func (p ByName) Less(i, j int) bool { return p[i].Name < p[j].Name }

type ByAge []Person

func (p ByAge) Len() int           { return len(p) }
func (p ByAge) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }
func (p ByAge) Less(i, j int) bool { return p[i].Age < p[j].Age }

func sortExamples() {

	p1 := Person{
		Name: "Daniel",
		Age:  15,
	}
	p2 := Person{
		Name: "Zach",
		Age:  32,
	}
	p3 := Person{
		Name: "San",
		Age:  42,
	}
	p4 := Person{
		Name: "CrazyJoe",
		Age:  51,
	}

	people := []Person{p1, p2, p3, p4}
	fmt.Println(people)
	sort.Sort(ByName(people))
	fmt.Printf("Sorted by Name....\n")
	fmt.Printf("%v\n", people)
	sort.Sort(ByAge(people))
	fmt.Printf("Sorted by Age....\n")
	fmt.Printf("%v", people)
}
