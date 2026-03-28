import streamlit as st
import json
import os

# ARCH Technologies Branding
st.set_page_config(page_title="ARCH Tech To-Do List", page_icon="📝")

st.markdown("<h1 style='text-align: center;'>📝 ARCH TECHNOLOGIES</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>To-Do List Application</h3>", unsafe_allow_html=True)
st.markdown("---")

# File path for saving data [cite: 18]
DATA_FILE = "tasks_data.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

# Initialize tasks [cite: 18]
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- Sidebar: Add New Task [cite: 15, 20] ---
st.sidebar.header("Add New Task")
new_task = st.sidebar.text_input("Task Description")
category = st.sidebar.selectbox("Category", ["Work", "Personal", "Urgent", "Others"])

if st.sidebar.button("Add Task"):
    if new_task:
        task_obj = {
            "task": new_task,
            "category": category,
            "completed": False
        }
        st.session_state.tasks.append(task_obj)
        save_tasks(st.session_state.tasks)
        st.sidebar.success("Task Added!")
        st.rerun()

# --- Main Area: Filters [cite: 20] ---
st.write("### Your Tasks")
filter_cat = st.selectbox("Filter by Category", ["All", "Work", "Personal", "Urgent", "Others"])

# Filtering logic [cite: 17, 20]
filtered_tasks = st.session_state.tasks
if filter_cat != "All":
    filtered_tasks = [t for t in st.session_state.tasks if t['category'] == filter_cat]

# --- Display Tasks [cite: 15, 16] ---
for index, t in enumerate(filtered_tasks):
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    # Mark as completed 
    is_done = col1.checkbox("", value=t['completed'], key=f"check_{index}")
    if is_done != t['completed']:
        t['completed'] = is_done
        save_tasks(st.session_state.tasks)
        st.rerun()
    
    # Task text display
    display_text = f"~~{t['task']}~~" if t['completed'] else t['task']
    col2.write(f"**{display_text}** ({t['category']})")
    
    # Remove task [cite: 15]
    if col3.button("🗑️", key=f"del_{index}"):
        st.session_state.tasks.remove(t)
        save_tasks(st.session_state.tasks)
        st.rerun()

st.markdown("---")
if st.button("Clear All Completed Tasks"):
    st.session_state.tasks = [t for t in st.session_state.tasks if not t['completed']]
    save_tasks(st.session_state.tasks)
    st.rerun()