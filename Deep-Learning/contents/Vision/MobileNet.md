## MobileNet 
### Mobilenet이 왜 필요할까요? 
- 고성능의 디바이스가 아니라 자동차, 드론, 스마트폰과 같은 환경에서는 CPU를 하나 정도 가지고 있는 경우도 많고, GPU가 없을 수도 있으며, 메모리도 부족함
- 높은 퍼포먼스는 뒷전이고 돌리는 것 자체가 힘들 수 있음
- 이러한 환경에서 CNN을 돌려야 하는 경우 MobileNet 컴퓨터 성능이 제한되거나 배터리 퍼포먼스가 중요한 곳에서 사용될 목적으로 설계된 CNN 구조

### 작은 신경망을 만들기 위한 기술들
- Remove Fully-Connected Layers 
  - 파라미터의 90% 정도가 Fully-Connected layers에 들어감 
- Kernel Reduction(3x3 -> 1x1)
  - 3x3 -> 1x1로 연산량을 줄임 
- Channel Reduction
  - 채널 수를 줄임 
- Evenly(고르게) Spaced Downsampling
  - 초반에 downsampling을 많이 : accuracy가 떨어지지만 파라미터가 적어짐
  - 후반에 downsampling을 많이 : accuracy가 좋아지지만 파라미터가 많아짐
- Depthwise Seperable Convolutions
- Shuffle Operations
- Distillation & Compression

### mobileNet에서 사용되는 기술들 
- Channel Reduction
- Depthwise Seperable Convolutions
- Distillation & Compression