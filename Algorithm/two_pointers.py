"""
투 포인터 이용
- 왼쪽 포인터와 오른쪽 포인터를 left, right 로 setting 하고, 특정 조건에따라 움직여가면서
  원하는 값을 찾아가는 것
"""

#- 투 포인터를 이용하여 두 수의 합의 조합을 return 하는 코드 예제
#- 다음은 nums가 정렬이 되어있다는 가정하에 사용 가능
def two_sum(nums, target):
    left, right = 0, len(nums)-1
    while not left == right:
        if nums[left] + nums[right] < target:
            left += 1
        elif nums[left] + nums[right] > target:
            right -= 1
        else:
            return f"{nums[left]} + {nums[right]}"


two_sum([1, 4, 5, 6], 11)
