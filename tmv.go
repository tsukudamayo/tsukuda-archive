package main

import (
    "fmt"
    "os"
    "path/filepath"
)

func main() {
    fileName := filepath.Base(os.Args[1])
    dstDir := os.Args[2]
    dstFile := filepath.Join(dstDir, fileName)
    
    if err := os.Rename(os.Args[1], dstFile); err != nil {
        fmt.Println(err)
    }
}
