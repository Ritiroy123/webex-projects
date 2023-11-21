import schedule
import time

def job():
    print("I'm working...")

schedule.every(1).seconds.do(job)
def job_schedule():
    print("print the main value ")
schedule.every(1).seconds.do(job_schedule)



while True:
    schedule.run_pending()
    time.sleep(5)
    
