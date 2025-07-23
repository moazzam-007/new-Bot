import requests
from config import Telegram
headers = {
    "accesstoken": f"{Telegram.EXTRAPE_SESSION_SECRET}",
}

cookies = {
    "accessToken": headers["accesstoken"]
}


def convert_rest(input_text: str, bitly_convert: bool = False, advance_mode: bool = False) -> dict:
    url = "https://www.extrape.com/handler/convertText"
    data = {
        "inputText": input_text,
        "bitlyConvert": bitly_convert,
        "advanceMode": advance_mode
    }
    return requests.post(url, headers=headers, cookies=cookies, json=data).json()


def shorten_link(long_url, custom_alias=None):
    base_url = "https://tinyurl.com/api-create.php"
    params = {'url': long_url}
    if custom_alias:
        params['alias'] = custom_alias
    response = requests.get(base_url, params=params)
    return response.text


def amazon_convert(url):
    response = requests.get(url)
    final_url = response.url

    for tag in Telegram.FILTER_AMAZON_TAGS:
        if tag in final_url:
            final_url = final_url.replace(tag, Telegram.YOUR_AMAZON_TAG)

    return shorten_link(final_url)

