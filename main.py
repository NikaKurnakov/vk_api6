import requests
import os
from dotenv import load_dotenv
import random


def download_img(filename, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_json():
    filename = 'python.png'
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response_json = response.json()
    number_of_comics = response_json['num']
    random_number = random.randint(1, number_of_comics)
    comic_url = f'https://xkcd.com/{random_number}/info.0.json'
    comic_response = requests.get(comic_url)
    url_of_comic = comic_response.json()['img']
    download_img(filename, url_of_comic)
    return response_json


def receive_url(access_token, group_id, v):
    receive_url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": access_token,
        "group_id": group_id,
        "v": v
    }
    response = requests.get(receive_url, params=params)
    response_json = response.json()
    return response_json


def post_photo(upload_url):
    with open('python.png', 'rb') as photo:
        files = {
            "photo": photo
        }
        response = requests.post(upload_url, files=files)
        response_json = response.json()
        print(response_json['hash'])
    return response_json


def save_photo(access_token, server, group_id, photo, photo_hash, v):
    print(photo_hash)
    save_url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "access_token": access_token,
        "group_id": group_id,
        "server": server,
        "photo": photo,
        "hash": photo_hash,
        "v": v
    }
    response = requests.post(save_url, params=params)
    response_json = response.json()
    return response_json


def publish_photo(access_token, group_id, message, attachment, from_group, v):
    publish_url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": access_token,
        "v": v,
        "owner_id": f'-{group_id}',
        "from_group": from_group,
        "message": message,
        "attachment": attachment
    }
    response = requests.post(publish_url, params=params)
    response_json = response.json()
    return response_json


def main():
    load_dotenv()
    access_token = os.environ["ACCESS_TOKEN"]
    group_id = os.environ["GROUP_ID"]
    v = '5.131'

    get_info = get_json()
    message = get_info['alt']

    upload_info = receive_url(access_token, group_id, v)
    upload_url = upload_info['response']['upload_url']

    photo_info = post_photo(upload_url)
    server, photo, photo_hash = photo_info['server'], photo_info['photo'], photo_info['hash']

    save_info = save_photo(access_token, group_id, server, photo, photo_hash, v)
    media_id, owner_id = save_info['response'][0]['id'], save_info['response'][0]['owner_id']

    attachment = f"photo{owner_id}_{media_id}"
    from_group = 1
    publish_photo(access_token, group_id, message, attachment, from_group, v)


if __name__ == '__main__':
    main()