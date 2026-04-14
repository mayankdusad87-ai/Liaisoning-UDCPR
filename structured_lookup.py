import json

class StructuredLookup:

    def __init__(self):
        with open("data/structured_rules.json", "r") as f:
            self.rules = json.load(f)

    def get_fsi(self, zone, road_width):
        zone = zone.lower()

        if zone not in self.rules["fsi"]:
            return None

        zone_rules = self.rules["fsi"][zone]

        available = sorted(
            [int(k) for k in zone_rules.keys()]
        )

        closest = max(
            [r for r in available if r <= road_width],
            default=available[0]
        )

        return zone_rules[str(closest)]

    def get_setback(self, height):
        if height <= 15:
            return self.rules["setbacks"]["up_to_15m"]
        return self.rules["setbacks"]["above_15m"]
