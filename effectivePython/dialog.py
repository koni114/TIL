import app

print("dialog 입니다.")

class Dialog:
    def __init__(self, save_dir):
        self.save_dir = save_dir


save_dialog =Dialog(app.prefs.get('save_dir'))


def now():
    pass
