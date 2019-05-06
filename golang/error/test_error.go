package main

import "fmt"

type SomeError struct {
    Reason string
}

func (s SomeError) Error() string {
    return s.Reason
}

func main() {
    var err error = SomeError{"something happened"}
    fmt.Println(err)
}
