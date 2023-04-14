import requests
import base64


def get_favicon_from_url(url: str):

    response = requests.get("https://www.google.com/s2/favicons?domain=" + url)

    favicon = response.content

    with open('fav.png', 'wb') as decode:
        decode.write(favicon)

    with open('fav.png', 'rb') as encode:
        encoded_string = base64.b64encode(encode.read())

    return encoded_string.decode()
