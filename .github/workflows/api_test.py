import os
import requests
import time

def run_api_request():
    url = "https://upfr.agristack.gov.in/farmer-registry-api-up/agristack/v1/api/admin/general/validateAadhaarNumber?aadhaarNumber=Nzk4OTk2OTYxOTY5"
    
    # GitHub Secrets से टोकन प्राप्त करें
    bearer_token = os.environ.get('BEARER_TOKEN')
    dpop_token = os.environ.get('DPOP_TOKEN')

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,hi;q=0.8,mr;q=0.7",
        "authorization": f"Bearer {bearer_token}",
        "cache-control": "no-cache",
        "dpop": dpop_token,
        "pragma": "no-cache",
        "referer": "https://upfr.agristack.gov.in/farmer-registry-up/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
    }

    print("API Request भेजा जा रहा है...")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_api_request()