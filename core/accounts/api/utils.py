from threading import Thread

class EmailThread(Thread):
    """Sends an email in a separate thread."""
    def __init__(self, email_obj):
        Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()