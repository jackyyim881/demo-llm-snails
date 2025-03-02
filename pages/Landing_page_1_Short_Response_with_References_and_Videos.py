import streamlit as st
# Set page configuration
st.set_page_config(
    page_title="Snail Sleep Assignment",
    page_icon="🐌",
    layout="wide"
)


def main():
    # Custom CSS for a professional academic look
    st.markdown("""
        <style>
        .title {
            font-size: 48px;
            color: #2E8B57;
            text-align: center;
            font-weight: bold;
        }
        .warning {
            color: #FF4500;
            font-weight: bold;
            font-size: 60px;
            text-align: center;
        }
         .content {
            font-size: 56px;  /* Increased from 18px */
            line-height: 1.8;  /* Increased from 1.6 */
        }
        h2 {
            font-size: 48px;
        }
        p {
            font-size: 36px;
        }
        
        </style>
    """, unsafe_allow_html=True)
    # Title and intro
    st.markdown('<div class="title">Snail Sleep: A Critical Assignment 🐌</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="warning">Worth 50% of the Course Grade</div>',
                unsafe_allow_html=True)
    st.markdown("---")

    # Description and purpose
    st.markdown("""
    <div class="content">
        <h2>Assignment Overview</h2>
        <p>This project explores the fascinating topic of snail sleep, leveraging AI tools to create an informative and engaging study. As a major assessment contributing 50% to the final grade, this assignment requires a deep dive into the biology, behavior, and ecological significance of how snails rest. The use of AI is permitted, making this an innovative blend of technology and science.</p>
    </div>
    """, unsafe_allow_html=True)
    # Description for tranditional chinese
    st.markdown("""
    <div class="content">
        <h2>作業概述</h2>
        <p>本項目探討了蝸牛睡眠這一迷人的主題，利用人工智能工具創建了一個信息豐富且引人入勝的研究。 作為對最終成績貢獻50％的重要評估，此作業要求深入研究蝸牛休息的生物學，行為和生態意義。 允許使用人工智能，使其成為技術和科學的創新結合。</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Short_Response_with_References_and_Videos.py",
                 label="Start Assignment", icon="🚀")


if __name__ == "__main__":
    main()
