"""
- 이진 트리를 입력받아 전위 순회, 중위 순회, 후위 순회한 결과를 출력하는 프로그램을 작성해라
- 첫째 줄에는 이진 트리의 노드의 개수 N(1<=N<=26)이 주어짐
- 둘째 줄부터 N개의 줄에 걸쳐 각 노드와 그의 왼쪽 자식 노드, 오른쪽 자식 노드가 주어짐

- 항상 A가 루트 노드가 되며, 자식 노드가 없는 경우에는 .으로 표시
"""
import sys
inf = sys.stdin
N = int(inf.readline().strip())
tree = dict()
for _ in range(N):
    parent, left, right = [i for i in inf.readline().strip().split()]
    tree[parent] = [left, right]

def preorder(node):
    if node == '.':
        return
    print(f"{node}", end="")
    [preorder(i) for i in tree[node]]

def inorder(node):
    if node == '.':
        return
    inorder(tree[node][0])
    print(f"{node}", end="")
    inorder(tree[node][1])

def postorder(node):
    if node == '.':
        return
    postorder(tree[node][0])
    postorder(tree[node][1])
    print(f"{node}", end="")


preorder('A')
print("")
inorder('A')
print("")
postorder('A')