import streamlit as st
import pandas as pd
import crawler as cr
import problems as pb


def show_message():
    st.title("問題進捗確認")
    st.write("AtCoderの問題の進捗を確認することができます。")


def input_student_ids() -> list:
    student_ids = []
    for i in range(1, 6):
        student_id = st.text_input(f"AtCoder IDを入力してください({i}人目)")
        if student_id != "":
            student_ids.append(student_id)
    if student_ids == []:
        student_ids.append("chokudai")
    return student_ids


def select_course() -> str:
    course = st.selectbox(
        label="選択してください",
        options=(
            "A-四則演算",
            "A-条件分岐",
            "B-文字列",
            "B-forループ",
            "C-リスト",
            "C-1次予選過去問",
            "S1-whileループ",
            "S1-多重ループ",
            "S1-多次元リスト",
            "S2-組み込み関数",
            "S2-組み込み関数(上級)",
            "S2-ソート関数",
            "S2-ソート関数(上級)",
            "S3-関数の定義",
            "S3-再帰関数",
            "S3-再帰関数(上級)",
            "手動入力",
        ),
    )
    return course


def select_crawl_mode() -> str:
    crawl_mode = st.selectbox(
        label="モードを選択してください",
        options=(
            "高速モード：直近の提出のみ参照",
            "詳細モード：過去の提出も参照",
        ),
    )
    return crawl_mode


def get_problems_by_course(course: str) -> list:
    if course == "A-四則演算":
        return pb.A_calc
    elif course == "A-条件分岐":
        return pb.A_if
    elif course == "B-文字列":
        return pb.B_string
    elif course == "B-forループ":
        return pb.B_for
    elif course == "C-リスト":
        return pb.C_list
    elif course == "C-1次予選過去問":
        return pb.C_kakomon
    elif course == "S1-whileループ":
        return pb.S1_while
    elif course == "S1-多重ループ":
        return pb.S1_multi
    elif course == "S1-多次元リスト":
        return pb.S1_multi_list
    elif course == "S2-組み込み関数":
        return pb.S2_Built_in_functions
    elif course == "S2-組み込み関数(上級)":
        return pb.S2_Built_in_functions_Advance
    elif course == "S2-ソート関数":
        return pb.S2_sort
    elif course == "S2-ソート関数(上級)":
        return pb.S2_sort_Advance
    elif course == "S3-関数の定義":
        return pb.S3_function
    elif course == "S3-再帰関数":
        return pb.S3_recursive
    elif course == "S3-再帰関数(上級)":
        return pb.S3_recursive_Advance
    else:
        return []


def input_problems() -> dict:
    crawler = cr.Crawler()
    course_detail = {}
    for i in range(1, 6):
        url = st.text_input(f"問題ページのURLを入力してください({i}問目)")
        if url != "":
            # urlから問題名を取得
            if url in pb.url_to_problem_name.keys():
                problem_name = pb.url_to_problem_name[url]
            else:
                problem_name = crawler.fetch_problem_name(self=crawler, url=url)
            course_detail[url] = problem_name
    if course_detail == {}:
        course_detail["https://atcoder.jp/contests/practice/tasks/practice_1"] = (
            "A - Welcome to AtCoder"
        )
    return course_detail


def get_course_detail() -> dict:
    course = select_course()
    if course != "手動入力":
        problems = get_problems_by_course(course)
        course_detail = {}
        for problem in problems:
            course_detail[problem] = pb.url_to_problem_name.get(problem, "問題名不明")
        return course_detail
    else:
        return input_problems()


def ditect_submission_detail_color(result_text: str) -> str:
    color_map = {
        "AC": "lightgreen",
        "WA": "orange",
        "TLE": "orange",
        "RE": "orange",
        "CE": "orange",
    }
    return color_map.get(result_text, "lightgray")


def make_dataframe(
    student_ids: list, course_detail: dict, crawl_mode: str
) -> pd.DataFrame:
    data = {
        "問題リンク": [
            f'<a href="{url}" target="_blank">{name}</a>'
            for url, name in course_detail.items()
        ]
    }
    for student_id in student_ids:
        data[student_id] = []
    if crawl_mode.startswith("高速"):
        return fast_mode(data, student_ids, course_detail)
    else:
        return detail_mode(data, student_ids, course_detail)


def fast_mode(
    data: pd.DataFrame, student_ids: list, course_detail: dict
) -> pd.DataFrame:
    crawler = cr.Crawler()
    for url in course_detail.keys():
        results = crawler.fetch_result_by_problem(crawler, url, student_ids)
        for student_id in student_ids:
            result_text, submission_detail = results[student_id]
            color = ditect_submission_detail_color(result_text)
            if submission_detail != "":
                data[student_id].append(
                    f'<div style="text-align: center; background-color: {color};"><a href="{submission_detail}" target="_blank">{result_text}</a></div>'
                )
            else:
                data[student_id].append(
                    f'<div style="text-align: center; background-color: {color};">{result_text}</div>'
                )
    return pd.DataFrame(data)


def detail_mode(
    data: pd.DataFrame, student_ids: list, course_detail: dict
) -> pd.DataFrame:
    crawler = cr.Crawler()
    for student_id in student_ids:
        for url in course_detail.keys():
            result_text, submission_detail = crawler.fetch_result_by_user(
                crawler, url, student_id
            )
            color = ditect_submission_detail_color(result_text)
            if submission_detail != "":
                data[student_id].append(
                    f'<div style="text-align: center; background-color: {color};"><a href="{submission_detail}" target="_blank">{result_text}</a></div>'
                )
            else:
                data[student_id].append(
                    f'<div style="text-align: center; background-color: {color};">{result_text}</div>'
                )
    return pd.DataFrame(data)


def main():
    show_message()
    student_ids = input_student_ids()
    course_detail = get_course_detail()
    crawl_mode = select_crawl_mode()
    if st.button("進捗を確認する"):
        df = make_dataframe(student_ids, course_detail, crawl_mode)
        st.write(
            # htmlでリンクを有効化、ヘッダを中央揃え
            df.to_html(escape=False, index=False).replace(
                "<th>", '<th style="text-align: center;">'
            ),
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
