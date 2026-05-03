# AI Customer Support Bot

A fully offline, open-source AI customer support bot.
No API keys. No cloud. No cost. Runs 100% on your machine.

## Tech Stack
| Tool | Purpose |
|------|---------|
| Ollama + Mistral 7B | Local LLM |
| LangChain | RAG pipeline |
| ChromaDB | Vector database |
| HuggingFace Embeddings | Text search |
| Gradio | Chat UI |

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/richakumari0311/ai-support-bot.git
cd ai-support-bot
```

### 2. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Modifying dependencies
Direct dependencies are listed in `requirements.in`.
After editing it, recompile with:
```bash
pip-compile requirements.in --no-annotate --no-header
pip install -r requirements.txt
```

### 4. Install Ollama and pull Mistral
```bash
# Install from https://ollama.com
ollama pull mistral
```

### 5. Add your HuggingFace token
```bash
cp .env.example .env
# Edit .env and add your HF_TOKEN
```

### 6. Add your FAQs
Edit `knowledge_base/faqs.txt` with your own Q&A pairs.

### 7. Run the bot
```bash
python main.py
```
Open http://127.0.0.1:7860 in your browser.

## Customize
- Edit `knowledge_base/faqs.txt` to add your own FAQs
- After editing FAQs run: `python -c "from bot import reload_knowledge_base; reload_knowledge_base()"`
- Edit the system prompt in `bot.py` to change the bot's personality