#- try/except 구문에서 from 구문 활용하기
#- 1. 최상위 예외 정의
import logging

class Error(Exception):
    pass

class NegativeDensityError(Error):
    pass

class InvaildDensityError(Error):
    pass

class InvaildVolumeError(Error):
    pass


def determine_weights(density, volume):
    if density < 0:
        raise NegativeDensityError('밀도는 음수여서는 안됩니다.')
    if volume < 0:
        raise InvaildVolumeError('부피는 0보다 작아서는 안됩니다.')
    return volume / density

try:
    weight = determine_weights(-1, -1)
except NegativeDensityError as exc:
    raise ValueError('밀도로 음수가 아닌 값을 제공해야 합니다.') from exc
except InvaildDensityError:
    weight = 0
except Error:
    logging.exception('호출 코드에 버그가 있음')
except Exception:
    logging.exception('API 코드에 버그가 있음')

