import streamlit as st
import requests

st.set_page_config(page_title="Onboarding Buddy", page_icon="🤖")

st.title("Onboarding Buddy")
st.caption("AI assistant for company policies")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Employee Info")

    role = st.selectbox(
        "Role",
        ["intern", "full_time", "manager", "mentor"]
    )

    # Fetch list from backend
    try:
        r = requests.get(
            "http://localhost:8000/list_by_role",
            params={"role": role},
            timeout=10
        )
        r.raise_for_status()
        items = r.json().get("items", [])
    except Exception as e:
        st.error(f"Failed to load users: {e}")
        items = []

    if not items:
        st.warning("No users found for this role")
        user_id = ""
    else:
        selected = st.selectbox(
            "Select Person",
            items,
            format_func=lambda x: f"{x['id']} - {x['name']}"
        )
        user_id = selected["id"]

    show_debug = st.checkbox("Show retrieved context (debug)")

# -----------------------------
# Main area
# -----------------------------
st.divider()

question = st.text_area("Ask your question")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not user_id:
        st.warning("Please select a user.")
    else:
        with st.spinner("Thinking..."):
            try:
                r = requests.post(
                    "http://localhost:8000/chat",
                    json={
                        "user_id": user_id,
                        "question": question,
                        "debug": show_debug
                    },
                    timeout=120
                )

                if r.status_code != 200:
                    st.error(r.text)
                else:
                    data = r.json()

                    st.subheader("Answer")
                    st.write(data.get("answer", "No answer returned."))

                    if show_debug:
                        st.subheader("Context")
                        for c in data.get("context", []):
                            st.code(c)

            except Exception as e:
                st.error(f"Request failed: {e}")
