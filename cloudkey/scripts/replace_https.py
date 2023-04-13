

def short_url(url: str):

    if url[:5] == "https":

        name = url[8:].split("/")
        return name[0]

    elif url[:4] == "http":

        name = url[7:].split("/")
        return name[0]

    else:
        return ""


print(short_url("https://fox.com/index=0?1312"))
