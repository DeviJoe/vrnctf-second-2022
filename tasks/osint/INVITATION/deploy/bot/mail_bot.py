import subprocess
import time
import sys
import email_utils

from defines import *

print("Starting bot")
count = 0
while True:
    try:
        subprocess.check_call(['python', 'receive_mails.py'], shell=False, timeout=60)
        subprocess.check_call(['python', 'send_mails.py'], shell=False, timeout=60)
    except subprocess.TimeoutExpired:
        print('error!!!')
        email_utils.send_email('Error',
                               'Exception timeout subprocess ' + str(count),
                               '')
        count += 1
        if count > 5:
            sys.exit(1)
    except Exception as e:
        print(str(e))
        email_utils.send_email('Error',
                               'Exception in module mail_bot ' + str(e),
                               '')
        sys.exit(1)
    time.sleep(REPEAT_TIME)

