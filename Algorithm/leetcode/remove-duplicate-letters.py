"""
중복된 문자를 제외하고 사전식 순서(Lexicographical Order)로 나열
"""
class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        from collections import Counter
        c, stack = Counter(s), []
        stack.append(s[0])
        c[s[0]] -= 1

        for char in s[1:]:
            while stack and stack[-1] > char and c[stack[-1]] and char not in stack:
                stack.pop()
            if char not in stack:
                stack.append(char)
            c[char] -= 1
        return "".join(stack)

s = Solution()
s.removeDuplicateLetters("abacb")


