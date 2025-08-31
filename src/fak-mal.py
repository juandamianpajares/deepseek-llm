# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI
client = OpenAI(api_key="sk-7d3758c80b8445d393261bc997466fc1", base_url="https://api.deepseek.com/v1/chat/completions")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=True
)

print(response.choices[0].message.content)
