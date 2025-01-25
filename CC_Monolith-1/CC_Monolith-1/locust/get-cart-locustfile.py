from locust import task, run_single_user, FastHttpUser
from insert_product import login  # Ensure this function is implemented correctly

class AddToCart(FastHttpUser):
    host = "http://localhost:5000"
    username = "test123"
    password = "test123"

    def __init__(self, environment):
        super().__init__(environment)
        cookies = login(self.username, self.password)
        self.token = cookies.get("token") if cookies else None
        if not self.token:
            raise ValueError("Failed to retrieve token during login")
        
        self.default_headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        }

    @task
    def fetch_cart(self):
        headers = {
            **self.default_headers,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Cookie": f"token={self.token}",
            "Referer": "http://localhost:5000/product/1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }

        with self.client.get("/cart", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to fetch cart: {response.text}")

if __name__ == "__main__":
    run_single_user(AddToCart)
