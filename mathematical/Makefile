run-client:
	go run client/main.go

run-server:
	go run server/main.go

generate-proto:
	protoc --go_out=client/ client/*.proto
	protoc --go_out=server/ server/*.proto

clean:
	rm -rf server/*.pb.go
	rm -rf client/*.pb.go
