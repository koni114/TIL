#- 정렬 알고리즘 정리

#- 1. bubble sort
#- 서로 인접한 두 원소를 검사하여 정렬하는 알고리즘
#- 인접한 두 개의 레코드를 검사하여 크기가 순서대로 되어 있지 않으면 서로 교환함
#- 시간 복잡도: O(N^2)

#- 향상된 bubble sort
#- swap 이 한 번도 일어나지 않았으면 더 이상 정렬할 원소가 없다는 의미이므로,
#- sorting 종료
def bubble_sort(num_list):
    for i, _ in enumerate(num_list):
        is_swap = False
        for j in range(len(num_list)-(i+1)):
            if num_list[j] >= num_list[j+1]:
                is_swap = True
                num_list[j], num_list[j+1] = num_list[j+1], num_list[j]
        if not is_swap:
            break
    print(num_list)

#- 2. selection sort
#- 제자리 정렬(in-place sorting) 알고리즘 중 하나
#- 입력 배열 이외에 다른 추가 메모리를 요구하지 않음
def selection_sort(num_list):
    for i in range(len(num_list)-1):
        tmp, idx = num_list[i], i
        for j in range(i+1, len(num_list)):
            if num_list[j] <= tmp:
                tmp, idx = num_list[j], j
        if not i == idx:
            num_list[i], num_list[idx] = num_list[idx], num_list[i]
    print(num_list)

#- 3. insertion sort
#- 두 번째 자료부터 시작하여 그 앞의 자료들과 비교하여 삽입할 위치를 지정한 후 자료를 뒤로 옮기고
#- 지정한 자리에 자료를 삽입하여 정렬하는 알고리즘
def insertion_sort(num_list):
    for i in range(1, len(num_list)):
        for j in range(i):
            if num_list[i] < num_list[j]:
                tmp = num_list[i]
                num_list[j+1:i+1] = num_list[j:i]
                num_list[j] = tmp
                break
    print(num_list)

insertion_sort([10, 8, 5, 6, 2, 4])

#- 4. merge sort
from collections import deque
arr = [5, 4, 1, 2, 3]
def merge_sort(left, right):
    if left >= right:
        return

    mid = (left + right) // 2
    merge_sort(left, mid)
    merge_sort(mid+1, right)
    merge(left, right)

def merge(left, right):
    mid = (left + right) // 2
    i, j = left, mid+1

    tmp = deque()
    while i <= mid and j <= right:
        if arr[i] < arr[j]:
            tmp.append(arr[i])
            i += 1
        else:
            tmp.append(arr[j])
            j += 1

    while i <= mid:
        tmp.append(arr[i])
        i += 1

    while j <= right:
        tmp.append(arr[j])
        j += 1

    arr[left:right+1] = tmp