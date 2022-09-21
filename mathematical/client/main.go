package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {
	addr, err := net.ResolveUDPAddr("udp4", "127.0.0.1:4000")
	if err != nil {
		panic(err)
	}

	conn, err := net.DialUDP("udp4", nil, addr)
	if err != nil {
		panic(err)
	}

	defer func(conn *net.UDPConn) {
		err := conn.Close()
		if err != nil {
			panic(err)
		}
	}(conn)

	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter equation: ")
	equation, _ := reader.ReadString('\n')
	equation = strings.Replace(equation, "\n", "", -1)
	if err != nil {
		panic(err)
	}
	_, err = conn.Write([]byte(equation))
	if err != nil {
		panic(err)
	}

	buf := make([]byte, 1024)
	n, _, _ := conn.ReadFromUDP(buf)
	if err != nil {
		panic(err)
	}

	println("The response is:", string(buf[0:n]))
}
