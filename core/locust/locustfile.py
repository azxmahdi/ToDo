from locust import HttpUser, task , between

class HelloWorldUser(HttpUser):
  wait_time = between(1, 5)

  def on_start(self):
    response = self.client.post('accounts/api/v1/jwt/create/',data={
      "email": "root@gmail.com",
      "password": "123"
    })
    response = response.json()

   
    self.client.headers = {"Authorization": f"Bearer {response.get('access') }"}

  @task
  def task_list(self):
    self.client.get("/api/v1/task/")
