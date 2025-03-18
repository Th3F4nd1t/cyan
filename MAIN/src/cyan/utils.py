# utils file
import datetime

class LogLevel:
    # LEVEL = [TAG, COLOR, SHOULD TERMINATE]
    INFO = ["INFO", "", False]
    SUCCESS = ["SUCCESS", "\033[1;34m", False]
    WARNING = ["WARNING", "\033[1;33m", False]
    ERROR = ["ERROR", "\033[1;31m", False]
    FATAL = ["FATAL", "\033[1;31m", True]

def log(message: str, level: LogLevel) -> None:
    with open("./log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} [{level[0]}] {message}\n")
        print(f"{level[1]}{datetime.datetime.now()} [{level[0]}] {message}\033[0m") # PROD: COMMENT THIS OUT
        if level[2]:
            f.write("Exiting due to fatal error\n")
            print("\033[1;31mExiting due to fatal error\033[0m") # PROD: COMMENT THIS OUT
            exit(1)

def reset_log():
    with open("./log.txt", "w") as f:
        f.write("")


# Put testing here so that when run, it will be seen but not when imported
if __name__ == "__main__":
    # Test logs
    log("This is a test log", LogLevel.INFO)
    log("This is a test warning", LogLevel.WARNING)
    log("This is a test error", LogLevel.ERROR)
    log("This is a test fatal", LogLevel.FATAL)