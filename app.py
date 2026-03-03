import streamlit as st
from auth import login_user, add_user
from tasks import (
    create_task,
    get_all_members,
    get_tasks_for_member,
    get_all_tasks,
    get_member_email
)
from emailer import send_task_email


def main():
    st.set_page_config(page_title="Event Work System", layout="centered")
    st.title("📋 Event Accounting – Work Allocation System")

    # ---------- LOGIN ----------
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

    # ---------- AFTER LOGIN ----------
    else:
        user = st.session_state["user"]
        st.success(f"Logged in as {user['name']} ({user['role']})")

        # ===== HEAD VIEW =====
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

                    create_task(
                        title,
                        description,
                        member_id,
                        user["id"],
                        str(due_date),
                        priority
                    )

                    email_to, member_real_name = get_member_email(member_id)

                    send_task_email(
                        to_email=email_to,
                        subject="New Work Assigned",
                        body=f"""
Hello {member_real_name},

New work has been assigned to you.

Title: {title}
Due Date: {due_date}
Priority: {priority}

Please login to update the status.

Regards,
Event Accounting Team
"""
                    )

                    st.success("Work assigned and email sent")
                else:
                    st.warning("Please fill all required fields")

            st.divider()
            st.subheader("📊 All Assigned Work")

            for t in get_all_tasks():
                st.write(
                    f"**{t[1]}** → {t[2]} | Due: {t[3]} | "
                    f"{t[4]} | Status: {t[5]}"
                )

        # ===== MEMBER VIEW =====
        else:
            st.subheader("🧑‍💻 My Assigned Work")

            tasks = get_tasks_for_member(user["id"])
            if tasks:
                for t in tasks:
                    st.write(f"**{t[1]}** | Due: {t[3]} | {t[4]} | Status: {t[5]}")
                    st.write(t[2])
                    st.divider()
            else:
                st.info("No work assigned yet")

        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
