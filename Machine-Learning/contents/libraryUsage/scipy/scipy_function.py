#- 앞면이 나올확률이 0.51일 때, 동전을 n번 던져 다수가 나올 확률
from scipy.stats import binom
1 - binom.cdf(499, 1000, 0.51)   #- 0.75
1 - binom.cdf(4999, 10000, 0.51) #- 0.98
