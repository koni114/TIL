"""
중복 문자 제거
"""
def removeDuplicateLetters(s):
    import collections
    #- seen --> 이미 처리된 문자 여부 확인
    counter, seen, stack = collections.Counter(s), set(), []

    for char in s:
        counter[char] -= 1
        if char in seen:
            continue
        #- 뒤에 붙일 문자가 남아 있다면 stack 에서 제거
        while stack and char < stack[-1] and counter[stack[-1]] > 0:
            seen.remove(stack.pop())
        stack.append(char)
        seen.add(char)

    return ''.join(stack)

