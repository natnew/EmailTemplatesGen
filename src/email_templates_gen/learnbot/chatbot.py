from openai import OpenAI
from learnbot.rag_pipeline import load_index

def stream_answer_from_docs(question, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    db = load_index(openai_api_key=openai_api_key)
    docs = db.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are an AI assistant that explains how a project works using internal documentation.

Context:
{context}

Question:
{question}

Answer clearly and helpfully:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a friendly and knowledgeable assistant who helps explain this AI email project."},
            {"role": "user", "content": prompt}
        ],
        stream=True  # ✅ Streaming enabled
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
