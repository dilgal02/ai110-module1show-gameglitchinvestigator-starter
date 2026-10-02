def get_range_for_difficulty(difficulty: str):
    """Return the inclusive number range for a difficulty level.

    Args:
        difficulty: "Easy", "Normal" or "Hard".

    Returns:
        A tuple (low, high). An unknown difficulty falls back to (1, 100).
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Convert the player's raw input into a whole-number guess.

    Decimal input such as "3.7" is cut down to a whole number (3).

    Args:
        raw: The text typed into the guess box, or None.

    Returns:
        A tuple (ok, guess, error). ok is True when the input is a number,
        guess is the int value (None if ok is False), and error is a
        message for the player (None if ok is True).
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess with the secret number.

    Args:
        guess: The player's guess.
        secret: The secret number.

    Returns:
        A tuple (outcome, message). outcome is "Win", "Too High" or
        "Too Low", and message is the hint shown to the player.
    """
    # FIX: The two hint messages were swapped. I selected the lines and asked
    # Claude Code for a targeted fix, then checked it with pytest.
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def get_closeness(guess, secret):
    """Describe how close a guess is to the secret number.

    Args:
        guess: The player's guess.
        secret: The secret number.

    Returns:
        "🎯 Exact" for a correct guess, "🔥 Hot" when the guess is at most
        5 away, "🌡️ Warm" when it is at most 15 away, and "🧊 Cold"
        otherwise.
    """
    distance = abs(guess - secret)
    if distance == 0:
        return "🎯 Exact"
    if distance <= 5:
        return "🔥 Hot"
    if distance <= 15:
        return "🌡️ Warm"
    return "🧊 Cold"


def format_history_line(attempt, guess, hint, closeness):
    """Build one line of the Guess History shown in the sidebar.

    Args:
        attempt: The attempt number of the guess.
        guess: The number the player guessed.
        hint: The hint message shown for the guess.
        closeness: The closeness label from get_closeness().

    Returns:
        A string such as "#3: 60 — 📈 Go HIGHER! (🔥 Hot)".
    """
    return f"#{attempt}: {guess} — {hint} ({closeness})"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Return the new score after a guess.

    A win adds 100 - 10 * (attempt_number + 1) points, but at least 10.
    A wrong guess usually costs 5 points, except that a "Too High" guess
    on an even attempt adds 5 points.

    Args:
        current_score: The score before this guess.
        outcome: "Win", "Too High" or "Too Low".
        attempt_number: Which attempt this guess was, starting at 1.

    Returns:
        The updated score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
