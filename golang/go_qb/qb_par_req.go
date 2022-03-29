package main

// Copyright (C) 2022 - DevAnaZ
// Distributed under terms of the MIT license.

import (
        "fmt"
        "sync"
        "os/exec"
)



func ad() {
        cmd := exec.Command("sleep", "50")
        cmd.Run()
}


func as() {
        cmd := exec.Command("sleep", "100")
        cmd.Run()
}

func main() {

        var wg sync.WaitGroup

        fmt.Printf( "On your mark, Get set, GO!\n" )

        wg.Add( 2 )
        go ad()
        go as()

        wg.Wait()
        fmt.Printf( "All athletes have finished\n" )

}


//Parallelized two functions ad and as
