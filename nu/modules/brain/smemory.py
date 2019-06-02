# Short-term memory (PriorityQueue)

import logging

import asyncio
import redis
from queue import PriorityQueue
#from threading import Thread
from nu.modules.config import smemory_config


logger = logging.getLogger()

class SMemoryStorageManager():

    def __init__(self):
        config = smemory_config()
        hostname = config.get('storage', 'hostname')
        port = config.get('storage', 'port')
        database = config.get('sense', 'database')
        pool = redis.ConnectionPool(host=hostname, port=port, db=database)
        self.storage = redis.Redis(connection_pool=pool)
        self.pubsub = self.storage.pubsub(ignore_subscribe_messages=True)

SMemoryStorageManagerInstance = SMemoryStorageManager()
SMemoryStorage = SMemoryStorageManagerInstance.storage
SMemoryPubSub = SMemoryStorageManagerInstance.pubsub


class SMemoryEntry:

    def __init__(self, name, priority, expiry, payload):
        self.name = name
        self.priority = priority
        self.expiry = expiry
        self.payload = payload

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented


class SMemoryQueueManager:

    def __init__(self):
        self.queue = asyncio.PriorityQueue()
        self.queueThread = None

    async def start(self, callback):
        while True:
            entry = await self.queue.get()
            logger.debug('GOT ENTRY')
            await self.processEntry(entry, callback)
            logger.debug('DONE WITH ENTRY')
            self.queue.task_done()

    async def processEntry(self, entry, callback):
        logger.debug('PROCESSINF ENTRY')
        logger.debug(str(entry))
        await callback(entry)
        #self.queueThread = Thread(target=self.processEntry, args=(self.entry, callback), daemon=True)
        #self.queueThread.start()
        #self.queue.join()

    def stop(self):
        self.thread._stop()

    def flush(self):
        self.queue.empty()

    def put(self, name, priority, expiry, payload):
        self.queue.put(SMemoryEntry(name, priority, expiry, payload))

    def get(self):
        return self.queue.get()

SMemoryQueue = SMemoryQueueManager()
