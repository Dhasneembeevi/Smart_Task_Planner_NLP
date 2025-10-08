import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="AI Productivity Agent", layout="wide")
st.title("🤖 Smart Task Manager")

# -----------------------
# Initialize session state
# -----------------------
if "tasks" not in st.session_state:
    try:
        tasks = pd.read_csv("tasks.csv")
        tasks["Deadline"] = pd.to_datetime(tasks["Deadline"], errors="coerce")
    except FileNotFoundError:
        tasks = pd.DataFrame(columns=["Task Name", "Priority", "Deadline", "Done"])
    st.session_state.tasks = tasks.copy()

tasks = st.session_state.tasks

# -----------------------
# Add New Task
# -----------------------
st.sidebar.header("Add New Task")
task_name = st.sidebar.text_input("Task Name")
priority = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"])
deadline = st.sidebar.date_input("Deadline")
deadline_dt = pd.to_datetime(deadline)

if st.sidebar.button("Add Task"):
    if task_name.strip() != "":
        new_task = pd.DataFrame(
            [[task_name, priority, deadline_dt, "No"]],
            columns=["Task Name", "Priority", "Deadline", "Done"],
        )
        st.session_state.tasks = pd.concat([tasks, new_task], ignore_index=True)
        st.session_state.tasks.to_csv("tasks.csv", index=False)
        st.sidebar.success(f"Task '{task_name}' added successfully!")

# -----------------------
# Mark Tasks as Done
# -----------------------
st.sidebar.subheader("Mark Tasks Done")
if not tasks.empty:
    for index, row in tasks.iterrows():
        deadline_str = (
            row["Deadline"].strftime("%Y-%m-%d") if pd.notna(row["Deadline"]) else "-"
        )
        if st.sidebar.checkbox(
            f"{row['Task Name']} ({row['Priority']}, {deadline_str})",
            value=(row["Done"] == "Yes"),
            key=f"done_{index}",
        ):
            st.session_state.tasks.at[index, "Done"] = "Yes"
        else:
            st.session_state.tasks.at[index, "Done"] = "No"

    st.session_state.tasks.to_csv("tasks.csv", index=False)


# -----------------------
# Helper: Get Top 3 Tasks
# -----------------------
@st.cache_data
def get_top_tasks(tasks_df):
    if tasks_df.empty:
        return pd.DataFrame()

    pending_tasks = tasks_df[tasks_df["Done"] == "No"].copy()
    if pending_tasks.empty:
        return pd.DataFrame()

    # Map priorities to numbers
    priority_map = {"High": 1, "Medium": 2, "Low": 3}
    pending_tasks["PriorityNum"] = (
        pending_tasks["Priority"].map(priority_map).astype(int)
    )
    pending_tasks["Deadline"] = pd.to_datetime(
        pending_tasks["Deadline"], errors="coerce"
    )

    # Sort by PriorityNum then Deadline
    pending_tasks = pending_tasks.sort_values(
        by=["PriorityNum", "Deadline"], ascending=[True, True], ignore_index=True
    )

    return pending_tasks.head(3)


top3_tasks = get_top_tasks(st.session_state.tasks)

# -----------------------
# Agentic Suggestion
# -----------------------
st.subheader("💡 Today's Suggestion")
if not top3_tasks.empty:
    top_task = top3_tasks.iloc[0]
    st.info(
        f"🤖 Start with **{top_task['Task Name']}** "
        f"(Priority: {top_task['Priority']}, Deadline: {top_task['Deadline'].date() if pd.notna(top_task['Deadline']) else '-'})"
    )

# -----------------------
# Top 3 Tasks Display
# -----------------------
st.subheader("Top 3 Tasks Today")
if not top3_tasks.empty:
    for _, row in top3_tasks.iterrows():
        color = (
            "#ff4d4d"
            if row["Priority"] == "High"
            else "#ffd633" if row["Priority"] == "Medium" else "#66ff66"
        )
        st.markdown(
            f"<div style='background-color:{color}; color:black; padding:10px; border-radius:5px;'>"
            f"<b>{row['Task Name']}</b> — {row['Priority']} — {row['Deadline'].date() if pd.notna(row['Deadline']) else '-'}"
            f"</div>",
            unsafe_allow_html=True,
        )
else:
    st.info("No pending tasks!")

# -----------------------
# Visual Task Overview
# -----------------------
st.subheader("📊 Task Completion Overview")
if not tasks.empty:
    fig = px.bar(
        tasks,
        x="Priority",
        color="Done",
        barmode="stack",
        title="Tasks by Priority and Completion",
        color_discrete_map={"No": "red", "Yes": "green"},
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# All Tasks Table with Delete Confirmation
# -----------------------
st.subheader("📋 All Tasks")
if not tasks.empty:

    def color_priority(row):
        if row["Priority"] == "High":
            return ["background-color: #ff4d4d; color: black"] * len(row)
        elif row["Priority"] == "Medium":
            return ["background-color: #ffd633; color: black"] * len(row)
        else:
            return ["background-color: #66ff66; color: black"] * len(row)

    remove_indices = []

    # Track delete confirmation
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = None

    for i, row in tasks.iterrows():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.write(f"**{row['Task Name']}**")
        with col2:
            st.write(row["Priority"])
        with col3:
            st.write(row["Deadline"].date() if pd.notna(row["Deadline"]) else "-")
        with col4:
            if st.button("🗑️ Delete", key=f"delete_{i}"):
                st.session_state.confirm_delete = i

    # Show confirmation if delete clicked
    if st.session_state.confirm_delete is not None:
        idx = st.session_state.confirm_delete
        st.warning(
            f"⚠️ Are you sure you want to delete '{tasks.iloc[idx]['Task Name']}'?"
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Yes, Delete"):
                st.session_state.tasks.drop(idx, inplace=True)
                st.session_state.tasks.reset_index(drop=True, inplace=True)
                st.session_state.tasks.to_csv("tasks.csv", index=False)
                st.success("🗑️ Task deleted successfully!")
                st.session_state.confirm_delete = None

        with c2:
            if st.button("❌ Cancel"):
                st.session_state.confirm_delete = None
                st.info("Deletion cancelled.")

    st.dataframe(
        st.session_state.tasks.style.apply(color_priority, axis=1),
        use_container_width=True,
    )
else:
    st.info("No tasks available. Add one from the sidebar ➕")
