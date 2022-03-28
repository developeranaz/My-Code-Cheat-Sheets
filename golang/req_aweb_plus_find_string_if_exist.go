package main

import (
        "fmt"
        "io/ioutil"
        "net/http"
        "strings"
        "time"
)

func main() {

        for {
                c := http.Client{Timeout: time.Duration(1) * time.Second}
                resp, err := c.Get("http://127.0.0.1:8080")
                if err != nil {
                        continue
                }

                defer resp.Body.Close()
                body, err := ioutil.ReadAll(resp.Body)
                responseString := string(body)
                substr := "usery"
                if strings.Contains(responseString, substr) {
                        fmt.Println("The substring is present in the string.")
                } else {
                        fmt.Println("The substring is not present in the string.")
                }

        }

}
