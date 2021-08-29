## 정렬 
### 버블 정렬(Bubble sort)
- 데이터를 두 개씩 묶어서 비교 후 크기가 큰 쪽이 오른쪽으로 가도록 자리를 바꿔가는 방식
- 최선 O(N) : 정렬이 이미 되어있는 경우 -> 한 번의 순회로 정렬 여부를 알 수 있음
- 최악 O(N^2) : 정렬이 하나도 안되어있는 경우 -> 각 자리를 찾기 위해서 n번 순회를 해야하며 n번의 회전 동안에 요소의 개수만큼 또 순회를 해야함
- 코드 구현
~~~python
#- len(arr) - i - 1 에서 - 1은 i, i+1를 비교하기 때문
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
~~~

### 선택 정렬(Selection Sort)
- 구현 방법
  - 먼저 주어진 리스트 중에 최소값을 찾음
  - 그 값을 맨 앞에 위치한 값과 교환
  - 이제 맨 앞을 제외하고 다시 순회하며 최소값을 찾음
  - 그 값을 맨 앞 위치 바로 다음 위치와 교체
- 시간 복잡도
  - 최선 - O(N^2): 정렬이 이미 되어있는 경우
  - 최악 - O(N^2): 정렬이 하나도 안되어있는 경우 - 매 번 정해진 자리에 올 수 있는 최소값을 찾아야 하기 때문. 때문에 성능이 매우 떨어짐  
- 제자리 정렬
- 데이터가 중복된 경우 위치가 바뀔 수 있기 때문에 불안정 정렬
~~~python
def selection_sort(arr):
    for i in range(len(arr)):
        min_num, idx = sys.maxsize, 0
        for j in range(i, len(arr)):
            if arr[j] < min_num:
                min_num, idx = arr[j], j
        arr[i], arr[j] = min_num, arr[i]
    return arr

selection_sort(arr)
~~~

### 삽입 정렬(insertion sort)
- 구현 방법
  - 항상 두 번째 요소부터 시작하여 왼쪽 요소들과 비교하여 자신의 위치를 찾아감
  - 항상 현재 정렬 회차에서 비교하는 값의 왼쪽 배열은 정렬되어 있음
- 시간 복잡도
  - 최선 - O(N) : 정렬이 이미 되어있는 경우 -> 한 번의 순회로 정렬 여부를 알 수 있음 
  - 최악 - O(N^2) : 정렬이 하나도 안되어있는 경우 -> 각 자리를 찾기 위해 n번의 순회를 해야하며 n번의 회전 동안에 요소의 개수만큼 순회 필요 
- 제자리 정렬이므로 메모리가 절약된다는 장점이 있음
~~~python
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
~~~

### 병합 정렬(Merge Sort)
- 분할 정복(divide and conquer) 기법과 재귀 알고리즘을 이용한 정렬 알고리즘
- 주어진 배열을 원소가 하나 밖에 남지 않을 때까지 쪼갠 다음, 병합하는 과정에서 정렬하는 알고리즘
- 계속 둘로 쪼갠 후에 다시 크기 순으로 재배열
- 시간 복잡도
  - 최선 - O(NlogN) : 정렬이 이미 되어있는 경우
  - 최악 - O(NlogN) : 정렬이 하나도 안 되어있는 경우 

~~~python
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
~~~

### 퀵 정렬(quick sort)
- 분할 정복기법을 활용한 정렬 방법
- 참조 지역성의 원리가 가장 뛰어나 속도가 삼대장 중에서 가장 빠름
- 시간 복잡도
  - 최선 O(NlogN) : 정렬이 하나도 안되어 있는 경우
  - 최악 O(N^2) : 정렬이 되어있는 경우 + pivot값이 맨 뒤에 있는 경우 -> pivot이 항상 오른쪽에 위치하여 pivot의 변경이 전혀 이루어지지 않음 
- 알고리즘 특징
  - 속도가 빠름. 시간 복잡도가 O(nlogn)을 가지는 다른 정렬 알고리즘과 비교했을 때도 가장 빠름
  - 추가적인 메모리 공간을 필요로 하지 않음(In-place)
  - 정렬된 리스트에 대해서는 퀵 정렬의 불균형 분할에 의해 오히려 수행시간에 더 걸림   
  - 퀵 정렬의 불균형 분할을 방지하기 위해 피벗을 선택할 때 더욱 균등하게 분할할 수 있는 데이터 선택
~~~python
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
~~~