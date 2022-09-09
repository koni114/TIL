# vector_size_check
# vector 간 덧셈 또는 뺄셈 연산을 할 때,
# 연산이 가능한 사이즈인지를 확인하여 가능 여부를 True 또는 False로 반환함
# 실행결과
# print(vector_size_check([1,2,3], [2,3,4], [5,6,7])) # Expected value: True
# print(vector_size_check([1, 3], [2,4], [6,7])) # Expected value: True
# print(vector_size_check([1, 3, 4], [4], [6,7])) # Expected value: False
def vector_size_check(*vector_variables):
    return None

# vector_addition : vector간 덧셈을 실행하여 결과를 반환함, 단 입력되는 vector의 갯수와 크기는 일정하지 않음
# print(vector_addition([1, 3], [2, 4], [6, 7])) # Expected value: [9, 14]
# print(vector_addition([1, 5], [10, 4], [4, 7])) # Expected value: [15, 16]
# print(vector_addition([1, 3, 4], [4], [6,7])) # Expected value: ArithmeticError
def vector_addition(*vector_variables):
    return None

# vector_subtraction : vector간 뺄셈을 실행하여 결과를 반환함, 단 입력되는 vector의 갯수와 크기는 일정하지 않음
# 실행결과
# print(vector_subtraction([1, 3], [2, 4])) # Expected value: [-1, -1]
# print(vector_subtraction([1, 5], [10, 4], [4, 7])) # Expected value: [-13, -6]
def vector_subtraction(*vector_variables):
    if not vector_size_check(*vector_variables):
        raise ArithmeticError
    return None

# scalar_vector_product	 : 하나의 scalar 값을 vector에 곱함, 단 입력되는 vector의 크기는 일정하지 않음
# print (scalar_vector_product(5,[1,2,3])) # Expected value: [5, 10, 15]
# print (scalar_vector_product(3,[2,2])) # Expected value: [6, 6]
# print (scalar_vector_product(4,[1])) # Expected value: [4]
def scalar_vector_product(alpha, vector_variable):
    return None

# matrix_size_check : matrix 간 덧셈 또는 뺄셈 연산을 할 때, 연산이 가능한 사이즈인지를 확인하여 가능 여부를 True 또는 False로 반환함
# matrix_x = [[2, 2], [2, 2], [2, 2]]
# matrix_y = [[2, 5], [2, 1]]
# matrix_z = [[2, 4], [5, 3]]
# matrix_w = [[2, 5], [1, 1], [2, 2]]
# print (matrix_size_check(matrix_x, matrix_y, matrix_z)) # Expected value: False
# print (matrix_size_check(matrix_y, matrix_z)) # Expected value: True
# print (matrix_size_check(matrix_x, matrix_w)) # Expected value: True
def matrix_size_check(*matrix_variables):
    return None

# is_matrix_equal : 비교가 되는 n개의 matrix가 서로 동치인지 확인하여 True 또는 False를 반환함
# matrix_x = [[2, 2], [2, 2]]
# matrix_y = [[2, 5], [2, 1]]
# print (is_matrix_equal(matrix_x, matrix_y, matrix_y, matrix_y)) # Expected value: False
# print (is_matrix_equal(matrix_x, matrix_x)) # Expected value: True
def is_matrix_equal(*matrix_variables):
    return None

# matrix_addition	: matrix간 덧셈을 실행하여 결과를 반환함, 단 입력되는 matrix의 갯수와 크기는 일정하지 않음
# matrix_x = [[2, 2], [2, 2]]
# matrix_y = [[2, 5], [2, 1]]
# matrix_z = [[2, 4], [5, 3]]
# print (matrix_addition(matrix_x, matrix_y)) # Expected value: [[4, 7], [4, 3]]
# print (matrix_addition(matrix_x, matrix_y, matrix_z)) # Expected value: [[6, 11], [9, 6]]
def matrix_addition(*matrix_variables):
    if not matrix_size_check(*matrix_variables):
        raise ArithmeticError
    return None

# matrix_subtraction : matrix간 뺄셈을 실행하여 결과를 반환함, 단 입력되는 matrix의 갯수와 크기는 일정하지 않음
# matrix_x = [[2, 2], [2, 2]]
# matrix_y = [[2, 5], [2, 1]]
# matrix_z = [[2, 4], [5, 3]]
# print (matrix_subtraction(matrix_x, matrix_y)) # Expected value: [[0, -3], [0, 1]]
# print (matrix_subtraction(matrix_x, matrix_y, matrix_z)) # Expected value: [[-2, -7], [-5, -2]]
def matrix_subtraction(*matrix_variables):
    if not matrix_size_check(*matrix_variables):
        raise ArithmeticError
    return None

# matrix_transpose	: matrix의 전치행렬을 구하여 결과를 반환함, 단 입력되는 matrix의 크기는 일정하지 않음
# matrix_w = [[2, 5], [1, 1], [2, 2]]
# matrix_transpose(matrix_w) =  [[2, 1, 2], [5, 1, 2]]
def matrix_transpose(matrix_variable):
    return None

# scalar_matrix_product	 : 하나의 scalar 값을 matrix에 곱함, 단 입력되는 matrix의 크기는 일정하지 않음
# matrix_x = [[2, 2], [2, 2], [2, 2]]
# matrix_y = [[2, 5], [2, 1]]
# matrix_z = [[2, 4], [5, 3]]
# matrix_w = [[2, 5], [1, 1], [2, 2]]
# print(scalar_matrix_product(3, matrix_x)) #Expected value: [[6, 6], [6, 6], [6, 6]]
# print(scalar_matrix_product(2, matrix_y)) #Expected value: [[4, 10], [4, 2]]
# print(scalar_matrix_product(4, matrix_z)) #Expected value: [[8, 16], [20, 12]]
# print(scalar_matrix_product(3, matrix_w)) #Expected value: [[6, 15], [3, 3], [6, 6]]
def scalar_matrix_product(alpha, matrix_variable):
    return None

# matrix_x= [[2, 5], [1, 1]]
# matrix_y = [[1, 1, 2], [2, 1, 1]]
# matrix_z = [[2, 4], [5, 3], [1, 3]]
# print(is_product_availability_matrix(matrix_y, matrix_z)) # Expected value: True
# print(is_product_availability_matrix(matrix_z, matrix_x)) # Expected value: True
# print(is_product_availability_matrix(matrix_z, matrix_w)) # Expected value: False //matrix_w가없습니다
# print(is_product_availability_matrix(matrix_x, matrix_x)) # Expected value: True
def is_product_availability_matrix(matrix_a, matrix_b):
    return None

# matrix_x= [[2, 5], [1, 1]]
# matrix_y = [[1, 1, 2], [2, 1, 1]]
# matrix_z = [[2, 4], [5, 3], [1, 3]]
# print(matrix_product(matrix_y, matrix_z)) # Expected value: [[9, 13], [10, 14]]
# print(matrix_product(matrix_z, matrix_x)) # Expected value: [[8, 14], [13, 28], [5, 8]]
# print(matrix_product(matrix_x, matrix_x)) # Expected value: [[9, 15], [3, 6]]
# print(matrix_product(matrix_z, matrix_w)) # Expected value: False
def matrix_product(matrix_a, matrix_b):
    if not is_product_availability_matrix(matrix_a, matrix_b):
        raise ArithmeticError
    return None

    