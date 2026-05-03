import gradio as gr
import os
from bot import(
    load_knowledge_base,
    build_vector_store,
    load_vector_store,
    ask_bot
)

# Load or build vector store on stratup
print("Starting AI Support Bot!")

if not os.path.exists("chroma_db"):
    chunks = load_knowledge_base()
    vector_store = build_vector_store(chunks)
else:
    vector_store = load_vector_store()
print("Bot is ready!\n")

# Chat function Gradio will call

def chat(user_message, history):
    return ask_bot(vector_store, user_message)

# Launch with ChatInterface
app = gr.ChatInterface(
    fn=chat,
    title="AI Customer Support Bot",
    description=(
        "**Fully offline | Powered by Mistral | Built with LangChain + ChromaDB**\n\n"
        "Ask me anything about orders, refunds, shipping, payments and more!\n\n"
        "**Try:** `Where is my order?` | `How do I get a refund?` | "
        "`Do you accept PayPal?` | `My package arrived broken` | `How do I earn reward points?`"
    )
)
    
# Launch
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )

