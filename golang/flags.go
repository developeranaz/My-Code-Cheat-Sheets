package main

import (
	"flag"
	"fmt"
)

func main() {
	wordPtr := flag.String("word", "foo", "a string")


	flag.Parse()

	fmt.Println("word:", *wordPtr)

}

