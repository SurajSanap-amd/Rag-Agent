Here’s a **clean, professional & complete README.md** for your project (Gemini RAG + Tools + Streamlit).
You can copy and paste directly to your GitHub repository.

---

# 🤖 AI Agent with RAG + Tools (Gemini + Streamlit)

A smart AI Assistant built using **Google Gemini**, with **Retrieval Augmented Generation (RAG)** and **function calling tools**.
It allows you to **upload PDFs/TXT files**, store them in a **Vector Database**, and then **ask questions based on your documents**.

📌 **Tech Stack**:
`Python` · `Streamlit` · `SQLite` · `Gemini API` · `RAG` · `Embeddings` · `Function Calling`

---

## 🚀 Features

| Feature             | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| 📄 Document Upload  | Upload PDF/TXT and convert into embeddings                    |
| 🧠 RAG Search       | Ask queries that read from your uploaded documents            |
| 🔧 Tools            | Calculator, Todo Manager, Document Search                     |
| 💬 Chat Agent       | AI Agent calls tools based on user intent                     |
| 🗄️ Vector DB       | Embeddings stored using SQLite                                |
| 🗂 Manage Documents | View/delete uploaded docs & their chunks                      |
| 🎨 UI/UX            | Modern hacker-style UI with animations, stickers & dark theme |

---

## 🏗️ Project Flow

```
        ┌──────────────┐       ┌──────────────┐
        │  Upload PDF   │─────▶│  Extract Text │
        └──────────────┘       └──────────────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │ Chunk Text   │
                               └──────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Create Embeddings (Gemini) │
                         └─────────────────────────┘
                                      │
                                      ▼
                           ┌────────────────────┐
                           │ Store in SQLite DB │
                           └────────────────────┘
                                      │
                                      ▼
          ┌──────────────┐     ┌───────────────────┐
          │ User Query    │────▶│ AI Agent (Tools + RAG) │
          └──────────────┘     └───────────────────┘
```

---

## 📂 Project Structure

```
Rag-Agent/
│── Home.py                     # Main landing page
│
├── pages/
│   ├── 1_📄_Upload_Documents.py       # Upload & ingest PDFs/TXT
│   ├── 2_🤖_Chat_with_Agent.py        # Chat with AI Agent
│   └── 3_📚_Manage_Documents.py       # View & delete stored docs
│
├── src/
│   ├── config.py                       # API Keys, DB Paths, Upload Dir
│   ├── vectorstore.py                  # Vector DB (SQLite)
│   ├── rag.py                           # RAG ingest + query
│   ├── agent.py                         # Gemini Agent + Tools
│   ├── gemini_client.py                 # Gemini model + embedding utils
│   └── tools.py                         # Tool functions (calc, todo, search)
│
├── utils/
│   ├── text_splitter.py                # Chunking logic
│   └── ui_components.py                # Custom chat bubbles
│
├── static/
│   ├── AI Lens.json                    # Lottie Animation (Optional)
│   ├── upload_sticker.png              # Sticker on Upload Page
│   └── chat_sticker.png                # (Optional) chat illustration
│
├── data/
│   ├── vectordb.sqlite                 # SQLite Embeddings DB
│   └── uploads/                        # Raw uploaded files
│
└── requirements.txt                    # Dependencies
```

---

## 🔐 Setup Instructions

### 📌 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Rag-Agent
```

### 📌 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 📌 3. Configure API Key

Create a `.env` file:

```
GEMINI_API_KEY=your_key_here
```

### 📌 4. Run the App

```bash
streamlit run Home.py
```

---

## 🧰 Tools Used by the Agent

| Tool                     | Description                            |
| ------------------------ | -------------------------------------- |
| 🔎 `search_documents`    | Searches Vector DB for relevant chunks |
| ➕ `calculate_expression` | Math calculator                        |
| 📝 `manage_todos`        | Add/remove/list todos                  |
| 💬 Default Chat          | If no tool matches, responds normally  |

---

## 📌 Future Enhancements (Roadmap)

* 🔐 User login & private docs
* 🤝 Multi-user Chat Memory
* 📊 Document statistics / chart insights
* 🔊 Voice assistant support

---

## 👨‍💻 Built By

**🚀 Suraj Sanap**

> Passionate about AI, Automation & Smart Apps
> *(Add your LinkedIn / GitHub link here)*

---

Would you like me to:

📌 **Add badges (stars, forks, license)**
🎨 **Add screenshots & GIF demo**

Just reply:
➡️ **Yes, add badges**
➡️ **Yes, add screenshots**
or **Both**! 🚀
