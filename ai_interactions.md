# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

```
Add a Guess History feature in the sidebar: after every guess, list all guesses of the current game with their hint and closeness, newest at the top. Put the formatting logic in a new function in logic_utils.py, add a pytest test for it, and make sure flake8 and all tests still pass.
```

**What did the agent do?**

- `logic_utils.py`: added `format_history_line()`, which builds one history line like `#3: 60 — 📈 Go HIGHER! (🔥 Hot)`.
- `app.py`: added a "Guess History" header and a placeholder in the sidebar, and a `show_history()` function. It runs when the page loads and again right after each guess. The agent used a placeholder because the sidebar is drawn before the guess is counted, so without it the list would be one guess behind (the same problem as the attempts counter).
- `tests/test_game_logic.py`: added `test_history_line_shows_attempt_guess_hint_and_closeness`.
- Ran `python -m flake8` (no warnings) and `python -m pytest` (11 passed), and played a scripted game with Streamlit's testing tool to check the sidebar after every guess.

**What did you have to verify or fix manually?**

I did not have to fix any code. I reviewed the diff and played a game to check that the history updates after each guess and that New Game clears it. I noticed that the attempt numbers skip a number after invalid input (for example #2 is missing after typing "abc"), because invalid input still uses up an attempt. I left that as it is, because it is how the attempts counter already works.


---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number (`"-5"`) | "Generate pytest edge-case tests in tests/test_game_logic.py for parse_guess and check_guess: a negative number, a decimal, non-numeric text, empty input, and a very large number." | `test_negative_number_is_too_low` | Yes | A player can type a minus sign by mistake. The game should not crash and should say the guess is too low. |
| Decimal (`"3.7"`) | same prompt | `test_decimal_guess_is_cut_to_whole_number` | Yes | The secret is a whole number, so a decimal guess must become one. The test shows `parse_guess` cuts 3.7 down to 3. |
| Non-numeric text (`"abc"`) | same prompt | `test_text_is_not_a_number` | Yes | Typing letters is the most common wrong input. The game should show an error instead of crashing. |
| Empty input (`""`) | same prompt | `test_empty_input_asks_for_a_guess` | Yes | Clicking Submit with an empty box should ask for a guess, not count as a number. |
| Very large number (`10**18`) | same prompt | `test_huge_number_is_too_high` | Yes | Checks that a number far outside the range does not break the comparison and is still "Too High". |

---

## Linting & Style (SF9)

**Prompt used:**

```
Add professional docstrings to every function in logic_utils.py and fix all flake8 warnings in logic_utils.py, app.py and tests/test_game_logic.py. Do not change how the game works.
```

**Linting output before** (`python -m flake8 logic_utils.py app.py tests/`):

```
app.py:3:80: E501 line too long (82 > 79 characters)
app.py:4:80: E501 line too long (88 > 79 characters)
app.py:51:80: E501 line too long (80 > 79 characters)
app.py:52:80: E501 line too long (83 > 79 characters)
app.py:55:1: E302 expected 2 blank lines, found 1
app.py:61:1: E305 expected 2 blank lines after class or function definition, found 1
app.py:108:80: E501 line too long (80 > 79 characters)
app.py:109:80: E501 line too long (86 > 79 characters)
logic_utils.py:48:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:3:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:8:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:13:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:18:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:24:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:32:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:38:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:42:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:47:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:52:1: E302 expected 2 blank lines, found 1
```

**Linting output after:** flake8 printed nothing (0 warnings). `python -m pytest` still shows 10 passed.

**Changes applied:**

- Added docstrings (summary, Args, Returns) to all four functions in `logic_utils.py`.
- E302 / E305: added a second blank line between functions in `logic_utils.py` and the tests, and around `show_attempts_left` in `app.py`.
- E501: split the long `# FIX:` comments into shorter lines and wrapped the `from logic_utils import ...` line into a multi-line import.
- No names were changed and the game logic stayed the same. I checked this with pytest and by playing a game.

**Suggested but not applied:**

- Claude pointed out that the `except TypeError` branch in `check_guess` can no longer run, because `app.py` now always passes the secret as a number. I left it in, because my prompt said not to change how the game works.


---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

Both models got the same prompt: the original buggy `check_guess` function and the app code that turned the secret into a string on every even attempt, with the question "Explain what causes the bug and show how you would fix it."

| | Model A | Model B |
|-|---------|---------|
| **Model name** | ChatGPT (sol 5.6) | Gemini 3.6 flash|
| **Response summary** | Converts both `guess` and `secret` to `int` at the start of `check_guess`, swaps the two hint messages, removes the `try/except TypeError` block, and calls `check_guess` with `st.session_state.secret` directly. Short answer, mostly code. | Names three causes: swapped hint text, string comparison on even attempts (`"9" > "42"` is True as text), and a claim that the win check gets skipped. The fix converts both values to `int` inside a `try/except` that returns a new `"Error"` outcome, swaps the hints, and removes the `str()` toggle in the caller. |
| **More Pythonic?** | Yes. It is short and simple, with no extra error handling the app does not need. | Less. The new `"Error"` outcome is not handled anywhere else in the app, and `parse_guess` already rejects bad input, so the extra `try/except` is not needed. |
| **Clearer explanation?** | No. It mostly shows code and explains the fix in one sentence. | Yes. It goes step by step and gives a concrete example (`"9" > "42"`). But one point is wrong: with the original code a correct guess still wins, because the `except` block compares `str(guess) == secret`. I checked it: `check_guess(50, "50")` returns `"Win"`. |

**Which did you prefer and why?**

For the fix I preferred ChatGPT, because it is simpler and fits this codebase. Gemini's version adds an `"Error"` outcome that the rest of the game does not know about. For understanding the bug Gemini was easier to follow, but one of its three claims was wrong, and I only noticed after running the original function. Both models agreed on the real causes, swapped hints and the secret becoming a string, which matches the fix I applied: swap the messages and always pass the secret as a number.

