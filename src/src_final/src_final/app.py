"""Streamlit chat interface for the GoldenAI Music Score Assistant."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from agent.music_score_agent import ask_music_agent


load_dotenv()

st.set_page_config(
    page_title="GoldenAI Music Score Assistant",
    page_icon="🎵",
    layout="centered",
)

st.title("🎵 GoldenAI Music Score Assistant")
st.caption(
    "直接输入大白话，例如：帮我看 P01B 的市场评分和综合评分。"
)

if not os.getenv("OPENAI_API_KEY"):
    st.warning(
        "尚未检测到 OPENAI_API_KEY。请先在项目根目录的 .env 文件中填写。"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "例如：P01A 和 P01B 哪一个更适合先测试？"
)

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("正在查询歌曲评分..."):
            try:
                answer = ask_music_agent(question)
            except Exception as exc:
                answer = (
                    "运行失败。请确认 API Key、依赖和 data/song_scores.csv "
                    f"均已准备好。错误：`{exc}`"
                )
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
