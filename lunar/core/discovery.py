import requests
import re


def discover_schema(base_url, endpoint, method="GET"):

    # Ensure URL formatting is correct (safe concatenation)
    if not base_url.endswith("/") and not endpoint.startswith("/"):
        url = base_url + "/" + endpoint
    else:
        url = base_url + endpoint

    try:
        response = requests.request(method, url)
    except Exception as e:
        return {
            "status_code": "CONNECTION_ERROR",
            "type": "connection_failed",
            "keys": [],
            "error_msg": str(e)
        }

    try:
        data = response.json()
    except:
        # If response is non-JSON (like HTML or text)
        title = ""
        text = response.text
        if "<title>" in text and "</title>" in text:
            try:
                title = text.split("<title>")[1].split("</title>")[0].strip()
            except:
                pass
        
        # Simple regex to strip HTML tags and obtain a body text preview
        body_text = ""
        try:
            body_text = re.sub(r'<[^>]+>', ' ', text)
            body_text = ' '.join(body_text.split())[:300]
        except:
            body_text = text[:300]

        return {
            "status_code": response.status_code,
            "type": "html" if "text/html" in response.headers.get("Content-Type", "") else "text/plain",
            "content_type": response.headers.get("Content-Type", ""),
            "title": title,
            "text_preview": body_text,
            "headers": list(response.headers.keys())
        }

    if isinstance(data, list):

        if len(data) > 0 and isinstance(data[0], dict):
            keys = list(data[0].keys())
        else:
            keys = []

        return {
            "status_code": response.status_code,
            "type": "array",
            "keys": keys
        }

    if isinstance(data, dict):
        return {
            "status_code": response.status_code,
            "type": "object",
            "keys": list(data.keys())
        }

    return {
        "status_code": response.status_code,
        "type": str(type(data)),
        "keys": []
    }