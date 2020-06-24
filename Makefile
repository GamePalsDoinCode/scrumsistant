flask_docker.success: Dockerfile_Flask backend/requirements.txt
	sudo docker build -t latest -t flask --file $< .
	touch $@

websocket_docker.success: Dockerfile_Websocket backend/requirements.txt
	sudo docker build -t latest -t websocket --file $< .
	touch $@

angular_docker.success: Dockerfile_Angular frontend/package-lock.json
	sudo docker build -t latest -t angular --file $< .
	touch $@

.PHONY: buildall run

run: buildall
	sudo docker-compose up

buildall: flask_docker.success websocket_docker.success angular_docker.success

