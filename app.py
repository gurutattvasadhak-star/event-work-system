import streamlit as st
from auth import login_user, add_user
from tasks import (
    create_task,
    get_all_members,
    get_tasks_for_member,
    get_all_tasks,
    get_member_email,
    mark_task_completed,
    get_head_email
)
from emailer import send_task_email

st.set_page_config(page_title="Event Work System", layout="centered")

st.title("📋 Event Accounting – Work Allocation System")

# ---------------- LOGIN ----------------
if "user" not in st.session_state:

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state["user"] = user
            st.success(f"Welcome {user['name']} ({user['role']})")
        else:
            st.error("Invalid email or password")

# ---------------- AFTER LOGIN ----------------
else:
    user = st.session_state["user"]
    st.success(f"Logged in as {user['name']} ({user['role']})")

    # ========== HEAD VIEW ==========
    if user["role"] == "head":
        st.subheader("➕ Assign New Work")

        members = get_all_members()
        member_dict = {name: uid for uid, name in members}

        title = st.text_input("Work Title")
        description = st.text_area("Work Description")
        member_name = st.selectbox("Assign To", list(member_dict.keys()))
        due_date = st.date_input("Due Date")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])

        if st.button("Assign Work"):
            if title and member_name:
                member_id = member_dict[member_name]

                # Create task
                create_task(
                    title,
                    description,
                    member_id,
                    user["id"],
                    str(due_date),
                    priority
                )

                # Member email
                email_to, member_name_real = get_member_email(member_id)

                email_body = f"""
Hello {member_name_real},

A new work has been assigned to you.

Work Title: {title}
Description: {description}
Due Date: {due_date}
Priority: {priority}

Please login to the Event Work System to update the status.

Regards,
Event Accounting Team
"""

                send_task_email(
                    to_email=email_to,
                    subject="New Work Assigned",
                    body=email_body
                )

                st.success("Work assigned and email sent successfully!")
            else:
                st.warning("Please fill required fields")

        st.divider()
        st.subheader("📊 All Assigned Work")

        tasks = get_all_tasks()
        for t in tasks:
            st.write(
                f"**{t[1]}** → {t[2]} | Due: {t[3]} | "
                f"{t[4]} | Status: {t[5]}"
            )

    # ========== MEMBER VIEW ==========
    else:
        st.subheader("🧑‍💻 My Assigned Work")

        tasks = get_tasks_for_member(user["id"])
        if tasks:
            for t in tasks:
                task_id, title, desc, due, priority, status = t

                st.write(
                    f"**{title}** | Due: {due} | "
                    f"{priority} | Status: {status}"
                )
                st.write(desc)

                if status != "Completed":
                    if st.button(f"Mark Completed – {task_id}"):
                        # Update status
                        mark_task_completed(task_id)

                        # Email to Head
                        head_email = get_head_email(user["head_id"])
                        send_task_email(
                            to_email=head_email,
                            subject="✅ Task Completed",
                            body=f"""
Hello,

The following task has been completed:

Task: {title}
Completed by: {user['name']}

Please login to the system for details.

Regards,
Event Work System
"""
                        )

                        st.success("Task completed and Head notified")
                        st.rerun()

                st.divider()
        else:
            st.info("No work assigned yet")

    # ---------------- LOGOUT ----------------
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
