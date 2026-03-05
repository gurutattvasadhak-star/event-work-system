import streamlit as st
from auth import login_user, add_user, init_db
from emailer import send_notice_email
from tasks import (
    create_task,
    get_all_members,
    get_tasks_for_member,
    get_all_tasks,
    mark_task_completed,
)

# ---------------- MAIN APP ----------------
def run():
    st.set_page_config(page_title="Event Work System", layout="wide")
    st.title("📋 Event Accounting & Work Allocation System")

    # Initialize database (important for cloud)
    init_db()

    # Create default users safely
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


# ---------------- LOGIN UI ----------------
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

    # ---------- CREATE MEMBER ----------
    st.subheader("👤 Create New Member")

    new_name = st.text_input("Member Name")
    new_email = st.text_input("Member Email")
    new_password = st.text_input("Member Password", type="password")

    if st.button("Create Member"):
        if new_name and new_email and new_password:
            try:
                add_user(new_name, new_email, new_password, "member")
                st.success("✅ Member created successfully")
            except:
                st.error("Member already exists or error occurred")
        else:
            st.warning("Please fill all fields")

    st.divider()

    # ---------- ASSIGN TASK ----------
    st.subheader("➕ Assign New Task")

    members = get_all_members()

    if not members:
        st.warning("No members found")
        return

    member_map = {m[1]: m[0] for m in members}

    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    member_name = st.selectbox("Assign to", list(member_map.keys()))
    due_date = st.date_input("Due Date")
    priority = st.selectbox("Priority", ["Low","Medium","High"])

    send_email = st.checkbox("Send Email Notification")
    member_email = st.text_input("Member Email (for notification)")

    if st.button("Assign Task"):

        if not title:
            st.warning("Task title is required")
            return

        create_task(
            title,
            description,
            member_map[member_name],
            user["id"],
            str(due_date),
            priority
        )

        st.success("✅ Task assigned successfully")

        # ---------- EMAIL NOTIFICATION ----------
        if send_email:

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
                    result = send_notice_email(
                        member_email,
                        "New Task Assigned",
                        message
                    )

                    st.success("📧 Email notification sent")

                except Exception as e:
                    st.error(f"Email sending failed: {e}")

            else:
                st.warning("⚠ Email notification selected but no email entered")

    st.divider()

    # ---------- ALL TASKS ----------
    st.subheader("📊 All Tasks")

    tasks = get_all_tasks()

    if tasks:
        st.table(tasks)
    else:
        st.info("No tasks assigned yet")


# ---------------- MEMBER DASHBOARD ----------------
def member_dashboard(user):

    st.subheader("🧑‍💻 My Tasks")

    tasks = get_tasks_for_member(user["id"])

    if not tasks:
        st.info("No tasks assigned yet")
        return

    for t in tasks:

        st.markdown(f"### {t[1]}")
        st.write(t[2])
        st.write(f"📅 Due: {t[3]} | ⚡ Priority: {t[4]} | 📌 Status: {t[5]}")

        if t[5] != "Completed":
            if st.button(f"Mark Completed (Task {t[0]})"):
                mark_task_completed(t[0])
                st.success("Task marked as completed")
                st.rerun()

        st.divider()


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    run()
