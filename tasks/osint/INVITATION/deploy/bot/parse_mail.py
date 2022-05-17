import re

from defines import *
from parse_handlers import *


# handlers = {
#     ['hello': handler_hello]
# }


def parse_mail(topic, content):
    # topic = topic
    # handlers
    # if topic in handlers:
    handler = handlers[topic]
    if handler:
        return handlers[topic](content)
    return None
