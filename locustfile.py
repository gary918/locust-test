from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)
    @task
    def getAPI(self):
        self.client.get("/")