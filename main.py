import ollama

def ask_bot(user_question):
    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful customer support assitant.
                Be polite, concise, and friendly.
                If you don't know the answer, say so honestly and suggest the user to contact support@comapny.com"""
            },
            {
                "role": "user",
                "content": "user_question"
            }
        ]     
    )   
    return(response["message"]["content"])

#Test
if __name__ == "__main__":
    questions = [
        "How do I reset my password?"
        "What is your refund policy?"
        "My order hasn't arrived yet."
    ]
    for q in questions:
        print(f"\n User: {q}")
        print(f"Bot: {ask_bot(q)}")
        print("-" * 50)
