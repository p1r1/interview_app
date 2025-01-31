import os
import json
from locust import HttpUser, task, between
import random


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings_file = os.path.join(
            os.path.dirname(__file__), ".vscode", "settings.json"
        )
        self.credentials = self._load_credentials()
        self.access_token = None
        self.cid_set = set()

    def _load_credentials(self):
        """Load credentials from vscode settings.json"""
        try:
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                shared_vars = settings.get("rest-client.environmentVariables", {}).get(
                    "$shared", {}
                )
                return {
                    "username": shared_vars.get("YOUR_USER_NAME"),
                    "password": shared_vars.get("YOUR_USER_PASS"),
                    "client_id": shared_vars.get("YOUR_CLIENT_ID"),
                    "client_secret": shared_vars.get("YOUR_CLIENT_SECRET"),
                }
        except FileNotFoundError:
            print(f"Error: {self.settings_file} not found")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON file: {self.settings_file}")
            return {}
        except Exception as e:
            print(f"Error while loading: {e}")
            return {}

    def on_start(self):
        if not self.credentials:
            print("Error: No credentials found, skipping authentication.")
            return
        # get the access token in on_start
        response = self.client.post(
            "/o/token/",
            data={
                "grant_type": "password",
                "username": self.credentials.get("username"),  # Get from settings.json
                "password": self.credentials.get("password"),  # Get from settings.json
                "client_id": self.credentials.get(
                    "client_id"
                ),  # Get from settings.json
                "client_secret": self.credentials.get(
                    "client_secret"
                ),  # Get from settings.json
            },
        )
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
        else:
            print(f"Failed to get token {response.text}")
            self.access_token = None

    def random_cid(self):
        while True:
            random_cid = random.randint(1, 1000000)
            if random_cid not in self.cid_set:
                self.cid_set.add(random_cid)
                return random_cid

    @task
    def list_employees(self):
        if self.access_token:
            self.client.get(
                "/api/employees/",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        else:
            print("No access token. Skipping request to employees endpoint")

    @task
    def create_customer(self):
        if self.access_token:

            self.client.post(
                "/api/customers/",
                json={
                    "C_ID": self.random_cid(),
                    "C_NAME": "Test Customer",
                    "C_EMAIL_ID": "test@example.com",
                    "C_CONT_NO": 9876543210,
                    "C_ADDR": "456 Avenue",
                    "C_TYPE": "Regular",
                    "M_ID": 1,
                },
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        else:
            print("No access token. Skipping request to customers endpoint")

    @task
    def get_customer_shipment_details(self):
        if self.access_token:
            customer_id = random.randint(1, 3)
            self.client.get(
                f"/api/customers/{customer_id}/shipments/",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        else:
            print("No access token. Skipping request to custom customer endpoint")

    @task
    def get_delivered_shipment(self):
        if self.access_token:
            self.client.get(
                f"/api/shipments/delivered/",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        else:
            print(
                "No access token. Skipping request to custom shipment delivered endpoint"
            )
