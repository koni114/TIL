# 두 개의 정방 매트릭스의 곱을 구현하는 한줄 컴프리핸션 코드
matrix_a = [[2, 5], [1, 1]]
matrix_b = [[1, 1, 2], [2, 1, 1]]
[[sum(a*b for a, b in zip(row_a, col_b)) for col_b in zip(*matrix_b)] for row_a in matrix_a]

# 함수 작성 예시

matrix_x = [[2, 5], [1, 1]]
matrix_y = [[1, 1, 2], [2, 1, 1]]
matrix_z = [[2, 4], [5, 3], [1, 3]]
matrix_w = [[2, 5], [1, 1], [2, 2]]


def is_product_availability_matrix(matrix_a, matrix_b):
    return len(matrix_a[0]) == len(matrix_b)


print(is_product_availability_matrix(matrix_y, matrix_z))  # Expected value: True
print(is_product_availability_matrix(matrix_z, matrix_x))  # Expected value: True
print(is_product_availability_matrix(matrix_z, matrix_w))  # Expected value: False
print(is_product_availability_matrix(matrix_x, matrix_x))  # Expected value: True


matrix_x = [[2, 5], [1, 1]]
matrix_y = [[1, 1, 2], [2, 1, 1]]
matrix_z = [[2, 4], [5, 3], [1, 3]]


def matrix_product(matrix_a, matrix_b):
    if not is_product_availability_matrix(matrix_a, matrix_b):
        raise ArithmeticError
    return [[sum(a*b for a, b in zip(row_a, col_b)) for col_b in zip(*matrix_b)] for row_a in matrix_a]


print(matrix_product(matrix_y, matrix_z))  # Expected value: [[9, 13], [10, 14]]
print(matrix_product(matrix_z, matrix_x))  # Expected value: [[8, 14], [13, 28], [5, 8]]
print(matrix_product(matrix_x, matrix_x))  # Expected value: [[9, 15], [3, 6]]
print(matrix_product(matrix_z, matrix_w))  # Expected value: False

