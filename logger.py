import logging
LOGFILENAME="./logs.txt"
logging.basicConfig(format='%(asctime)-15s %(message)s', filename=LOGFILENAME, level=logging.DEBUG)