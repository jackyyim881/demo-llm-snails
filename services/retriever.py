from langsmith import traceable
import streamlit as st


@st.cache_data
@traceable(run_type="retriever")
def retriever(query: str):
    # Replace with an actual knowledge base or data source
    results = ["Harrison worked at Kensho"]
    return results


@traceable(metadata={"llm": "grok-beta"})
def rag(question, openai_client):
    docs = retriever(question)
    system_message = f"""Answer the user's question using only the provided information below:

{'\n'.join(docs)}"""

    try:
        response = openai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question},
            ],
            model="grok-beta",  # Ensure you have access to this model
        )

        bot_response = response.choices[0].message.content
        return bot_response
    except Exception as e:
        return "抱歉，我現在無法提供回應。"
