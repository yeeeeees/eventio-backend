import json
import unittest
from app.schema import schema
from app import create_app, db
from graphene.test import Client
from app.config import TestingConfig


class TestCreateUser(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self.query = '''mutation{
                          createUser(email:"test@user.com", username:"test_user", password:"test", fname:"test", surname:"dummy"){
                            success
                          }
                        }'''

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_okay_register(self):

        response = self.client.post("/graphql", data={"query": self.query})
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("createUser").get("success") == True

    def test_taken_username_register(self):

        query2 = '''mutation{
                      createUser(email:"test2@user.com", username:"test_user", password:"test", fname:"test", surname:"dummy"){
                        success
                        message
                      }
                    }'''

        self.client.post("/graphql", data={"query": self.query})
        response = self.client.post("/graphql", data={"query": query2})
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("createUser").get("message") == "That username is already taken. Plesae try again with different username."

    def test_taken_email_register(self):

        query2 = '''mutation{
                     createUser(email:"test@user.com", username:"test_user2", password:"test", fname:"test", surname:"dummy"){
                       success
                       message
                      }
                    }'''

        self.client.post("/graphql", data={"query": self.query})
        response = self.client.post("/graphql", data={"query": query2})
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("createUser").get("message") == "That email is already in use. Plesae try again with different email."


class TestLoginUser(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        query = '''mutation{
                     createUser(email:"test@user.com", username:"test_user", password:"test", fname:"test", surname:"dummy"){
                       success
                       message
                      }
                    }'''

        self.client.post("/graphql", data={"query": query})

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_successful_login(self):
        query = '''mutation{
                     loginUser(username:"test_user", password:"test"){
                       success
                       message
                     }
                   }'''
        response = self.client.post("/graphql", data={"query": query})
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("loginUser").get("success") == True

    def test_no_info_login(self):
        query = '''mutation{
                     loginUser(password:"test"){
                       success
                       message
                     }
                   }'''
        response = self.client.post("/graphql", data={"query": query})
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("loginUser").get("message") == "Please enter your email/username to login."

    def test_invalid_username(self):
        query = '''mutation{
                     loginUser(username:"wrong_name", password:"test"){
                       success
                       message
                     }
                   }'''
        response = self.client.post("/graphql", data={"query": query})
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("loginUser").get("message") == "Invalid username/email or password."

    def test_invalid_email(self):
        query = '''mutation{
                     loginUser(email:"wrong_email", password:"test"){
                       success
                       message
                     }
                   }'''
        response = self.client.post("/graphql", data={"query": query})
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("loginUser").get("message") == "Invalid username/email or password."

    def test_invalid_password(self):
        query = '''mutation{
                     loginUser(username:"test_user", password:"wrong_pw"){
                       success
                       message
                     }
                   }'''
        response = self.client.post("/graphql", data={"query": query})
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("loginUser").get("message") == "Invalid username/email or password."


class TestCreatAccessToken(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        query = '''mutation{
                     createUser(email:"test@user.com", username:"test_user", password:"test", fname:"test", surname:"dummy"){
                       success
                       message
                      }
                    }'''

        self.client.post("/graphql", data={"query": query})

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def get_refresh_token(self, username, password):
        query = '''mutation{
                     loginUser(username:"test_user", password:"test"){
                       success
                       message
                       refreshToken
                     }
                   }'''
        response = self.client.post("/graphql", data={"query": query})
        data = json.loads(response.get_data(as_text=True))

        return data.get("data").get("loginUser").get("refreshToken")

    def test_successful_refresh_token(self):
        query = '''mutation{
                   getAccessToken {
                     accessToken
                     success
                     message
                   }
                 }'''
        headers = {"Authorization": "Bearer " + self.get_refresh_token("test_user", "test")}
        response = self.client.post("/graphql", data={"query": query}, headers=headers)
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("getAccessToken").get("message") == "Access token created successfully."


class TestEditUser(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        query = '''mutation{
                     createUser(email:"test@user.com", username:"test_user", password:"test", fname:"test", surname:"dummy"){
                       success
                       message
                      }
                    }'''

        self.client.post("/graphql", data={"query": query})

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def get_access_token(self, username, password):
        query = '''mutation{
                     loginUser(username:"test_user", password:"test"){
                       success
                       message
                       accessToken
                     }
                   }'''

        response = self.client.post("/graphql", data={"query": query})
        data = json.loads(response.get_data(as_text=True))

        return data.get("data").get("loginUser").get("accessToken")

    def test_successful_edit(self):
        query = '''mutation{
                     editUser(username:"test_user_changed"){
                       success
                       message
                       user{
                         username
                       }
                     }
                   }'''

        headers = {"Authorization": "Bearer " + self.get_access_token("test_user", "test")}
        response = self.client.post("/graphql", data={"query": query}, headers=headers)
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("editUser").get("success") == True
        assert data.get("data").get("editUser").get("user").get("username") == "test_user_changed"

    def test_no_data_supplied(self):
        query = '''mutation{
                     editUser{
                       success
                       message
                       user{
                         username
                       }
                     }
                   }'''

        headers = {"Authorization": "Bearer " + self.get_access_token("test_user", "test")}
        response = self.client.post("/graphql", data={"query": query}, headers=headers)
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("editUser").get("message") == "Please supply some data to edit user with."

    def test_username_taken(self):
        query = '''mutation{
                    editUser(username:"test_user"){
                      success
                      message
                    }
                 }'''

        headers = {"Authorization": "Bearer " + self.get_access_token("test_user", "test")}
        response = self.client.post("/graphql", data={"query": query}, headers=headers)
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("editUser").get("message") == "That username is already taken. Please try again with different username."

    def test_email_taken(self):
        query = '''mutation{
                    editUser(email:"test@user.com"){
                      success
                      message
                    }
                 }'''

        headers = {"Authorization": "Bearer " + self.get_access_token("test_user", "test")}
        response = self.client.post("/graphql", data={"query": query}, headers=headers)
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("editUser").get("message") == "That email is already in use. Please try again with different email."


class TestDeleteUser:

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

        query = '''mutation{
                     createUser(email:"test@user.com", username:"test_user", password:"test", fname:"test", surname:"dummy"){
                       success
                       message
                      }
                    }'''

        self.client.post("/graphql", data={"query": query})

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def get_access_token(self, username, password):
        query = '''mutation{
                     loginUser(username:"test_user", password:"test"){
                       success
                       message
                       accessToken
                     }
                   }'''
        response = self.client.post("/graphql", data={"query": query})
        data = json.loads(response.get_data(as_text=True))

        return data.get("data").get("loginUser").get("accessToken")

    def test_successful_user_delete(self):
        query = '''mutation{
                     deleteUser{
                       success
                       message
                     }
                   }'''
        headers = {"Authorization": "Bearer " + self.get_access_token("test_user", "test")}
        response = self.client.post("/graphql", data={"query": query}, headers=headers)
        data = json.loads(response.get_data(as_text=True))

        assert data.get("data").get("deleteUser").get("success") == True
