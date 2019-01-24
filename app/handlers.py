def default_handler():
    return 'alert("I do nothing");'


def mail_request_handler() -> str:
    return 'window.open("https://www.google.com/gmail/");'
