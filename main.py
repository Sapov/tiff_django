def sol(num, k):
    s = ""
    for i in num:
        s += str(i)
    str_list = " ".join(str(int(s) + k)).split()
    l = list(map(int, str_list))
    print(l)


print(sol(num=[1, 2, 0, 0], k=34))
