rest-code:
	protoc -I=./rest -I=./common \
		--python_out=../server/protos/rest \
		./common/item.proto \
		./rest/generic.proto \
		./rest/service.proto