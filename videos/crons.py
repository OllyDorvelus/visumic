from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "videos.crons.MyCronJob"   # a unique code

    def do(self):
        print("Hello World")    # do your thing here
