# def romanToInt(s: str) -> int:
#     m = {
#         'I': 1,
#         'V': 5,
#         'X': 10,
#         'L': 50,
#         'C': 100,
#         'D': 500,
#         'M': 1000
#     }
#
#     ans = 0
#
#     for i in range(len(s)):
#         if i < len(s) - 1 and m[s[i]] < m[s[i + 1]]:
#             ans -= m[s[i]]
#         else:
#             ans += m[s[i]]
#
#
# romanToInt("LVIII")
import hashlib


def calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

calculate_signature()