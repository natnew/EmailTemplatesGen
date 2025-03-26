from openai import OpenAI

def stream_generated_email(input_text, tone, purpose, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    prompt = f"""
You are a helpful assistant that writes emails in a {tone.lower()} tone for business use.

Purpose: {purpose}
Input:
{input_text}

Write the full email, including greeting and sign-off.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You write high-quality emails for professionals."},
            {"role": "user", "content": prompt}
        ],
        stream=True  # 🟢 Enable streaming
    )

    # Yield tokens as they arrive
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
