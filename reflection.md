# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game opened fine and looked normal, but I could not win by following the hints. I used the Developer Debug Info panel to see the secret number and noticed the hints were wrong. The attempts counter and the New Game button were also broken.

- The hints were backwards. When my guess was higher than the secret, the game told me to go higher.
- The game showed "Attempts left: 7" before I made any guess, even though the sidebar said 8 attempts were allowed.
- After I won, the New Game button did not start a new game. It kept saying I already won.

**Bug Reproduction Log**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|------------|-------------------|-----------------|------------------------|-------------------------|
| Secret 50, guess 60 | "Go LOWER!" hint | "Go HIGHER!" hint shown | none | `app.py`, `check_guess`: the "Too High" branch returned "Go HIGHER!" (messages swapped); also the secret was turned into a string on every even attempt |
| Page just loaded, no guess yet (Normal) | "Attempts left: 8" | "Attempts left: 7" | none | `app.py`, `st.session_state.attempts = 1`: the counter started at 1 instead of 0 |
| Win the game, then click New Game | New game starts | "You already won. Start a new game to play again." | none | `app.py`, `if new_game:` block: resets `attempts` and `secret` but not `status`, so the game stays "won" |



## 2. How did you use AI as a teammate?

- **Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?**
- I used ClaudeCode
- **Correct suggestion**
  - What the AI suggested: Claude said the two hint messages in `check_guess` were swapped, and that `app.py` turned the secret into a string on every even attempt, so the hints changed from one attempt to the next.
  - Why it was correct: with secret 50 and guess 60 the old code showed "Go HIGHER!", which matched what I saw in the game. After the fix it shows "Go LOWER!".
  - How I verified it: I ran `python -m pytest` (5 passed) and played the game with the Developer Debug Info panel open.
- **Suggestion I did not accept as written**
  - What the AI suggested: The starter tests failed because `check_guess` returns the outcome and the message together. Claude suggested changing `check_guess` to return only the outcome and adding a new function for the hint text.
  - Why I changed it: that meant changing `logic_utils.py` and `app.py` again. I chose the simpler way: keep `check_guess` as it is and update the three starter tests to unpack the result.
  - How I verified my version: I ran `python -m pytest` and all 5 tests passed.


---

## 3. Debugging and testing your fixes

- **How did you decide whether a bug was really fixed?**
  - I counted a bug as fixed only when two things were true: `python -m pytest` passed, and the game showed the right behavior when I played it with the Developer Debug Info panel open.
- **Describe at least one test you ran and what it showed you about your code.**
  - `test_too_high_hint_says_go_lower` checks that a guess of 60 against a secret of 50 returns "Too High" and a hint with "LOWER". With the old code this test fails, because the hint said "Go HIGHER!". Now all 5 tests pass.
  - I also tested the attempts counter by hand: a fresh page shows "Attempts left: 8", and after one guess it shows 7.
- **Did AI help you design or understand any tests? How?**
  - Yes. Claude wrote the two new hint tests. It also explained why the starter tests failed at first: `check_guess` returns the outcome and the message together, and the tests compared that pair to one word. Plain `pytest` gave `ModuleNotFoundError`, and Claude explained that I need to run `python -m pytest` so Python can find `logic_utils.py`.

---

## 4. What did you learn about Streamlit and state?

- **How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?**
  - Every time you click a button or type in a box, Streamlit runs the whole `app.py` again from top to bottom. Normal variables start over on every rerun, so the game would forget the secret number and the attempts. `st.session_state` is a dictionary that survives reruns, so the secret, attempts, score and guesses are kept there. The rerun order also caused one of my bugs: the "Attempts left" box was drawn before the guess was counted, so it was one guess behind until it was redrawn after each guess.


---

## 5. Looking ahead: your developer habits

- **What is one habit or strategy from this project that you want to reuse?**
  - Fix one bug at a time: mark it with a `# FIXME` comment, select only those lines for the AI, then run pytest and commit before moving on.
- **What is one thing you would do differently next time you work with AI on a coding task?**
  - Give small, specific prompts from the start. At first the AI changed several files at once and did more than I asked, and I had to undo it.
- **How did this project change the way you think about AI generated code?**
  - AI code can look finished and still have bugs like swapped hints, and AI explanations can be wrong too: one of Gemini's claims about this bug was false. Now I check AI code with tests and by running it myself.

