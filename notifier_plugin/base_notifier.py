class BaseNotifier:
    def __init__(self, name):
        self.name = name
        self.active = True

    def send(self, message):
        raise NotImplementedError("send() must be implemented")

    def test_ping(self):
        raise NotImplementedError("test_ping() must be implemented")
