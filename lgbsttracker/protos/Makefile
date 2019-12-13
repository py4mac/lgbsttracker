GATEWAY_FLAGS := -I. -I/usr/local/include -I$(GOPATH)/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis -I/usr/local/go/src/github.com/grpc-ecosystem/grpc-gateway

rest-code:
	protoc -I=./rest -I=./common \
		--python_out=../server/protos/rest \
		./common/light_sensor.proto \
		./rest/generic.proto \
		./rest/service.proto

swagger-doc:
	protoc $(GATEWAY_FLAGS) \
		-I=./common \
		--swagger_out=logtostderr=true:../server/doc \
		./grpc/service_grpc.proto
	mv ../server/doc/grpc/service_grpc.swagger.json ../server/doc/swagger.json
	rm -rf ../server/doc/grpc/

deps:
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
	go get -u github.com/golang/protobuf/protoc-gen-go