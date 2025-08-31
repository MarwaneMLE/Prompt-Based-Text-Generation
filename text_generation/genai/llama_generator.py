from groq import Groq

def ask_llama(message): 
    client = Groq(api_key=GROQ_API_KEY)

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
        {
            "role": "system",
            "content": "AI Chatbot"
        },
        {
            "role": "user",
            "content": "Conversation"
        },
        {
            "role": "assistant",
            "content": "I'm happy to chat with you. How's your day going so far?\n\n(Type a response, ask a question, or share a topic you'd like to discuss. I'm all ears... or rather, all text!)"
        },
        {
            "role": "user",
            "content": message
        }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None
    )
    L = []
    for chunk in completion:
        L.append(chunk.choices[0].delta.content)
    return L

