import os
import json
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")
print("HF_TOKEN FOUND:", HF_TOKEN is not None)

client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=HF_TOKEN
)

import json
import time
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta"
)

def fallback_tests(endpoint, method):
    return [
        {
            "name": "Basic status check",
            "endpoint": endpoint,
            "method": method,
            "assertions": {
                "status_code": 200,
                "json_keys": []
            }
        }
    ]


def generate_tests(endpoint, method="GET", schema=None):

    prompt = f"""
Generate 3 API test cases in JSON format.

Endpoint: {endpoint}
Method: {method}

Return ONLY JSON array.
"""

    for attempt in range(3):

        try:
            response = client.chat_completion(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )

            content = response.choices[0].message["content"]

            data = json.loads(content)

            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list):
                        return v

            return data

        except Exception as e:
            print(f"⚠ AI attempt {attempt+1} failed: {e}")
            time.sleep(1)

    print("⚠ AI failed completely → using fallback generator")
    return fallback_tests(endpoint, method)