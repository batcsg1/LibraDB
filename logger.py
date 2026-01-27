from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
  
class Colors:
    def __init__(self):
        self.error = '\033[31m'
        self.success = '\033[32m'
        self.warning = '\033[93m'
        self.reset = '\033[0m'
        self.info = '\u001b[1;34m'

class Logger:
    def __init__(self, logFile = './logs/log' ):
        self.logFile = logFile
        self.colors = Colors()
    
    def _log(self, message, color="\033[97m"):       
        message == print(f"{color}{message}{self.colors.reset}")
        self._write(message)
    
    def _write(self, message):
        with open(self.logFile, 'a') as f:
            try:
                f.write(f"{now} : {message}\n")
            except Exception as e:
                print(f"Error writing to log file: {e}")
    
    
    
