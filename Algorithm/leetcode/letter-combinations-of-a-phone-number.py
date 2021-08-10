"""
2에서 9까지의 숫자를 포함하는 문자열이 주어지면
숫자가 나타낼 수 있는 모든 가능한 문자 조합을 반환합니다.
어떤 순서로든 답을 반환하십시오.

전화 버튼과 마찬가지로 숫자 대 문자 매핑이 아래에 나와 있습니다.
1은 어떤 문자에도 매핑되지 않습니다.

Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Input: digits = ""
Output: []

Input: digits = "2"
Output: ["a","b","c"]
"""
from typing import List
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        dics = {'1': "", '2': "abc", "3": 'def', "4": "ghi", "5": "jkl",
               "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        results = []
        def dfs(index, path):
            if len(path) == len(digits):
                results.append(path)
                return

            for i in range(index, len(digits)):
                for char in dics[digits[i]]:
                    dfs(i + 1, path + char)

        if not digits:
            return []

        dfs(0, "")
        return results

s = Solution()
s.letterCombinations("23")

