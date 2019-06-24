#!/usr/bin/python

class BaseModule:
    def __init__(self):
        pass

    def add_args(self, parser):
        raise NotImplementedError("Subclass to implement add_args()")

    def action(self, args):
        raise NotImplementedError("Subclass to implement action()")
