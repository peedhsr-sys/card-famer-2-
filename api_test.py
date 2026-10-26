import os
import requests
import json
from datetime import datetime

def call_api(url, bearer_token, dpop_token, api_name):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,hi;q=0.8",
        "authorization": f"Bearer {bearer_token}",
        "dpop": dpop_token,
        "pragma": "no-cache",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"\n📡 [{api_name}] चल रहा है...")
    try:
        # कुछ APIs POST हो सकते हैं, लेकिन अभी हम GET से ट्राई कर रहे हैं
        response = requests.get(url, headers=headers, timeout=30)
        print(f"   ✅ Status: {response.status_code}")
        
        try:
            data = response.json()
        except:
            data = {"raw_response": response.text}
            
        return {"api": api_name, "status": response.status_code, "data": data}
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"api": api_name, "status": 0, "error": str(e)}

def main():
    bearer_token = os.environ.get('BEARER_TOKEN', '')
    dpop_token = os.environ.get('DPOP_TOKEN', '')
    
    if not bearer_token or not dpop_token:
        print("❌ Tokens नहीं मिले! GitHub Secrets चेक करें।")
        return

    print("🚀 Agristack Farmer Data Fetching Started...")
    
    # सिर्फ वो APIs जो असली Farmer Data देते हैं (Deduplicated)
    target_apis = [
        {
            "name": "1. Validate Aadhaar",
            "url": "https://upfr.agristack.gov.in/farmer-registry-api-up/agristack/v1/api/admin/general/validateAadhaarNumber?aadhaarNumber=Nzk4OTk2OTYxOTY5"
        },
        {
            "name": "2. Check Farmer Active Status",
            "url": "https://upfr.agristack.gov.in/farmer-registry-api-up/agristack/v1/api/farmerRegistry/checkFarmerIsActiveOrInActive?aadhaarBase64Hash=Nzk4OTk2OTYxOTY5"
        },
        {
            "name": "3. Get Full Farmer Data (V1)",
            "url": "https://upfr.agristack.gov.in/farmer-registry-api-up/agristack/v1/api/farmerRegistry/getFarmerDataByAadhaarV1"
        }
    ]
    
    results = []
    for api in target_apis:
        results.append(call_api(api["url"], bearer_token, dpop_token, api["name"]))
    
    # Final JSON File बनाना
    final_output = {
        "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aadhaar_reference": "Nzk4OTk2OTYxOTY5",
        "results": results
    }
    
    filename = "complete_farmer_data.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
        
    print(f"\n🎉 सफलता! डेटा '{filename}' में सेव हो गया है।")

if __name__ == "__main__":
    main()
