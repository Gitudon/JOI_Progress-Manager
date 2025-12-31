import streamlit as st
import pandas as pd
import problems as pb
import crawler as cr

# グローバル変数で状態を管理？
questions = []
questions_urls = []
student_ids = []
mode = "手動入力"


def show_message():
    st.title("問題進捗確認")
    st.write("AtCoderの問題の進捗を確認することができます。")


def input_student_ids():
    global student_ids
    for i in range(1, 6):
        student_id = st.text_input(f"AtCoder IDを入力してください({i}人目)")
        if student_id != "":
            student_ids.append(student_id)
    if student_ids == []:
        student_ids.append("chokudai")
    return


def main():
    show_message()
    input_student_ids()
    if st.button("進捗を確認する"):
        st.write("入力されたAtCoder ID:")
        st.write(student_ids)


if __name__ == "__main__":
    main()
