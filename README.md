# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**
  It is a number guessing game built with Streamlit. The game picks a secret number, and the player tries to guess it in a limited number of attempts. After each guess the game gives a hint to go higher or lower.
- [x] **Detail which bugs you found.**
  - The hints were backwards: a guess above the secret showed "Go HIGHER!". On every second attempt the secret was also turned into a string, so the numbers were compared as text and the hints changed between attempts.
  - The attempts counter started at 1, so the game showed "Attempts left: 7" before any guess on Normal (8 attempts allowed).
  - After a win, the New Game button did not start a new game. It kept saying "You already won."
- [x] **Explain what fixes you applied.**
  - Moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` from `app.py` into `logic_utils.py`.
  - Swapped the two hint messages in `check_guess`, and made `app.py` always pass the secret as a number.
  - Started the attempts counter at 0 and made "Attempts left" update right after each guess.
  - Updated the starter tests and added two new tests for the hint bug (5 tests pass).
  - The New Game bug is not fixed yet. The task asked to fix two bugs first.


## 📸 Demo Walkthrough

A sample game on Normal difficulty (range 1 to 100, 8 attempts):

1. Start the game with `python -m streamlit run app.py`. The game shows "Attempts left: 8".
2. Open "Developer Debug Info" to see the secret number. In this game it is 63.
3. User enters a guess of 40 and clicks Submit. The game shows "Go HIGHER!" (outcome "Too Low"). Attempts left: 7, score: -5.
4. User enters a guess of 70. The game shows "Go LOWER!" (outcome "Too High"). Attempts left: 6, score: 0.
5. User enters a guess of 60. The game shows "Go HIGHER!". Attempts left: 5, score: -5.
6. User enters a guess of 63. The game shows "Correct!", balloons appear, and the message says "You won! The secret was 63. Final score: 45".
7. The game is over. Any new guess shows "You already won. Start a new game to play again."

## 🧪 Test Results

```
tests/test_game_logic.py::test_winning_guess PASSED                  [ 10%]
tests/test_game_logic.py::test_guess_too_high PASSED                 [ 20%]
tests/test_game_logic.py::test_guess_too_low PASSED                  [ 30%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED    [ 40%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED    [ 50%]
tests/test_game_logic.py::test_negative_number_is_too_low PASSED     [ 60%]
tests/test_game_logic.py::test_decimal_guess_is_cut_to_whole_number PASSED [ 70%]
tests/test_game_logic.py::test_text_is_not_a_number PASSED           [ 80%]
tests/test_game_logic.py::test_empty_input_asks_for_a_guess PASSED   [ 90%]
tests/test_game_logic.py::test_huge_number_is_too_high PASSED        [100%]

============================ 10 passed in 0.02s ============================
```

## 🚀 Stretch Features

- [x] Advanced Edge-Case Testing: 5 edge-case tests in `tests/test_game_logic.py` (negative number, decimal, text, empty input, huge number). All tests pass, see Test Results above.

