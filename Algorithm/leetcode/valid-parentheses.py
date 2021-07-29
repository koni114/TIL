#- 괄호로 된 입력값이 올바른지 판별해라
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        d = {")": "(",
             "]": "[",
             "}": "{"}
        for char in s:
            if char not in s:
                stack.append(char)
            elif not stack or d[char] != stack.pop():
                return False
        return len(stack) == 0