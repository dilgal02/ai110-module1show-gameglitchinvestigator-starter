from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Bug fix: a guess of 60 against a secret of 50 used to show "Go HIGHER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Bug fix: a guess of 40 against a secret of 50 used to show "Go LOWER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

# Edge cases (Challenge 1)

def test_negative_number_is_too_low():
    ok, guess, err = parse_guess("-5")
    assert ok and guess == -5
    outcome, message = check_guess(guess, 50)
    assert outcome == "Too Low"

def test_decimal_guess_is_cut_to_whole_number():
    ok, guess, err = parse_guess("3.7")
    assert ok and guess == 3

def test_text_is_not_a_number():
    ok, guess, err = parse_guess("abc")
    assert not ok
    assert err == "That is not a number."

def test_empty_input_asks_for_a_guess():
    ok, guess, err = parse_guess("")
    assert not ok
    assert err == "Enter a guess."

def test_huge_number_is_too_high():
    outcome, message = check_guess(10**18, 50)
    assert outcome == "Too High"
