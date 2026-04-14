import json


class StructuredLookup:

    def __init__(self):
        with open("data/structured_rules.json", "r") as f:
            self.rules = json.load(f)

    def get_fsi(self, zone, road_width, scheme="general_udcpr"):
        zone = zone.lower()
        scheme = scheme.lower()

        # scheme-based direct FSI
        if scheme in ["sra", "mhada", "pmay"]:
            return self.rules[scheme]["base_fsi"]

        # general UDCPR lookup
        fsi_rules = self.rules["general_udcpr"]["fsi"]

        if zone not in fsi_rules:
            return None

        zone_data = fsi_rules[zone]

        available_roads = sorted(
            [int(k) for k in zone_data.keys()]
        )

        closest = max(
            [r for r in available_roads if r <= road_width],
            default=available_roads[0]
        )

        return zone_data[str(closest)]

    def get_setback(self, height):
        if height <= 10:
            return {
                "front": 3,
                "side": 1.5,
                "rear": 2
            }

        return {
            "front": 4.5,
            "side": 2,
            "rear": 3
        }
