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
    @task(3)  # This task will be run 3 times more often than the counter task
    def generate_random_alias(self):
        """Simulates a user generating a random alias."""
        url = f"https://example.com/long-url-{random.randint(1, 1_000_000)}"
        self.client.post(
            "/shortener/",
            json={
                "url": url,
            },
            name="/shortener/",  # Custom name for statistics
        )
