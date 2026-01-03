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


def select_course():
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


def input_problems():
    crawler = cr.Crawler()
    problem_urls = []
    problem_names = []
    for i in range(1, 6):
        url = st.text_input(f"問題ページのURLを入力してください({i}問目)")
        if url != "":
            problem_urls.append(url)
            problem_name = crawler.fetch_problem_name(self=crawler, url=url)
            problem_names.append(problem_name)
    return problem_urls, problem_names


def get_course_details():
    course = select_course()
    if course != "手動入力":
        problems = get_problems_by_course(course)
        problem_names = []
        for problem in problems:
            problem_names.append(pb.url_to_problem_name[problem])
        return problems, problem_names
    else:
        return input_problems()


def make_dataframe(student_ids, problem_urls, problem_names):
    data = {
        "問題リンク": [
            f'<a href="{url}" target="_blank">{name}</a>'
            for url, name in zip(problem_urls, problem_names)
        ]
    }
    # ここに各問題を学生でクロールして進捗を確認する処理を追加
    for student_id in student_ids:
        data[student_id] = ["未確認"] * len(problem_urls)
    df = pd.DataFrame(data)
    return df


def main():
    show_message()
    student_ids = input_student_ids()
    problem_urls, problem_names = get_course_details()
    if st.button("進捗を確認する"):
        df = make_dataframe(student_ids, problem_urls, problem_names)
        st.write(
            # htmlでリンクを有効化、ヘッダを中央揃え
            df.to_html(escape=False, index=False).replace(
                "<th>", '<th style="text-align: center;">'
            ),
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
