class HandlersManager:

    @staticmethod
    def get_handler(intent):
        if intent == 'mail':
            return HandlersManager.__mail_request_handler()
        else:
            return HandlersManager.__default_handler()

    @staticmethod
    def __default_handler():
        return 'alert("I do nothing");'

    @staticmethod
    def __mail_request_handler(self) -> str:
        return 'window.open("https://www.google.com/gmail/");'
