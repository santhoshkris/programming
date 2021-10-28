package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/sayHello", func(w http.ResponseWriter, r *http.Request) {
		params := r.URL.Query()
		fmt.Println(params)
		msg := fmt.Sprintf("Hello %s. You are %s years old", params["name"][0], params["age"][0])
		io.WriteString(w, msg)
	})
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func sayHello(msg string) {
	fmt.Println("HELLO ", msg)
}
