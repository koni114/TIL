import re
s = "A man, a plan, a canal: Panama"
s = re.sub("[^a-zA-Z0-9]", "", s)




class Solution:
    def isPalindrome(self, s: str) -> bool:
        s_alnum = [c.lower() for c in s if c.isalnum()]
        return s_alnum == s_alnum[::-1]

