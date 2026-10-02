import random
import streamlit as st
# FIX: Refactored the game logic from app.py into logic_utils.py
# with Claude Code.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    get_closeness,
    format_history_line,
    update_score,
)

# UI: each closeness level gets its own colored box.
HINT_BOX = {
    "🎯 Exact": st.success,
    "🔥 Hot": st.error,
    "🌡️ Warm": st.warning,
    "🧊 Cold": st.info,
}


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # FIX: The counter started at 1, so the game showed one attempt less than
    # allowed. I marked this line and asked Claude Code to fix the counter.
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "rounds" not in st.session_state:
    st.session_state.rounds = []

# FEATURE: Guess History in the sidebar. The box is a placeholder so it can
# be redrawn right after a new guess is added.
st.sidebar.header("Guess History")
history_box = st.sidebar.empty()


def show_history():
    """List every valid guess of this game in the sidebar, newest first."""
    rounds = st.session_state.rounds
    if not rounds:
        history_box.caption("No guesses yet.")
        return
    lines = [
        format_history_line(r["Attempt"], r["Guess"], r["Hint"],
                            r["Closeness"])
        for r in reversed(rounds)
    ]
    history_box.markdown("\n".join(f"- {line}" for line in lines))


show_history()

st.subheader("Make a guess")

# FIX: This box is drawn before the guess is counted, so "Attempts left"
# was one guess behind. Claude Code made it a placeholder that is redrawn
# after each guess.
attempts_box = st.empty()


def show_attempts_left():
    attempts_box.info(
        f"Guess a number between 1 and 100. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )


show_attempts_left()


def show_summary():
    """Show a table of every valid guess in this game."""
    if st.session_state.rounds:
        st.subheader("Game summary")
        st.dataframe(st.session_state.rounds, hide_index=True)


with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.session_state.rounds = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    show_summary()
    st.stop()

if submit:
    st.session_state.attempts += 1
    show_attempts_left()

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: The secret was turned into a string on every even attempt,
        # so the hints changed between attempts. I asked Claude Code to
        # always pass a number.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        closeness = get_closeness(guess_int, st.session_state.secret)
        st.session_state.rounds.append({
            "Attempt": st.session_state.attempts,
            "Guess": guess_int,
            "Hint": message,
            "Closeness": closeness,
        })
        show_history()

        if show_hint:
            HINT_BOX[closeness](f"{message}  {closeness}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

        if st.session_state.status != "playing":
            show_summary()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
