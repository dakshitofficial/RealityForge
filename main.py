
import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

st.set_page_config(
    page_title="RealityForge",
    page_icon="🌌",
    layout="centered"
)

st.title("🌌 RealityForge")
st.caption("Your imagination. An AI-generated reality.")

if "history" not in st.session_state:
    st.session_state.history = []

if "world_started" not in st.session_state:
    st.session_state.world_started = False

def ask_ai(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )
    response.raise_for_status()
    return response.json()["response"]

if not st.session_state.world_started:
    st.subheader("Create your reality")

    idea = st.text_area(
        "Describe the world you want to explore",
        placeholder="A city where memories can be traded...",
        height=120
    )

    genre = st.selectbox(
        "Choose a genre",
        ["Fantasy", "Sci-Fi", "Mystery", "Horror", "Adventure"]
    )

    if st.button("✨ Generate My World", type="primary"):
        if not idea.strip():
            st.warning("First, describe your world.")
        else:
            with st.spinner("AI is creating your world..."):
                prompt = f"""
                You are the creative engine of RealityForge, an interactive
                story-generation AI.

                Genre: {genre}
                User's idea: {idea}

                Create an original world based on the user's idea.
                Do not use a fixed template.
                Include:
                1. A unique world name and atmosphere.
                2. Important world rules and a central mystery.
                3. A main character and an immediate problem.
                4. An engaging opening scene.
                5. Exactly three distinct choices for what happens next.

                Make the story immersive but easy to understand.
                End with a section titled CHOICES and number the three options.
                """
                try:
                    result = ask_ai(prompt)
                    st.session_state.history = [
                        {"role": "assistant", "content": result}
                    ]
                    st.session_state.world_started = True
                    st.rerun()
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Ollama is not running. Open a terminal and run "
                        "'ollama run qwen2.5:3b'."
                    )
                except Exception as e:
                    st.error(f"AI request failed: {e}")

else:
    for item in st.session_state.history:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    choice = st.text_input(
        "What happens next?",
        placeholder="Enter a choice or invent your own action..."
    )

    if st.button("Continue the story", type="primary"):
        if choice.strip():
            with st.spinner("Reality is changing..."):
                previous_story = "\n\n".join(
                    f"{item['role']}: {item['content']}"
                    for item in st.session_state.history
                )

                prompt = f"""
                You are RealityForge, an interactive generative storytelling AI.

                Continue this existing story without restarting it.
                Maintain continuity with the previous events and characters.

                STORY SO FAR:
                {previous_story}

                PLAYER'S ACTION:
                {choice}

                Show the consequences of the player's action and advance
                the story meaningfully. Keep the scene engaging.
                End with exactly three numbered choices for the next action.
                The player may also enter their own action.
                """

                try:
                    result = ask_ai(prompt)
                    st.session_state.history.append(
                        {"role": "user", "content": choice}
                    )
                    st.session_state.history.append(
                        {"role": "assistant", "content": result}
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not continue the story: {e}")

    if st.button("🌌 Create a New Reality"):
        st.session_state.history = []
        st.session_state.world_started = False
        st.rerun()
