package main

import (
	"fmt"
)

func smile(b, a string) {
	fmt.Println("a in smile():", b)
	fmt.Println("a in smile():", a)
}

func smilo(c, d string) {
	fmt.Println("o in smile():", c)
	fmt.Println("o in smile():", d)
}

func main() {
	a := "an"
	b := "hello"
	c := "howard"
	d := "you"
	//	fmt.Println("a in main():", a)
	smile(a, b)
	// fmt.Println(b, a)
	smilo(c, d)
}
