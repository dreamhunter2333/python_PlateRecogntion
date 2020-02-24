#!bin/bash
if [ $# -eq 0 ]
then
    echo "flask_image is starting";
    docker-compose -f docker-compose.yml up;
elif [ $# -eq 1 ]
then 
    if [ $1 == "down" ]
    then
    	echo "flask_image is downing";
    	docker-compose -f docker-compose.yml down;
    elif [ $1 == "build" ]
    then
	echo "flask_image is building";
	docker build -f Dockerfile -t flask_image:1.0 .;
    else
	echo "参数错误";
    fi
else
    echo "参数错误";
fi
