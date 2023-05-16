import requests;
import json;

class TestAuth():
  def __init__(self):
    self.host = "http://127.0.0.1:5000"
    self.token = None
    self.user = None

    self.setUser("test@gmail.com", "111111")
    print("Application initialized.")

    def setUser(self, email, password):
        self.user = {
        "email": email,
        "password": password
        }
        
        print("Testing user:" + self.user['email'])

    def testRegister(self):
        r = requests.get(self.host + "/register", json=self.user)
        token = r.json()["token"]
        self.token = token
        print("registered")
        print("token: " + token)

def main():
  test_app = TestAuth()

  token = test_app.testRegister()



if __name__ == '__main__':
    main() 