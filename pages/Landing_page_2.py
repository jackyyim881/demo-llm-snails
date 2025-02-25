import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Snail Sleep Fun Facts",
    page_icon="🐌",
    layout="wide"
)


def main():
    # Custom CSS for a playful, casual look
    st.markdown("""
        <style>
        .title {
            font-size: 40px;
            color: #4682B4;
            text-align: center;
            font-weight: bold;
        }
        .fun-note {
            color: #FFD700;
            font-style: italic;
            text-align: center;
        }
        .content {
            font-size: 18px;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title and intro
    st.markdown('<div class="title">Snail Sleep: Quirky Cold Knowledge 🐌</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="fun-note">An Extracurricular Adventure - No Grades, Just Fun!</div>',
                unsafe_allow_html=True)
    st.markdown("---")

    # Description and fun facts
    st.markdown("""
    <div class="content">
        <h2>Welcome to Snail Sleep Trivia!</h2>
        <p>This is a casual, extracurricular activity where we explore weird and wonderful facts about snail sleep—powered by AI! Since it’s not graded, relax and enjoy the quirky side of science. Here are some tidbits to get you started:</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
