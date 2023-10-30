import requests
import os
from dotenv import load_dotenv
import random


def check_vk_error(response):
    if response.get('error'):
        raise requests.exceptions.HTTPError


def download_img(filename, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def download_comic():
    filename = 'python.png'
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    response_comic = response.json()
    number_of_comics = response_comic['num']
    random_number = random.randint(1, number_of_comics)
    comic_url = f'https://xkcd.com/{random_number}/info.0.json'
    comic_response = requests.get(comic_url)
    url_of_comic = comic_response.json()['img']
    download_img(filename, url_of_comic)
    return response_comic


def get_upload_url(vk_access_token, vk_group_id, v):
    receive_url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": vk_access_token,
        "group_id": vk_group_id,
        "v": v
    }
    response = requests.get(receive_url, params=params)
    response.raise_for_status()
    received_response = response.json()
    check_vk_error(received_response)
    return received_response


def upload_photo(upload_url):
    with open('python.png', 'rb') as photo:
        files = {
            "photo": photo
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    downloaded_response = response.json()
    check_vk_error(downloaded_response)
    return downloaded_response


def save_photo(vk_access_token, server, vk_group_id, photo, photo_hash, v):
    save_url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "access_token": vk_access_token,
        "group_id": vk_group_id,
        "server": server,
        "photo": photo,
        "hash": photo_hash,
        "v": v
    }
    response = requests.post(save_url, params=params)
    response.raise_for_status()
    saved_response = response.json()
    check_vk_error(saved_response)
    return saved_response


def publish_photo(vk_access_token, vk_group_id, message, attachment, from_group, v):
    publish_url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": vk_access_token,
        "v": v,
        "owner_id": f'-{vk_group_id}',
        "from_group": from_group,
        "message": message,
        "attachment": attachment
    }
    response = requests.post(publish_url, params=params)
    response.raise_for_status()
    published_response = response.json()
    check_vk_error(published_response)
    return published_response


def main():
    load_dotenv()
    vk_access_token = os.environ["VK_ACCESS_TOKEN"]
    vk_group_id = os.environ["VK_GROUP_ID"]
    v = '5.131'

    comic_info = download_comic()
    message = comic_info['alt']

    response = get_upload_url(vk_access_token, vk_group_id, v)
    upload_url = response['response']['upload_url']
    
    try:
        photo_response = upload_photo(upload_url)
        server, photo, photo_hash = photo_func['server'], photo_func['photo'], photo_func['hash']

        album_response = save_photo(vk_access_token, vk_group_id, server, photo, photo_hash, v)
        media_id, owner_id = album_response['response'][0]['id'], album_response['response'][0]['owner_id']

        attachment = f"photo{owner_id}_{media_id}"
        from_group = 1
        publish_photo(vk_access_token, vk_group_id, message, attachment, from_group, v)
    finally:
        os.remove("python.png")


if __name__ == '__main__':
    main()
