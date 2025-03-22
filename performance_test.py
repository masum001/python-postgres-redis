import requests
import time

# Base URL of your FastAPI app
BASE_URL = "http://localhost:8000"

# Endpoints to test
POSTGRES_ENDPOINT = "/postgres"
REDIS_ENDPOINT = "/redis"

# Data sizes to test (number of rows)
DATA_SIZES = [10000, 20000, 50000, 100000]

# Number of requests to make for each data size
REQUESTS_PER_SIZE = 5

# Function to fetch data from an endpoint
def fetch_data(endpoint, num_requests):
    total_time = 0
    for _ in range(num_requests):
        start_time = time.time()
        response = requests.get(f"{BASE_URL}{endpoint}")
        end_time = time.time()
        if response.status_code == 200:
            total_time += end_time - start_time
        else:
            print(f"Error fetching data from {endpoint}: {response.status_code}")
            return None
    return total_time / num_requests  # Return average response time

# Function to run performance tests
def run_performance_tests():
    for data_size in DATA_SIZES:
        print(f"Testing with {data_size} rows...")

        # Calculate the number of requests needed to fetch the desired data size
        num_requests = data_size // 1000  # Since each request fetches 1000 rows

        # Test PostgreSQL endpoint
        postgres_time = fetch_data(POSTGRES_ENDPOINT, num_requests)
        if postgres_time:
            print(f"PostgreSQL average response time for {data_size} rows: {postgres_time:.4f} seconds")

        # Test Redis endpoint
        redis_time = fetch_data(REDIS_ENDPOINT, num_requests)
        if redis_time:
            print(f"Redis average response time for {data_size} rows: {redis_time:.4f} seconds")

        # Performance comparison
        if postgres_time and redis_time:
            if postgres_time < redis_time:
                print(f"PostgreSQL is faster by {redis_time - postgres_time:.4f} seconds")
            else:
                print(f"Redis is faster by {postgres_time - redis_time:.4f} seconds")

        print("-" * 50)

# Run the performance tests
if __name__ == "__main__":
    run_performance_tests()