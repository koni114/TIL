import sys

arr = [8, 4, 3, 16, 5, 2, 10, 1, 2, 2]
def bubble_sort(arr):
    for i in range(len(arr)):
        toggle = 0
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j+1]:
                toggle = 1
                arr[j], arr[j+1] = arr[j+1], arr[j]
        if not toggle:
            break
    return arr

bubble_sort(arr)

def selection_sort(arr):
    for i in range(len(arr)):
        min_num, idx = sys.maxsize, 0
        for j in range(i, len(arr)):
            if arr[j] < min_num:
                min_num, idx = arr[j], j
        arr[i], arr[j] = min_num, arr[i]
    return arr

selection_sort(arr)


def selection_sort(arr):
    for i in range(len(arr)):
        min_num, idx = sys.maxsize, 0
        for j in range(i, len(arr)):
            if arr[j] < min_num:
                min_num, idx = arr[j], j
        arr[i], arr[idx] = min_num, arr[i]

    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        curr_num = arr[i]
        left = i - 1
        while left >= 0 and arr[left] > curr_num:
            arr[left + 1] = arr[left]
            arr[left] = curr_num
            left -= 1
    return arr

insertion_sort(arr)

def merged_sort(arr):
    if len(arr) < 2:
        return arr

    mid = len(arr) // 2
    low_arr = merged_sort(arr[:mid])
    high_arr = merged_sort(arr[mid:])

    low = high = 0
    merged_arr = []

    while low < len(low_arr) and high < len(high_arr):
        if low_arr[low] < high_arr[high]:
            merged_arr.append(low_arr[low])
            low += 1
        else:
            merged_arr.append(high_arr[high])
            high += 1

    merged_arr += low_arr[low:]
    merged_arr += high_arr[high:]

    return merged_arr

#- 최적화된 코드
def merge_sort(arr):
    def sort(low, high):
        if high - low < 2:
            return

        mid = (high + low) // 2
        sort(low, mid)
        sort(mid, high)

        merge(low, mid, high)

    def merge(low, mid, high):
        l, h = low, mid
        results = []
        while l < mid and h < high:
            if arr[l] < arr[h]:
                results.append(arr[l])
                l += 1
            else:
                results.append(arr[h])
                h += 1

        while l < mid:
            results.append(arr[l])
            l += 1

        while h < high:
            results.append(arr[h])
            h += 1

        for i in range(low, high):
            arr[i] = results[i - low]

    return sort(0, len(arr))


merge_sort(arr)


def quick_sort(arr):
    def sort(low, high):
        if high <= low:
            return

        mid = partition(low, high)
        sort(low, mid - 1)
        sort(mid, high)

    def partition(low, high):
        pivot = arr[(low + high) // 2]
        while low <= high:
            while arr[low] < pivot:
                low += 1
            while arr[high] > pivot:
                high -= 1
            if low <= high:
                arr[low], arr[high] = arr[high], arr[low]
                low, high = low + 1, high - 1
        return low

    return sort(0, len(arr) - 1)

quick_sort(arr)

