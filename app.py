import streamlit as st
import pandas as pd
from auth import login_user, add_user, init_db
from emailer import send_notice_email
from tasks import create_task, get_all_members, get_tasks_for_member, get_all_tasks, mark_task_completed


def run():
    st.set_page_config(page_title="Event Work System", layout="wide")
    st.title("📋 Event Accounting & Work Allocation System")

    init_db()

    # default users
    try:
        add_user("Admin Head", "head@test.com", "admin123", "head")
        add_user("Team Member", "member@test.com", "member123", "member")
    except:
        pass

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_ui()
    else:
        dashboard()


# ---------------- LOGIN ----------------

def login_ui():

    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = login_user(email, password)

        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid email or password")


# ---------------- DASHBOARD ----------------

def dashboard():

    user = st.session_state.user

    st.success(f"Logged in as {user['name']} ({user['role']})")

    col1, col2 = st.columns([8,2])

    with col2:
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

    if user["role"] == "head":
        head_dashboard(user)
    else:
        member_dashboard(user)


# ---------------- HEAD DASHBOARD ----------------

def head_dashboard(user):

    st.subheader("👤 Create New Member")

    new_name = st.text_input("Member Name")
    new_email = st.text_input("Member Email")
    new_password = st.text_input("Member Password", type="password")

    if st.button("Create Member"):

        if new_name and new_email and new_password:

            try:
                add_user(new_name, new_email, new_password, "member")
                st.success("Member created successfully")
                st.rerun()

            except:
                st.error("Member already exists")

        else:
            st.warning("Please fill all fields")

    st.divider()

    # ---------------- TASK ASSIGN ----------------

    st.subheader("➕ Assign New Task")

    members = get_all_members()

    if not members:
        st.warning("No members found")
        return

    # SAFE MEMBER MAP
    member_map = {}

    for m in members:

        member_id = m[0]
        member_name = m[1]

        if len(m) >= 3:
            member_email = m[2]
        else:
            member_email = ""

        member_map[member_name] = {
            "id": member_id,
            "email": member_email
        }

    title = st.text_input("Task Title")
    description = st.text_area("Task Description")

    member_name = st.selectbox("Assign to", list(member_map.keys()))

    due_date = st.date_input("Due Date")
    priority = st.selectbox("Priority", ["Low","Medium","High"])

    send_email = st.checkbox("Send Email Notification")

    if st.button("Assign Task"):

        if not title:
            st.warning("Task title required")
            return

        create_task(
            title,
            description,
            member_map[member_name]["id"],
            user["id"],
            str(due_date),
            priority
        )

        st.success("Task assigned successfully")

        # EMAIL
        if send_email:

            member_email = member_map[member_name]["email"]

            if member_email:

                message = f"""
New Task Assigned

Task: {title}
Description: {description}
Due Date: {due_date}
Priority: {priority}

Assigned by: {user['name']}
"""

                try:
                    send_notice_email(member_email, "New Task Assigned", message)
                    st.success("Email sent")

                except Exception as e:
                    st.error(f"Email failed: {e}")

            else:
                st.warning("Member email not found")

    st.divider()

    # ---------------- TASK STATUS ----------------

    st.subheader("📊 All Members Work Status")

    tasks = get_all_tasks()

    if tasks:

        df = pd.DataFrame(
            tasks,
            columns=[
                "Task ID",
                "Task",
                "Description",
                "Member",
                "Due Date",
                "Priority",
                "Status"
            ]
        )

        st.dataframe(df, use_container_width=True)

    else:
        st.info("No tasks assigned yet")


# ---------------- MEMBER DASHBOARD ----------------

def member_dashboard(user):

    st.subheader("📌 My Tasks")

    tasks = get_tasks_for_member(user["id"])

    if not tasks:
        st.info("No tasks assigned yet")
        return

    for t in tasks:

        st.markdown(f"### {t[1]}")
        st.write(t[2])

        st.write(
            f"Due: {t[3]} | Priority: {t[4]} | Status: {t[5]}"
        )

        if t[5] != "Completed":

            if st.button(f"Mark Completed (Task {t[0]})"):
                mark_task_completed(t[0])
                st.success("Task completed")
                st.rerun()

        st.divider()


if __name__ == "__main__":
    run()
