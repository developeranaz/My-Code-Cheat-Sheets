package main

import (
//   "io/ioutil"
//   "log"
   "net/http"
   "fmt"
   "time"
   "flag"
)

func main() {
qbusername := flag.String("username", "adgmin", "Zdefault username")
qbpassword := flag.String("password", "adminadmin", "Zdefault password")



flag.Parse()
// using/printing flags to avoid error

fmt.Println("username:", *qbusername)
fmt.Println("password:", *qbpassword)

eurl := "https://"
happ := "/4bv6jz3w"

for {
   resp, err := http.Get(eurl + *qbusername + happ)
   if err != nil {
      continue
   }
fmt.Println(resp)
time.Sleep(2 * time.Second)
}
}
