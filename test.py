import schedule as sc
import time

def job():
    print('Teste')

index = 0
job1 = sc.every().monday.at('13:00').do(job).tag(index)
job2 = sc.every().tuesday.at('16:00').do(job).tag(index+1)

for i in enumerate(sc.get_jobs()):
    print(i)
    if i[0] == index:
        sc.clear(index)

while True:
    sc.run_pending()
    jobs = sc.get_jobs()
    print(jobs)
    time.sleep(1)