import requests
import streamlit as st
from bs4 import BeautifulSoup
import os
import dotenv
import socket
import json
import time


class Crawler:
    def __init__(self):
        # ホスト名で環境を判断
        hostname = socket.gethostname()
        dotenv.load_dotenv()
        if hostname == os.getenv("LOCAL_HOSTNAME"):  # ローカル環境
            COOKIE = os.getenv("COOKIE")
        else:  # オンライン環境
            COOKIE = st.secrets["COOKIE"]
        self.headers = {"Cookie": COOKIE}

    @staticmethod
    def fetch_problem_name(self, url):
        if url == "":
            return ""
        time.sleep(1)
        html = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(html.content, "html.parser")
        for tag in soup.select("title"):
            while True:
                if tag.text[0] != "4":
                    return tag.text
        return "Error: Unable to fetch a problem name"


# 単体テスト
if __name__ == "__main__":
    crawler = Crawler()
    test_url = "https://atcoder.jp/contests/abc269/tasks/abc269_a"
    problem_name = crawler.fetch_problem_name(self=crawler, url=test_url)
    print(problem_name)
