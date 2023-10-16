from requests import get, exceptions
from os import path, remove
from json import dump, load
from datetime import datetime as date

file_path = 'temp.json'

followers = []
following = []


def save(file):
    """ Saves data to file """
    obj_to_save = {
        'followers': followers,
        'following': following,
        'followers_count': len(followers),
        'following_count': len(following),
        'follows_back': list(filter(lambda x: x in followers, following)),
        'dont_follow_back': list(filter(lambda x: x not in followers, following)),
        'time_stamp': date.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        if path.exists(file_path):
            remove(file_path)
        with open(file_path, "w") as json_file:
            dump(obj_to_save, json_file)
    except Exception as e:
        print(e)
        exit(1)


def make_req(username):
    def fetch_data(url, data_list):
        page = 1
        while True:
            response = get(url, params={"page": page, "per_page": 100})
            if response.status_code == 404:
                print("Not found. Check username")
                exit(1)
            elif response.status_code == 200:
                data = response.json()
                if not data:
                    break
                data_list.extend(item.get("login") for item in data)
                page += 1

    followers_url = f"https://api.github.com/users/{username}/followers"
    following_url = f"https://api.github.com/users/{username}/following"

    try:
        fetch_data(followers_url, followers)
        fetch_data(following_url, following)
        save(file_path)
    except exceptions.ConnectionError as e:
        print(f"Not found. Error: {e}")

def load_data(file_path):
    if path.exists(file_path):
        with open(file_path, 'r') as json_file:
            data = load(json_file)
        return data
