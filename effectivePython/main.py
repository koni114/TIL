import tracemalloc

tracemalloc.start(10)
time1 = tracemalloc.take_snapshot()

import waste_memory

x = waste_memory.run()
time2 = tracemalloc.take_snapshot()

#- compare_to 메소드의 인자를 traceback으로 입력
stats = time2.compare_to(time1, 'traceback')
top = stats[0]
print("가장 많이 사용하는 부분은:")
print('\n'.join(top.traceback.format()))
