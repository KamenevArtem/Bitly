import argparse
import sys
import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(access_token, url):
    url_template = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "long_url": url,
    }
    response = requests.post(url_template, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink
  

def count_clicks(access_token, url):
    url_template = ("https://api-ssl.bitly.com/v4/bitlinks/"
                    "{}/clicks/summary")
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    parsed_bitlink = urlparse(url)
    parsed_bitlink = f"{parsed_bitlink.netloc}{parsed_bitlink.path}"
    url = url_template.format(parsed_bitlink)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count    


def is_bitlink(access_token, url):
    url_template = "https://api-ssl.bitly.com/v4/expand"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    parsed_bitlink = urlparse(url)
    data = {
        "bitlink_id":  f"{parsed_bitlink.netloc}{parsed_bitlink.path}"
    }
    response = requests.post(url_template, headers=headers, json=data)
    return response.ok 


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--link')
    args = parser.parse_args()
    return args


def main():   
    args = parse_arg()
    input_url = args.link
    access_token = os.environ["BITLY_ACCESS_TOKEN"]
    if is_bitlink(access_token, input_url):
        print(count_clicks(access_token, input_url))
        print("Введеный адрес является сокращенным")    
    else:
        print(shorten_link(access_token, input_url))
        print("Введеный адрес не является сокращенным")    


if __name__ == "__main__":
    load_dotenv()
    main()