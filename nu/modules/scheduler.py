# Periodic Scheduler

import asyncio

async def Task(interval, action, actionargs):
    while True:
        await action(*actionargs)
        await asyncio.sleep(interval)

class Scheduler:

    def __init__(self):
        self.tasks = []

    def start(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(asyncio.wait(self.tasks))

    def add(self, interval, action, actionargs=()):
        self.tasks.append( Task(interval, action, actionargs) )

    def stop(self):
        self.tasks = {}
        self.loop.close()
