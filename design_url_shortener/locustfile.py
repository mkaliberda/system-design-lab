# locustfile.py
import random
from locust import HttpUser, task, constant


class AliasGeneratorUser(HttpUser):
    """
    A user class that simulates generating and fetching aliases.
    Users send requests as fast as possible (constant(0)).
    #
    """

    wait_time = constant(0)
    # Users send requests as fast as possible (virtually no wait)

    # Make sure this matches where your FastAPI application is running
    # Example: host = "http://127.0.0.1:8000"
    host = "http://localhost:8000"

    # You can adjust the task weights if you want a different distribution
    @task(3)  # This task will be run 3 time
    def generate_random_alias(self):
        # Replace with your actual POST data
        response = self.client.post("/shortener/", json={"url": "https://example.com"})
        if response.status_code == 200:
            short_url = response.json().get("short_url")
            if short_url:
                # After every 100 generations, try to open a random one
                for _ in range(100):
                    self.client.get(short_url)
