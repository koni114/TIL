"""
- 펠린드롬 문자열을 출력해라
"""
import sys
inf = sys.stdin
text = inf.readline().strip()

def longest_palindrome(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left+1:right]

    if len(s) < 1 and s == s[::-1]:
        return s

    result = ''
    for i in range(len(s)-1):
        result = max(result,
                     expand(i, i+1),
                     expand(i, i+2),
                     key=len
                     )
    return result

print(longest_palindrome('bababad'))