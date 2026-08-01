import ollama

print("🤖 MatchMind AI is Ready!")

messages = [
    {
        "role": "system",
        "content": "You are MatchMind AI assistant."
    }
]

while True:
    user = input("You: ")

    if user.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    messages.append({
        "role": "user",
        "content": user
    })

    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    ai_reply = response["message"]["content"]

    print("AI:", ai_reply)


    messages.append({
        "role": "assistant",
        "content": ai_reply
    })