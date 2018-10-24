package main

import (
    "fmt"
    "io"
    "net/http"
    "crypto/tls"
    "os"
    "flag"
    "path"
)

func main() {
    // ----------------------------------------
    // parse commandline parameter
    // ----------------------------------------
    var filename string
    flag.StringVar(&filename, "o", "", "output-document")
    flag.Parse()
    url := flag.Args()[0]

    if len(filename) == 0 {
        _, filename = path.Split(url)
    }

    // ----------------------------------------
    // ignore checking ssl certificate
    // ----------------------------------------    
    transport := &http.Transport {
        TLSClientConfig: &tls.Config { InsecureSkipVerify: true },
    }
    
    client := &http.Client {
        Transport: transport,
    }

    // ----------------------------------------
    // download
    // ----------------------------------------
    res, err := client.Get(url)
    if err != nil {
        panic(err)
    }
    defer res.Body.Close()

    file, err := os.Create(filename)
    if err != nil {
        panic(err)
    }
    defer file.Close()

    n, err := io.Copy(file, res.Body)
    if err != nil {
        panic(err)
    }

    fmt.Println(n, "bytes down loaded.")
}
