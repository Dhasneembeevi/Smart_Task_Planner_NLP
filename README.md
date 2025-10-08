## 🧠 AI Personal Productivity Assistant

An intelligent **task management app** built with **Streamlit** and **Python** that helps users organize, prioritize, and track their daily tasks efficiently. The assistant provides a simple, interactive dashboard to manage tasks with deadlines, priority indicators, and quick completion or deletion actions — all in one place.

---

### 🚀 Features

✅ **Add & Manage Tasks:** Easily create tasks with title, priority, and deadline.
✅ **Priority Highlighting:** Tasks are visually color-coded — High, Medium, and Low priority.
✅ **Top 3 Tasks Today:** Automatically identifies and displays the top three urgent tasks based on deadlines and priority.
✅ **Task Completion Tracking:** Mark tasks as done and store them persistently.
✅ **Delete with Confirmation:** Secure deletion via confirmation pop-up without page reload.
✅ **Persistent Storage:** Tasks are saved in a CSV file and loaded on every launch.
✅ **Interactive UI:** Built using Streamlit for a smooth, real-time user experience.

---

### 🧩 Tech Stack

* **Frontend/UI:** Streamlit
* **Backend Logic:** Python (Pandas, datetime)
* **Storage:** CSV (lightweight persistent storage)

---

### ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/ai-personal-productivity-assistant.git
cd ai-personal-productivity-assistant

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run productive_agent.py
```

---

### 📁 Project Structure

```
AI-Personal-Productivity-Assistant/
│
├── productive_agent.py     # Main Streamlit app
├── tasks.csv               # Persistent storage file for tasks
├── requirements.txt        # Dependencies
└── README.md               # Project description
```

