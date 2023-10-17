# def twosum(lst: list, target: int) -> list[int]:
#     n = len(lst)
#
#     for i in range(n):
#         for j in range(i + 1, n):
#             if lst[i] + lst[j] == target:
#                 return [i, j]
#
#
# print(twosum([2, 3, 4], 6))
#

# def twosum(lst: list, target: int) -> list[int]:
#     hm = {}
#     for i in range(len(lst)):
#         hm[lst[i]] = i
#     print(hm)
#     for i in range(len(lst)):
#         complement = target - lst[i]
#         if complement in hm and complement != i:
#             return [i, hm[complement]]
#
#
# print(twosum([2, 3, 4], 6))


# def twosum(lst: list, target: int) -> list[int]:
#     hm = {}
#     for i in range(len(lst)):
#         complement = target - lst[i]
#         if complement in hm:
#             return [i, hm[complement]]
#         hm[lst[i]] = i
#     return []
#
#
# print(twosum([2, 3, 4], 6))


def isPalindrome(x: int) -> bool:
    temp = x
    revers_nums = 0
    while temp:
        digit = temp % 10
        print(digit)
        revers_nums = revers_nums * 10 + digit

        temp //= 10
        print(temp)
    return revers_nums == x


print(isPalindrome(121))
