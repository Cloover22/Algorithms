players = ["mumu", "soe", "poe", "kai", "mine"]
callings = ["kai", "kai", "mine", "mine"]
result = ["mumu", "kai", "mine", "soe", "poe"]

# 시간초과
def solution(players, callings):
    answer = []

    idx = 0
    for call in callings:
        for play in players:
            if call == play:
                players[idx] = players[idx - 1]
                players[idx-1] = play
            idx += 1
        idx = 0

    answer = players
    return print(answer)

solution(players, callings)


# 딕셔너리 이용
def solution(players, callings):
    answer = []

    dict = {key : value for value, key in enumerate(players)}
    for call in callings:
        idx = dict[call]
        dict[call] -=1
        dict[players[idx-1]] += 1
        players[idx-1], players[idx] = players[idx], players[idx-1]

    print(sorted(dict.items(), key = lambda x: x[1]))   # value 값 정렬하여 출력 가능

    return players

solution(players, callings)