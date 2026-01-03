import requests
import streamlit as st
from bs4 import BeautifulSoup
import os
import dotenv
import socket
import time
import json


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
    def fetch_soup(self, url: str) -> BeautifulSoup:
        if url == "":
            return ""
        time.sleep(1)
        html = requests.get(url, headers=self.headers)
        return BeautifulSoup(html.content, "html.parser")

    @staticmethod
    def make_submission_url(problem_url: str, user_id: str) -> str:
        # "https://atcoder.jp/contests/joi2022yo1c/tasks/joi2022_yo1c_a"
        if problem_url == "":
            return ""
        problem_id = problem_url.split("/")[-1]
        submission_url = problem_url.replace(
            "/tasks/", f"/submissions?f.User={user_id}&f.Task={problem_id}"
        )
        return submission_url

    @staticmethod
    def fetch_problem_name(self, url: str) -> str:
        # "https://atcoder.jp/contests/joi2022yo1c/tasks/joi2022_yo1c_a"
        if url == "":
            return ""
        soup = self.fetch_soup(self=self, url=url)
        for tag in soup.select("title"):
            while True:
                if tag.text[0] != "4":
                    return tag.text
        return "問題名取得失敗"

    @staticmethod
    def fetch_result_by_user(self, problem_url: str, user_id: str) -> tuple:
        # "https://atcoder.jp/contests/joi2022yo1c/tasks/joi2022_yo1c_a"
        if problem_url == "" or user_id == "":
            return ("", "")
        submission_url = self.make_submission_url(
            self=self, problem_url=problem_url, user_id=user_id
        )
        soup = self.fetch_soup(self=self, url=submission_url)


# 単体テスト
if __name__ == "__main__":
    crawler = Crawler()
    test_url = "https://atcoder.jp/contests/abc269/tasks/abc269_a"
    problem_name = crawler.fetch_problem_name(self=crawler, url=test_url)
    print(problem_name)
