package main

import (
    "fmt"
    "log"
    "os"
    "path/filepath"
)

func main() {
    root := "./"
    err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
        if info.IsDir() {
            return nil
        }
        rel, err := filepath.Rel(root, path)
        fmt.Println(rel)
        return nil
    })
    if err != nil {
        log.Fatal(err)
    }
}
