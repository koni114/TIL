## Factory pattern
class AndroidSmartPhone:
    def send(self, message):
        print("send a message via Android platform")


class WindowsSmartphone:
    def send(self, message):
        print("send a message via Widnow Mobile platform")


class iOSSmartphone:
    def send(self, message):
        print("send a message via iOS platform")


class SmartphoneFactory(object):
    def __init__(self):
        pass

    def create_smartphone(self, device_type):
        if device_type == 'android':
            smartphone = AndroidSmartPhone()
        elif device_type == 'window':
            smartphone = WindowsSmartphone()
        else:
            smartphone = iOSSmartphone()

        return smartphone


smartphone_factory = SmartphoneFactory()
message_sender1 = smartphone_factory.create_smartphone('android')
message_sender1.send('hi')

message_sender2 = smartphone_factory.create_smartphone('window')
message_sender2.send('hi')

message_sender3 = smartphone_factory.create_smartphone('ios')
message_sender3.send('hi')

