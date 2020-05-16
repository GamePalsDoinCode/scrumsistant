flask_docker.success: Dockerfile_Flask
	sudo docker build -t latest -t flask --file $< .
	touch $@

websocket_docker.success: Dockerfile_Websocket
	sudo docker build -t latest -t websocket --file $< .
	touch $@

angular_docker.success: Dockerfile_Angular
	sudo docker build -t latest -t angular --file $< .
	touch $@

.PHONY: buildall run

run: buildall
	sudo docker-compose up

buildall: flask_docker.success websocket_docker.success angular_docker.success

