text_path = './test.txt'
with open(text_path, 'r') as f:
    f.readline()

def binary_search(arr, find_value):
    left, right = 0, len(arr)-1
    is_value = False
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == find_value:
            is_value = True
            break
        elif arr[mid] > find_value:
            right = mid-1
        else:
            left = mid+1
    return is_value, mid





