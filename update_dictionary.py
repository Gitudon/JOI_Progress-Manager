import dotenv
from dictionary import url_to_problem_name
from problems import *
from crawler import Crawler


class CrawlerForUpdate(Crawler):
    def __init__(self):
        dotenv.load_dotenv()
        COOKIE = dotenv.get_key(".env", "COOKIE")
        self.headers = {
            "Cookie": COOKIE,
            "User-Agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        }


def update_dictionary() -> dict:
    new_url_to_problem_name = url_to_problem_name.copy()
    crawler = CrawlerForUpdate()
    # ハードコーディングしないようにしたい
    problem_urls = [
        A_calc,
        A_if,
        B_string,
        B_for,
        C_list,
        C_kakomon,
        S1_while,
        S1_multi,
        S1_multi_list,
        S2_Built_in_functions,
        S2_Built_in_functions_advance,
        S2_sort,
        S2_sort_advance,
        S3_function,
        S3_recursive,
        S3_recursive_advance,
        EX1_supplement_of_each_courses_first,
        EX1_supplement_of_each_courses_second,
        EX2_techniques,
        EX2_cumulative_sum,
    ]
    for problem_list in problem_urls:
        for url in problem_list:
            if url not in new_url_to_problem_name.keys():
                problem_name = crawler.fetch_problem_name(self=crawler, url=url)
                new_url_to_problem_name[url] = problem_name
    return new_url_to_problem_name


if __name__ == "__main__":
    new_url_to_problem_name = update_dictionary()
    with open("dictionary.py", "w", encoding="utf-8") as f:
        f.write("# URLと問題名の対応。随時更新。\n")
        f.write("url_to_problem_name = {\n")
        for url, name in new_url_to_problem_name.items():
            f.write(f'    "{url}": "{name}",\n')
        f.write("}\n")
