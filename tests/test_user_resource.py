import json

from tests.base import BaseCase

class UserResourceTestCase(BaseCase):

    def setUp(self):
        super().setUp()
        self.user_creation_payload = {
            "username":"CodeYouEmpire",
            "email":"harryndegwa4@gmail.com",
            "password":"testuser"
        }

        self.invalid_user_creation_payload = {
            "email":"harryndegwa4@gmail.com",
            "password":"testuser"
        }

        self.username_user_payload = {
            "username":"CodeYouEmpire",
            "email":"harryndegwa4@gmail.com",
            "password":"testuser"
        }

        self.email_user_payload = {
            "username":"test",
            "email":"harryndegwa4@gmail.com",
            "password":"testuser"
        }

        self.update_payload = {
            "username":"test",
        }

    def create_test_user(self,client):
        res = client.post("/users/",json=self.user_creation_payload)
        data = json.loads(res.data)
        self.assertEqual(data,"User created successfully!")
        self.assertEqual(res.status_code,201)


    def login_user(self,client):
        login_payload = {
            "email":"harryndegwa4@gmail.com",
            "password":"testuser"
        }
        res2 = client.post("/login/",json=login_payload)
        data = json.loads(res2.data)
        self.assertIn("token",data.keys())
        self.assertEqual(res2.status_code,200)
        return data.get("token")


    def test_validate_token(self,token):
        from resources.user_resource import User
        is_valid = User.validate_token(token)
        self.assertIsInstance(is_valid,bool)




    def test_list_users(self):
        with self.app as client:
            self.create_test_user(client)
            token = self.login_user(client)
            res = client.get("/users/",headers={"Authorization":f"Bearer {token}"})
            data = json.loads(res.data.decode("utf-8"))
            self.assertIsInstance(data,list)


    def test_user_creation(self):
        with self.app as client:
            self.create_test_user(client)


    def test_user_creation_with_invalid_payload(self):
        with self.app as client:
            res = client.post("/users/",json=self.invalid_user_creation_payload)
            data = json.loads(res.data)
            self.assertIn("message",data.keys())
            self.assertEqual(res.status_code,400)


    def test_user_creation_with_existing_username(self):
        with self.app as client:
            self.create_test_user(client)
            res2 = client.post("/users/",json=self.username_user_payload)
            data = json.loads(res2.data)
            self.assertEqual(data,"Username already exists!")
            self.assertEqual(res2.status_code,400)


    def test_user_creation_with_existing_email(self):
        with self.app as client:
            self.create_test_user(client)
            res2 = client.post("/users/",json=self.email_user_payload)
            data = json.loads(res2.data)
            self.assertEqual(data,"Email already exists!")
            self.assertEqual(res2.status_code,400)



    def test_get_user_by_valid_id(self):
        test_id = 1
        with self.app as client:
            self.create_test_user(client)
            res2 = client.get(f"/user/{test_id}/")
            data = json.loads(res2.data)
            self.assertEqual(data.get("id"),test_id)
            self.assertIn("username",data.keys())
            self.assertEqual(res2.status_code,200)


    def test_get_user_by_invalid_id(self):
        test_id = 100
        with self.app as client:
            self.create_test_user(client)
            res2 = client.get(f"/user/{test_id}/")
            data = json.loads(res2.data)
            self.assertEqual(data.get("message"),f"User {test_id} does not exist!")
            self.assertEqual(res2.status_code,404)


    def test_update_valid_user(self):
        test_id = 1
        with self.app as client:
            self.create_test_user(client)
            res2 = client.put(f"/user/{test_id}/",json=self.update_payload)
            self.assertEqual(res2.status_code,204)


    def test_update_invalid_user(self):
        test_id = 100
        with self.app as client:
            self.create_test_user(client)
            res2 = client.put(f"/user/{test_id}/",json=self.update_payload)
            self.assertEqual(res2.status_code,404)


    def test_delete_valid_user(self):
        test_id = 1
        with self.app as client:
            self.create_test_user(client)
            res2 = client.delete(f"/user/{test_id}/")
            self.assertEqual(res2.status_code,204)


    def test_delete_invalid_user(self):
        test_id = 100
        with self.app as client:
            self.create_test_user(client)
            res2 = client.delete(f"/user/{test_id}/")
            self.assertEqual(res2.status_code,404)


    def test_user_login_with_valid_credentials(self):
        with self.app as client:
            self.create_test_user(client) 
            self.login_user(client)


    def test_user_login_with_invalid_credentials(self):
        with self.app as client:
            self.create_test_user(client) 
            login_payload = {
                "email":"harryndegwa@gmail.com",
                "password":"testuser"
            }
            res2 = client.post("/login/",json=login_payload)
            data = json.loads(res2.data)
            self.assertIsInstance(data,str)
            self.assertEqual(data,"Wrong email or password!")
            self.assertEqual(res2.status_code,404)

            