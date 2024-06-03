import requests


def check_url_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return False
        else:
            return True
    except requests.exceptions.RequestException as e:
        print(f"Exception occurred: {e}")
