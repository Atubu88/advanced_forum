from locust import HttpUser, TaskSet, task, between
from faker import Faker

fake = Faker()

class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        response = self.client.get("/login/")
        csrftoken = response.cookies['csrftoken']
        self.client.post("/login/", {
            "username": "your_username",
            "password": "your_password",
            "csrfmiddlewaretoken": csrftoken
        }, headers={"X-CSRFToken": csrftoken})

    @task(1)
    def load_home(self):
        with self.client.get("/", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to load home page: {response.status_code}")

    @task(2)
    def view_notifications(self):
        with self.client.get("/notifications/", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to load notifications page: {response.status_code}")

    @task(3)
    def view_subcategory(self):
        with self.client.get("/subcategory/1/", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to load subcategory page: {response.status_code}")

    @task(4)
    def view_topic(self):
        with self.client.get("/topic/1/", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to load topic detail page: {response.status_code}")

    @task(5)
    def leave_comment(self):
        response = self.client.get("/topic/1/")
        csrftoken = response.cookies['csrftoken']
        comment_data = {
            'body': fake.text(),
            'author': 1,  # Замените на соответствующего пользователя
            'topic': 1,   # Замените на соответствующую тему
            'csrfmiddlewaretoken': csrftoken
        }
        with self.client.post("/comment/add/", data=comment_data, headers={"X-CSRFToken": csrftoken}, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Failed to add comment: {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
    host = "http://127.0.0.1:8000"  # Убедитесь, что указали правильный хост вашего приложения
