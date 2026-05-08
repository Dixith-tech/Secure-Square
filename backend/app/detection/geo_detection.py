import requests


def get_location(ip):
    url = f"https://ipinfo.io/{ip}/json"

    response = requests.get(url)

    data = response.json()

    return {
        "city": data.get("city"),
        "country": data.get("country")
    }