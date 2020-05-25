from django.apps import AppConfig


class SchedularConfig(AppConfig):
    name = 'schedular'

    def ready(self):
        from schedular import cron_job
        cron_job.start()
