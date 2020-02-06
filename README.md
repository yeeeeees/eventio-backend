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


If you are using REST Clients like Postman or Insomnia, you might want to import schema for auto-completiton and introspection. Assuming you are in project root directory, type this:
```python
>>> from app.schema import schema
>>> print(schema)
schema {
  query: Query
  mutation: Mutation
}

type CreateEvent {
  event: Event
  message: String
  success: Boolean
}

type CreateUser {
  user: User
  message: String
  success: Boolean
}

type DeleteEvent {
  message: String
  success: Boolean
}

type DeleteUser {
  message: String
  success: Boolean
}

type EditEvent {
  event: Event
  message: String
  success: Boolean
}

type EditUser {
  user: User
  message: String
  success: Boolean
}

type Event implements Node {
  uuid: ID!
  title: String!
  datePosted: String!
  location: String
  description: String
  organizerUuid: Int!
  organizer: User
  joinedUsers(before: String, after: String, first: Int, last: Int): UserConnection
  id: ID!
}

type EventConnection {
  pageInfo: PageInfo!
  edges: [EventEdge]!
}

type EventConnectionsConnection {
  pageInfo: PageInfo!
  edges: [EventConnectionsEdge]!
}

type EventConnectionsEdge {
  node: Event
  cursor: String!
}

type EventEdge {
  node: Event
  cursor: String!
}

enum EventSortEnum {
  UUID_ASC
  UUID_DESC
  TITLE_ASC
  TITLE_DESC
  DATE_POSTED_ASC
  DATE_POSTED_DESC
  LOCATION_ASC
  LOCATION_DESC
  DESCRIPTION_ASC
  DESCRIPTION_DESC
  ORGANIZER_UUID_ASC
  ORGANIZER_UUID_DESC
}

type JoinEvent {
  event: Event
  user: User
  message: String
  success: Boolean
}

type LeaveEvent {
  event: Event
  user: User
  message: String
  success: Boolean
}

type Login {
  message: String
  success: Boolean
  accessToken: String
  user: User
}

type Mutation {
  createUser(email: String!, fname: String!, password: String!, surname: String!, username: String!): CreateUser
  loginUser(email: String, password: String!, username: String): Login
  editUser(email: String, fname: String, password: String, surname: String, username: String, uuid: Int!): EditUser
  deleteUser(uuid: Int!): DeleteUser
  createEvent(description: String!, organizerUuid: Int!, title: String!): CreateEvent
  editEvent(description: String, title: String, uuid: Int!): EditEvent
  joinEvent(eventUuid: Int!, userUuid: Int!): JoinEvent
  leaveEvent(eventUuid: Int!, userUuid: Int!): LeaveEvent
  deleteEvent(uuid: Int!): DeleteEvent
}

interface Node {
  id: ID!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Query {
  node(id: ID!): Node
  user(uuid: Int, username: String): User
  event(uuid: Int, title: String): Event
  allUsers(sort: [UserSortEnum] = [UUID_ASC], before: String, after: String, first: Int, last: Int): UserConnectionsConnection
  allEvents(sort: [EventSortEnum] = [UUID_ASC], before: String, after: String, first: Int, last: Int): EventConnectionsConnection
}

type User implements Node {
  uuid: ID!
  username: String!
  fname: String!
  surname: String!
  isVerified: Boolean
  profilePic: String
  email: String!
  password: String!
  createdEvents(before: String, after: String, first: Int, last: Int): EventConnection
  joinedEvents(before: String, after: String, first: Int, last: Int): EventConnection
  id: ID!
}

type UserConnection {
  pageInfo: PageInfo!
  edges: [UserEdge]!
}

type UserConnectionsConnection {
  pageInfo: PageInfo!
  edges: [UserConnectionsEdge]!
}

type UserConnectionsEdge {
  node: User
  cursor: String!
}

type UserEdge {
  node: User
  cursor: String!
}

enum UserSortEnum {
  UUID_ASC
  UUID_DESC
  USERNAME_ASC
  USERNAME_DESC
  FNAME_ASC
  FNAME_DESC
  SURNAME_ASC
  SURNAME_DESC
  IS_VERIFIED_ASC
  IS_VERIFIED_DESC
  PROFILE_PIC_ASC
  PROFILE_PIC_DESC
  EMAIL_ASC
  EMAIL_DESC
  PASSWORD_ASC
  PASSWORD_DESC
}
```
You can paste output or import [schema.gql](schema.gql) to your REST Client of choice and you'll have autocompletition when writing queries.

## Tests

Tests are developed using unittest, standard python testing library and those tests are being run by [nose test runner](https://nose.readthedocs.io/en/latest/).
To run tests, navigate to root project directory and type:
```
$ nosetests 
..............
----------------------------------------------------------------------
Ran 14 tests in 0.784s

OK
```

## Made with
- [Docker](https://docker.com/) - containerzation and virtualization
- [Flask](https://www.palletsprojects.com/p/flask/) - micro web framework 
- [pytest](https://docs.pytest.org/en/latest/) - python library made for testing and mocking
- [Postgres](https://postgres.com/) - open source relational database system
- [GraphQL](https://graphql.org/) - query language for APIs and a runtime for fulfilling queries with existing data