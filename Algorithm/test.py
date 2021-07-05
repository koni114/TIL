def solution(v):
    from collections import defaultdict
    dict_x = defaultdict(int)
    dict_y = defaultdict(int)

    for x, y in v:
        dict_x[x] += 1
        dict_y[y] += 1

    x_items = sorted(dict_x.items(), key=lambda x:x[1])
    y_items = sorted(dict_y.items(), key=lambda x:x[1])
    answer = [x_items[0][0], y_items[0][0]]
    return answer

solution([[1, 4], [3, 4], [3, 10]])
solution([[1, 1], [2, 2], [1, 2]])