import requests

user_locations = {}

def get_location(ip):

    response = requests.get(
        f"https://ipinfo.io/{ip}/json"
    )

    data = response.json()

    return data.get("city"), data.get("country")

def detect_location_change(user_email, ip):

    city, country = get_location(ip)

    current_location = f"{city}, {country}"

    if user_email not in user_locations:
        user_locations[user_email] = current_location
        return False

    previous = user_locations[user_email]

    if previous != current_location:
        return True

    return False