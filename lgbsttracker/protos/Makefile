rest-server:
	protoc -I. -I/usr/local/go/src/github.com/grpc-ecosystem/grpc-gateway \
		--python_out=. \
		light_sensor.proto \
		generic.proto \
		sensors_api.proto

swagger-doc:
	protoc -I. -I/usr/local/go/src/github.com/grpc-ecosystem/grpc-gateway \
		--swagger_out=logtostderr=true:../server/doc \
		sensors_api.proto
	mv ../server/doc/sensors_api.swagger.json ../server/doc/swagger.json

grpc-server:
	python -m grpc_tools.protoc \
		--python_out=. --grpc_python_out=. \
		-I. -I/usr/local/include \
		sensors_service.proto

deps:
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
	go get -u github.com/golang/protobuf/protoc-gen-go