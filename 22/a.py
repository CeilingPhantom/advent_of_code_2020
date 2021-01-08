def a(lines):
    player1 = []
    player2 = []
    i = 1
    while lines[i]:
        player1.append(int(lines[i]))
        i += 1
    i += 2
    while i < len(lines):
        player2.append(int(lines[i]))
        i += 1
    while player1 and player2:
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        # assuming no two numbers are equal
        if card1 > card2:
            player1.append(card1)
            player1.append(card2)
        elif card2 > card1:
            player2.append(card2)
            player2.append(card1)
    player = player1 or player2
    s = 0
    for i, num in enumerate(player):
        s += num * (len(player) - i)
    return s

def b(lines):
    player1 = []
    player2 = []
    i = 1
    while lines[i]:
        player1.append(int(lines[i]))
        i += 1
    i += 2
    while i < len(lines):
        player2.append(int(lines[i]))
        i += 1
    r = play_game(player1, player2)
    player = r[0] or r[1]
    s = 0
    for i, num in enumerate(player):
        s += num * (len(player) - i)
    return s

sub_game_results = {}

def play_game(player1, player2):
    sub_game_key = (tuple(player1), tuple(player2))
    if sub_game_key in sub_game_results:
        return sub_game_results[sub_game_key]
    round_configs = set()
    while player1 and player2:
        # assuming root game doesn't get infinite rounds
        round_config = (tuple(player1), tuple(player2))
        if round_config in round_configs:
            player2 = []
            break
        round_configs.add(round_config)
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        if len(player1) >= card1 and len(player2) >= card2:
            r = play_game(player1[:card1], player2[:card2])
            if r[0]:
                player1.append(card1)
                player1.append(card2)
            else:
                player2.append(card2)
                player2.append(card1)
        elif card1 > card2:
            player1.append(card1)
            player1.append(card2)
        elif card2 > card1:
            player2.append(card2)
            player2.append(card1)
    sub_game_results[sub_game_key] = (player1, player2)
    return sub_game_results[sub_game_key]

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))
