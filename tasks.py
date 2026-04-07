def easy_task(state):
    # survive without breach for few steps
    return 1.0 if state["attack_level"] < 0.5 else 0.5


def medium_task(state):
    # maintain low load and high encryption
    score = 0

    if state["encryption_level"] >= 3:
        score += 0.5

    if state["server_load"] < 80:
        score += 0.5

    return score


def hard_task(state):
    # no breach + balanced system
    score = 0

    if state["attack_level"] < 0.4:
        score += 0.3

    if state["server_load"] < 70:
        score += 0.3

    if state["encryption_level"] >= 4:
        score += 0.4

    return score
