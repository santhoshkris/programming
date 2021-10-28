package main

import (
	"fmt"
)

func main() {
	mm := map[string][]string{
		"bond_james":  {"Shaken,not stirred", "Martini", "Women"},
		"money_penny": {"James Bond", "Literature", "Computer Science"},
		"no_dr":       {"Being evil", "Icecream", "Sunsets"},
	}
	mm["san"] = []string{"hello", "world", "fountain pens"}
	for i, v := range mm {
		fmt.Printf("Record # %v\n", i)
		for j, vv := range v {
			fmt.Printf("\tIndex: %v\t Value: %v\n", j, vv)
		}
	}
}
