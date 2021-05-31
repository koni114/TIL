#- 무게(weight)를 계산하는 함수를 작성하고,
#- 각각의 세부적인 예외처리를 수행
#-  예외 종류: InvaildDensityError
#-          InvaildVolumeError

class Error(Exception):
    pass


class InvaildDensityError(Error):
    pass


class InvaildVolumeError(Error):
    pass


class NegativeDensityError(Error):
    pass

def determine_weight(volume, density):
    if density < 0:
        raise NegativeDensityError('밀도는 0보다 커야함')
    if volume < 0:
        raise InvaildVolumeError('부피는 0보다 커야함')
    return density / volume

