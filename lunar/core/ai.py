import os
import json
import time
from huggingface_hub import InferenceClient
from lunar.utils.config import load_config

def get_hf_token():
    # 1. Check environment variable
    token = os.getenv("HF_TOKEN")
    if token:
        return token
    # 2. Check local config file
    config = load_config()
    return config.get("hf_token") or config.get("HF_TOKEN")

def get_inference_client():
    token = get_hf_token()
    # If token is empty string or None, pass None to InferenceClient so it defaults to standard behavior
    return InferenceClient(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        token=token if token else None
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

def generate_tests(endpoint, method=None, schema=None):
    client = get_inference_client()

    is_crud_suite = method is None or method.upper() == "CRUD"

    if is_crud_suite:
        prompt_instruction = f"""
Generate a complete, high-tech API lifecycle test suite containing 5-6 test cases.
Since no specific HTTP method was constrained, you must cover a comprehensive CRUD lifecycle:
1. GET (Retrieve list/schema)
2. POST (Create a resource with realistic JSON body payload matching the discovered keys)
3. PUT (Update the resource with JSON body payload)
4. DELETE (Delete the resource)
5. GET/Negative (Verify 404 behavior on non-existing ID, e.g. {endpoint}/99999)
"""
    else:
        method = method.upper()
        prompt_instruction = f"""
Generate 3 detailed, high-tech test cases specifically focusing on the {method} method for this endpoint.
Include positive path, negative path (invalid data inputs, returning bad request/400 or unauthorized), and edge-case scenarios.
"""

    prompt = f"""
Generate a high-tech API test suite in JSON format for the following target:
Endpoint: {endpoint}
Discovered Schema/Context: {schema}
{prompt_instruction}

Each test case in the JSON array must follow this exact structure:
{{
  "name": "Intelligent and descriptive test name (e.g., 'Verify user registration success')",
  "endpoint": "{endpoint}" or a subpath like "{endpoint}/123" depending on the CRUD action,
  "method": "GET" / "POST" / "PUT" / "DELETE" / "PATCH",
  "headers": {{}}, // Optional: custom headers if needed (e.g., {{"Authorization": "Bearer token"}} or {{"Content-Type": "application/json"}})
  "query_params": {{}}, // Optional: URL query parameters if needed (e.g., {{"limit": 10}})
  "body": null or a JSON object, // Include realistic JSON request body payloads for POST/PUT/PATCH!
  "assertions": {{
    "status_code": 200, // Expected HTTP status code (200, 201, 400, 404, etc.)
    "content_type": "application/json", // Optional: content type checks (e.g. "application/json", "text/html")
    "contains_text": ["keyword1"], // Optional: check if body text contains specific keywords
    "json_keys": ["key1", "key2"], // Optional: check for existence of JSON keys in response object
    "json_types": {{
      "key1": "string",
      "key2": "int",
      "key3": "bool",
      "key4": "array"
    }}, // Optional: check response key data types (supported: "str", "int", "float", "bool", "list", "dict")
    "json_values": {{
      "key2": 100
    }}, // Optional: assert exact values of specific response fields
    "max_response_time_ms": 1500 // Optional: latency performance threshold check in ms
  }}
}}

Return ONLY a valid JSON array of these test case objects. Do not wrap it in markdown block, do not include any other text or explanations.
"""

    for attempt in range(3):
        try:
            response = client.chat_completion(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )

            message = response.choices[0].message
            content = message.content if hasattr(message, "content") else message.get("content", "")
            
            content = content.strip()
            
            # Clean up markdown code blocks if present
            if content.startswith("```"):
                lines = content.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()

            data = json.loads(content)

            if isinstance(data, dict):
                # If AI wrapped tests inside an object
                for v in data.values():
                    if isinstance(v, list):
                        return v

            return data

        except Exception as e:
            print(f"⚠ AI attempt {attempt+1} failed: {e}")
            time.sleep(1)

    print("⚠ AI failed completely → using fallback generator")
    return fallback_tests(endpoint, method)