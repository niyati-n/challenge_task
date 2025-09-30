"""Simple public test for candidate to run"""

import json
import requests
import csv

SERVER_URL = "http://localhost:8090"


def test_chat_completions():
    """Test OpenAI proxy endpoint"""
    url = f"{SERVER_URL}/v1/chat/completions"
    payload = {
        # "model": "gpt-5-mini",
        "model": "moonshotai/kimi-k2:free",
        "messages": [{"role": "user", "content": "Hello, respond with just 'Hi!'"}],
        "max_tokens": 10,
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "choices" in data
    content = data["choices"][0]["message"]["content"].strip()
    print(f"✓ Chat completions: {content}")


def test_prefill_simple():
    """Test prefill endpoint with simple email"""
    url = f"{SERVER_URL}/v1/prefill"

    with open("emails/simple_invoice.txt", "r") as f:
        email_text = f.read()

    payload = {"email_text": email_text, "model": "default"}
    response = requests.post(url, json=payload)

    assert response.status_code == 200
    data = response.json()
    print(f"✓ Prefill: {json.dumps(data, separators=(',', ':'))}")
    assert data["success"] is True

    # Show CSV
    import os
    import csv

    if os.path.exists("data.csv"):
        with open("data.csv", "r") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                print(f"Row {i + 1}: {json.dumps(dict(row), separators=(',', ':'))}")


def test_with_prefill_gpt():
    url = f"{SERVER_URL}/v1/prefill/complex"

    with open("emails/simple_invoice.txt", "r") as f:
        email_text = f.read()

    payload = {"email_text": email_text, "model": "moonshotai/kimi-k2:free"}
    response = requests.post(url, json=payload)
    data = response.json()
    
    if data.get("success"):
        print(f"✓ Prefill Complex: {json.dumps(data, separators=(',', ':'))}")
        solution_json = data["solution"]
        solution_json = solution_json.strip("```json").strip("```").strip()
        invoice_data = json.loads(solution_json)
        csv_file = "../data/invoices.csv"
        
        
        with open(csv_file, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=invoice_data.keys())
            f.seek(0)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(invoice_data)
            
        print(f"Invoice saved to {csv_file}")
    else:
        print("Prefill failed.")
    

def cleanup_csv():
    """Clean up CSV file after tests"""
    import os

    if os.path.exists("data.csv"):
        os.remove("data.csv")
        print("Cleaned up data.csv file")


if __name__ == "__main__":
    try:
        test_chat_completions()
        test_prefill_simple()
        test_with_prefill_gpt()
        print("All tests passed!")
    finally:
        cleanup_csv()
