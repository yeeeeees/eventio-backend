# eventio 
Calendar on steroids.
**This repository is only for storing backend side of the application. To see mobile application go [here](https://github.com/yeeeeees/eventio-frontend/).**


## Prerequisites
The only thing needed to run and develop this app is [Docker](https://docker.com) and docker-compose.
This is the version of docker which this app was built with.
```
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
To run this app locally, run the following:
```bash
docker-compose up 
```
This will build up all the services that are listed in docker-compose.yml file.

If you are running this project for the first time, tables in the database are not defined. To solve this, open new terminal window and type the following:

```bash
docker exec -it eventio_graphql python create_db.py
```
This will define all the tables and relationships and grant the user needed permissions. 
Also use this command if you make changes to database schema in `app/models.py` or if you just want to flush all the data out of database.

To shut down previously built containers and networks,press `Ctrl+C` or type this:
```bash
docker-compose down
```
This app listens on host's port 5000 and all network interfaces.
If we want to test graphql api:
```bash
$ http POST localhost:5000/graphql query=="query{ allUsers{ edges{ node{ username } } } }"


HTTP/1.0 200 OK
Content-Length: 34
Content-Type: application/json
Date: Wed, 08 Jan 2020 20:51:16 GMT
Server: Werkzeug/0.16.0 Python/3.6.9

{
    "data": {
        "allUsers": {
            "edges": []
        }
    }
}

```
*Since this app listens or all network interfaces, adrresses localhost, 0.0.0.0 and 127.0.0.1 are all accepted*
*This paste was made with [httpie](https://github.com/jakubroztocil/httpie).*

## Made with
- [Docker](https://docker.com/) - containerzation and virtualization
- [Flask](https://www.palletsprojects.com/p/flask/) - micro web framework 
- [pytest](https://docs.pytest.org/en/latest/) - python library made for testing and mocking
- [Postgres](https://postgres.com/) - open source relational database system
- [GraphQL](https://graphql.org/) - query language for APIs and a runtime for fulfilling queries with existing data