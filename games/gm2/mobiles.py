import sys
import os


class Character:
    def __init__(self, name):
        self.name=name
        self.strength = 10
        self.health = 10
        self.inventory = {}

    def strike(self, source):
        self.health = self.health - 1



class action:
    def __init__(self, type:str, source:Character, target:Character):
        self.type = type
        self.source = source
        self.target = target
        self.type = "strike"


class action_queue:
    def __init__(self):
        self.q = []

