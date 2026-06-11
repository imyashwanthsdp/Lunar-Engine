import requests

def send_request(method, url, data=None):
    method = method.upper()

    if method == "GET":
        return requests.get(url)

    elif method == "POST":
        return requests.post(url, json=data)

    elif method == "PUT":
        return requests.put(url, json=data)

    elif method == "DELETE":
        return requests.delete(url)

    else:
        raise Exception("Unsupported method")