from pathlib import Path
from typing import List
from datetime import datetime
import random

import streamlit as st
import pandas as pd
from pythainlp.word_vector import WordVector
# from streamlit_extras.switch_page_button import switch_page


ROOT_DIR = Path(__file__).parent
WORD_POOL_DIR = str(ROOT_DIR / 'data' / 'thai_noun.txt')
wv = WordVector()

st.set_page_config(
    page_title="Home",
    page_icon="⏱️",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)


def get_words():
    """ get list of words from txt file """
    with open(WORD_POOL_DIR, encoding='utf-8', mode='r') as wordspool:
        pool = wordspool.read()
        return pool.split("\n")


def random_pick_word(word_list: List[str]) -> str:
    """ random choose new words everyday"""
    now = datetime.now()
    seed = now.day + now.month + now.year
    random.seed(seed)

    return random.sample(word_list, 1)[0]


def guess_word(input_word:str, today_word:str) -> int:
    """ calculate similarity between words"""
    try:
        if input_word == today_word:
            return st.switch_page("pages/Finish.py")
        else:
            sim_score = wv.similarity(input_word, today_word)
            st.session_state['status'] = "ลองใหม่นะครับ"
            return float(abs(sim_score))
    except Exception as e:
        print(e)
        st.session_state['status'] = "อ่านไม่ออกอะครับ"
        return None


def save_to_dataframe(input_text: str, today_word:str) -> None:
    """ save input value to dataframe"""
    # Check if DataFrame exists
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame(columns=['input_text', 'score'])
    
    score = guess_word(input_text, today_word)
    if score:
        new_guess = pd.DataFrame([{'input_text': input_text, "score": score}])
    # Append input to DataFrame
        st.session_state['data'] = pd.concat(
            [st.session_state['data'], new_guess]
        )
    st.session_state['data'] = st.session_state['data'].reset_index(drop=True)
    st.session_state['data'] = st.session_state['data'].drop_duplicates()
    
    st.session_state['data'] = st.session_state['data'].sort_values(
        by='score', ascending=False
        )
    st.session_state['data'] = st.session_state['data'].head(5)

def submit():
    """remove previous sumitted text"""
    st.session_state['input_text'] = st.session_state['input_box']
    st.session_state['input_box'] = ""


def main():
    word_list = get_words()
    current_word = random_pick_word(word_list=word_list)
    # Submit button
    title = "<h1 style='text-align: center; color: #F15094;'>คอนเท็กโต้ เซินเจิ้น</h1>"
    st.markdown(title, unsafe_allow_html=True)
    st.text_input("Enter your text here:", key='input_box')
    columns = st.columns(3)
    # Input box
    with columns[1]:
        if st.button("Submit", on_click=submit):
            # Save input as DataFrame
            save_to_dataframe(st.session_state['input_text'], current_word)
        if 'status' not in st.session_state:
            st.write("", key='status')
        else:
            st.write(st.session_state['status'])
        if 'data' in st.session_state:
            st.write("Previous answer:")
            for n in range(0, len(st.session_state['data'])):

                st.markdown("""
                <style>
                .stProgress > div > div > div > div {
                        background-image: linear-gradient(to right, #BFFF87, #FFA665);
                    }
                </style>
                """, unsafe_allow_html=True)
                percentage = st.session_state['data'].iloc[n]['score']
                print('persentage: ', percentage)
                value = st.session_state['data'].iloc[n]['input_text']
                text = value + str(int((1-percentage)* 1000))
                st.progress(percentage, text=text)






if __name__ == "__main__":
    main()