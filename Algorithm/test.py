test = [[i for i in range(10)] for j in range(10)]
for i in range(len(test)):
    for j in range(len(test[0])):
        x = x + test[i][j]
        x = x + test[j][i]