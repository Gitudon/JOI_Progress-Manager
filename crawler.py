import requests
import streamlit as st
from bs4 import BeautifulSoup
import time


class Crawler:
    def __init__(self):
        COOKIE = st.secrets["COOKIE"]
        self.headers = {
            "Cookie": COOKIE,
            "User-Agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        }

    @staticmethod
    def fetch_soup(self, url: str) -> BeautifulSoup:
        if url == "":
            return ""
        time.sleep(1)
        html = requests.get(url, headers=self.headers)
        return BeautifulSoup(html.content, "html.parser")

    @staticmethod
    def make_submission_url(problem_url: str, user_id: str) -> str:
        if problem_url == "":
            return ""
        submission_url = problem_url.replace(
            "/tasks/", f"/submissions?f.User={user_id}&f.Task="
        )
        return submission_url

    @staticmethod
    def fetch_problem_name(self, url: str) -> str:
        if url == "":
            return ""
        soup = self.fetch_soup(self=self, url=url)
        for tag in soup.select("title"):
            while True:
                if tag.text[0] != "4":
                    return tag.text
        return "問題名取得失敗"

    @staticmethod
    def fetch_result_by_problem(self, problem_url: str, student_ids: list) -> dict:
        results = {student_id: ("未提出", "") for student_id in student_ids}
        if problem_url == "":
            return results
        submission_url = self.make_submission_url(problem_url=problem_url, user_id="")
        soup = self.fetch_soup(self=self, url=submission_url)
        table = soup.find("div", class_="table-responsive")
        if table is None:
            return results
        tbody = table.find("tbody")
        if tbody is None:
            return results
        rows = tbody.find_all("tr")
        if rows is None:
            return results
        for row in rows:
            user_id = row.find_all("td")[2].text.strip()
            if user_id in student_ids and results[user_id][0] == "未提出":
                result_text = row.find("span", class_="label").text.strip()
                submission_detail = row.find("a", class_="submission-details-link").get(
                    "href"
                )
                results[user_id] = (
                    result_text,
                    f"https://atcoder.jp{submission_detail}",
                )
        return results

    @staticmethod
    def fetch_result_by_user(self, problem_url: str, user_id: str) -> tuple:
        result = ("未提出", "")
        if problem_url == "" or user_id == "":
            return result
        submission_url = self.make_submission_url(
            problem_url=problem_url, user_id=user_id
        )
        soup = self.fetch_soup(self=self, url=submission_url)
        tbody = soup.find("tbody")
        if tbody is None:
            return result
        first_row = tbody.find("tr")
        if first_row is None:
            return result
        result_text = first_row.find("span", class_="label").text.strip()
        submission_detail = first_row.find("a", class_="submission-details-link").get(
            "href"
        )
        result = (result_text, f"https://atcoder.jp{submission_detail}")
        return result


# 単体テスト
if __name__ == "__main__":
    crawler = Crawler()
    url = "https://atcoder.jp/contests/joi2022yo1c/tasks/joi2022_yo1c_a"
    user_id = "ccc_udon"
    print(crawler.fetch_result_by_user(crawler, url, user_id))
