# n = int(input())
# lst = [int(input()) for i in range(n)]

n = 3
lst = [4, 3, 2]
count_five = 0
median = sum(lst) / len(lst)
if median < 4:
    while median < 4:
        lst.append(5)
        count_five += 1
        median = sum(lst) / len(lst)
    print(count_five)
    print(*lst)


else:
    print('все в порядке Федя!')
