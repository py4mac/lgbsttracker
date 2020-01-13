rest-code:
	protoc -I. -I/usr/local/go/src/github.com/grpc-ecosystem/grpc-gateway \
		--python_out=. \
		common.proto \
		sensors_message.proto \
		api_storage_sensors_service.proto

swagger-doc:
	protoc -I. -I/usr/local/go/src/github.com/grpc-ecosystem/grpc-gateway \
		--swagger_out=logtostderr=true,allow_merge=true:../server/doc \
		api_storage_sensors_service.proto \
		api_service.proto
	mv ../server/doc/apidocs.swagger.json ../server/doc/swagger.json

# grpc-code:
# 	python -m grpc_tools.protoc \
# 		--python_out=. --grpc_python_out=. \
# 		-I. -I/usr/local/include \
# 		sensors_service.proto

deps:
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
	go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger
	go get -u github.com/golang/protobuf/protoc-gen-go