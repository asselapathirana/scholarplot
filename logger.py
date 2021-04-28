import logging
LOGFILENAME="./logs.txt"
logging.basicConfig(format='%(asctime)-15s %(message)s', 
                    handlers=[logging.FileHandler(LOGFILENAME, 'a+', 'utf-8')],
                    level=logging.DEBUG)