# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

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

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
