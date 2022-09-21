package main

import (
	"fmt"
	"github.com/maja42/goval"
	_ "github.com/maja42/goval"
	"math"
	"net"
	"reflect"
)

func evaluateEquation(equation string) string {

	// Mathematical constants (e.g. pi, e, etc)
	variables := map[string]interface{}{}
	variables["pi"] = math.Pi
	variables["e"] = math.E

	// Mathematical functions (e.g. sin, cos, tan, etc)
	functions := make(map[string]goval.ExpressionFunction)
	functions["sin"] = func(args ...interface{}) (interface{}, error) {
		if len(args) != 1 {
			return nil, fmt.Errorf("sin() requires 1 argument")
		}
		return math.Sin(args[0].(float64)), nil
	}
	functions["cos"] = func(args ...interface{}) (interface{}, error) {
		if len(args) != 1 {
			return nil, fmt.Errorf("cos() requires 1 argument")
		}
		return math.Cos(args[0].(float64)), nil
	}
	functions["tan"] = func(args ...interface{}) (interface{}, error) {
		if len(args) != 1 {
			return nil, fmt.Errorf("tan() requires 1 argument")
		}
		return math.Tan(args[0].(float64)), nil
	}
	functions["sqrt"] = func(args ...interface{}) (interface{}, error) {
		// Check if the function has exactly one argument
		if len(args) != 1 {
			return nil, fmt.Errorf("sqrt() requires 1 argument")
		}

		// Force the argument to be a float64 case it is an int
		if reflect.TypeOf(args[0]).Kind() == reflect.Int {
			args[0] = float64(args[0].(int))
		}

		// Check if the argument is non-negative
		if args[0].(float64) < 0 {
			return nil, fmt.Errorf("sqrt() requires non-negative argument")
		}

		return math.Sqrt(args[0].(float64)), nil
	}

	eval := goval.NewEvaluator()
	result, err := eval.Evaluate(equation, variables, functions)
	if err != nil {
		return err.Error()
	}

	return fmt.Sprintf("%v", result)
}

func handleRequest(conn *net.UDPConn, addr *net.UDPAddr, n int, buf []byte) {
	n, addr, err := conn.ReadFromUDP(buf)
	if err != nil {
		panic(err)
	}

	equation := string(buf[0:n])
	println("> Received", equation, "from", addr.String())
	result := evaluateEquation(equation)
	println("> Sending", result, "to", addr.String())

	_, err = conn.WriteToUDP([]byte(result), addr)
	if err != nil {
		panic(err)
	}

}

func main() {
	// Create IPv4 UDP socket address
	addr, err := net.ResolveUDPAddr("udp4", "127.0.0.1:4000")
	if err != nil {
		panic(err)
	}

	// Create UDP socket for receiving requests at port 4000
	conn, err := net.ListenUDP("udp4", addr)
	if err != nil {
		panic(err)
	}

	// Close the socket if an error occurs
	defer func(conn *net.UDPConn) {
		err := conn.Close()
		if err != nil {
			panic(err)
		}
	}(conn)

	// Event loop for receiving requests
	buf := make([]byte, 1024)
	for {
		handleRequest(conn, addr, 0, buf)
	}

}
