# Abstract Skill

from time import time
from .brain.smemory import SMemoryStorage, SMemoryQueue


class Skill:

    NAMESPACE = 'skill'

    @staticmethod
    def id(uid):
        return __class__.NAMESPACE + '.' + uid

    @staticmethod
    def payload():
        return []

    @staticmethod
    def message(action, params={}, sleep=0):
        return {
            'action': action,
            'sleep': sleep,
            'params': params
        }

    @staticmethod
    def enqueue(child, payload=[]):
        SMemoryQueue.put(child.__name__, child.PRIORITY, (time() + child.EXPIRATION), payload)

    @staticmethod
    def handle_failure(action, params):
        return False

    @staticmethod
    def handle_success(action, params):
        return True

    @staticmethod
    def get(uid):
        return SMemoryStorage.get(__class__.id(uid))

    @staticmethod
    def set(uid, value):
        SMemoryStorage.set(__class__.id(uid), value)