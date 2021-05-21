import app


class Dialog:
    def __init__(self, save_dir):
        self.save_dir = save_dir


save_dialog = Dialog()


def show():
    pass

def configure():
    save_dialog.save_dir = app.prefs.get('save_dir')