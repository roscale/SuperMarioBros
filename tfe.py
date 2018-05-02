import os
os.system("/bin/bash -c 'chmod +x venv/bin/* && source venv/bin/activate && cd game/ && PYTHONPATH=\"{}\" python -O smb.py'".format(os.path.abspath("./")))
