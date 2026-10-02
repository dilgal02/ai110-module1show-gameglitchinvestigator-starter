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

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

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
