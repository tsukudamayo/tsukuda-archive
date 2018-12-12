package main

import (
    "fmt"
    "os"
)

func main() {
    if err := os.Rename(os.Args[1], os.Args[2]); err != nil {
        fmt.Println(err)
    }
}
