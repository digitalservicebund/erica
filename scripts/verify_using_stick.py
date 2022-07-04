import os

from erica.erica_legacy.pyeric.eric import verify_using_stick, verify_using_stick_with_queue

if os.getenv("ENABLED_VERSION") == 'v2':
    print(verify_using_stick_with_queue())
else:
    print(verify_using_stick())
