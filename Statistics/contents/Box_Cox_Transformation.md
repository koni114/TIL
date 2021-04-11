# Box-Cox Transformation
- power Transformation이라고도 함
- Box-Cox의 주된 용도는 데이터를 정규 분포에 가깝게 변환하거나 분산을 안정화 시킬 용도
- 정규성을 가정하는 분석법이나 정상성을 요구하는 분석법에 앞서 사용할 수 있음 
- 멱변환을 취하기 위해서는 모두 양수어야한다는 가정이 필요하지만, 실제로는 데이터의 최소 값이 양수가 되도록 데이터를 shift하는 방식으로 이용
- 수식은 다음과 같음(여기서의 로그는 자연로그, 밑이 exp)
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?x&space;>&space;0,&space;g(x)&space;=&space;\begin{pmatrix}&space;\frac{x^{\lambda}-&space;1}{\lambda},&space;\lambda&space;\neq&space;0\\&space;log(x),&space;\lambda&space;=&space;0&space;\end{pmatrix}" /></p>

- 분석자는 목적에 맞게 람다를 잘 결정해야함
- 주목할만한 람다로 0, 1, 2가 있음
  - lambda = 0, g(0)(x) = log(x)
  - lambda = 2, g(2)(x) = (sqrt(x) - 1)  / 2 
  - lambda = 1, g(1)(x) = x - 1이 되므로, 사실상 변환에서 1을 빼는 것은 거의 의미가 없으므로  
   항등변환이며, 변환이 필요 없음을 의미함
- 즉 lambda의 신뢰 구간에 1이 포함되면 변환의 의미가 크게 없음을 의미함  
  분산이 거의 일정함을 의미함
 