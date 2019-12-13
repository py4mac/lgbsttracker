rest-code:
	protoc -I=./rest -I=./common \
		--python_out=../server/protos/rest \
		./common/light_sensor.proto \
		./rest/generic.proto \
		./rest/service.proto