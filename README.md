# eventio 
Calendar on steroids.
**This repository is only for storing backend side of the application. To see mobile application go [here]().**


## Prerequisites
The only thing to run and develop this app is [Docker](https://docker.com) and docker-compose.
This is the version of docker which this app was build with.
```bash
$ docker version

Client:
 Version:           18.09.9
 API version:       1.39
 Go version:        go1.13.4
 Git commit:        1752eb3
 Built:             Sat Nov 16 01:05:26 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.09.9
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.13.4
  Git commit:       9552f2b
  Built:            Sat Nov 16 01:07:48 2019
  OS/Arch:          linux/amd64
  Experimental:     false

```


## Getting started
To run this app, run the following:
```bash
docker build -t containername .
```
This will build an image that is based on Python 3.6 with flask.


To run the previously built container, type this:
```bash
docker run -p 5000:5000 containername
```
This runs the container which listens on host's port 5000.
If we want to test this:
```bash
$ http localhost:5000 

HTTP/1.0 200 OK
Content-Length: 21
Content-Type: application/json
Date: Mon, 09 Dec 2019 20:31:33 GMT
Server: Werkzeug/0.16.0 Python/3.6.9

{
    "home": "page"
}


```