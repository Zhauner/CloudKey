import requests


def get_favicon_from_url(url: str):

    response = requests.get("https://www.google.com/s2/favicons?domain=" + url)

    return response.content


print(get_favicon_from_url('vk.com'))
