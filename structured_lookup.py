import json


class StructuredLookup:

    def __init__(self):
        with open("data/structured_rules.json") as f:
            self.rules = json.load(f)

    def get_fsi(self):
        return self.rules["fsi"]

    def get_parking(self):
        return self.rules["parking"]

    def get_setback(self):
        return self.rules["setbacks"]

    def get_approvals(self):
        return self.rules["approvals"]
