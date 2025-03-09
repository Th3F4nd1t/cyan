# utils file
import datetime

printLogs = True

def log(message: str, level: str) -> None:
    with open("./log.txt", "a") as f:
        f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {level.upper()}: {message}\n")

    if level == "INFO" or level == "WARNING":
        if printLogs:
            print(f"{level.upper()}: {message}")
    elif level == "ERROR" or level == "FATAL":
        print(f"{level.upper()}: {message}")
        print("Exiting the program...")
        with open("./log.txt", "a") as f:
            f.write(str(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {level.upper()}: Exiting the program...\n"))
        exit(1)
    
def resetLogger():
    with open("./log.txt", "w") as f:
        f.write("")