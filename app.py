import streamlit as st
from auth import login_user, add_user
from tasks import (
    create_task,
    get_all_members,
    get_tasks_for_member,
    get_all_tasks,
    mark_task_completed,
)

def run():
    st.set_page_config(page_title="Event Work System", layout="wide")
    st.title("Event Accounting & Work Allocation System")

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_ui()
    else:
        dashboard()

def login_ui():
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid login")

def dashboard():
    user = st.session_state.user
    st.success(f"Logged in as {user['name']} ({user['role']})")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

    if user["role"] == "head":
        head_dashboard(user)
    else:
        member_dashboard(user)

def head_dashboard(user):
    st.subheader("Assign Task")

    members = get_all_members()
    member_map = {m[1]: m[0] for m in members}

    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    member_name = st.selectbox("Assign to", list(member_map.keys()))
    due_date = st.date_input("Due Date")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    if st.button("Assign Task"):
        create_task(
            title,
            description,
            member_map[member_name],
            user["id"],
            str(due_date),
            priority,
        )
        st.success("Task assigned successfully")

    st.subheader("All Tasks")
    tasks = get_all_tasks()
    st.table(tasks)

def member_dashboard(user):
    st.subheader("My Tasks")
    tasks = get_tasks_for_member(user["id"])

    for t in tasks:
        st.write(f"**{t[1]}** — {t[5]}")
        if t[5] != "Completed":
            if st.button(f"Mark Completed {t[0]}"):
                mark_task_completed(t[0])
                st.rerun()
