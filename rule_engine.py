import json


class RuleEngine:

    def __init__(self):
        with open("data/structured_rules.json") as f:
            self.rules = json.load(f)

    # -----------------------------------
    # GET SCHEME DATA
    # -----------------------------------
    def get_scheme(self, scheme):
        return self.rules["schemes"].get(scheme, self.rules["schemes"]["33A10"])

    # -----------------------------------
    # FSI CALCULATION
    # -----------------------------------
    def calculate_fsi(self, plot_area, scheme):

        scheme_data = self.get_scheme(scheme)

        base = scheme_data["fsi"]["base"]
        fungible = base * (scheme_data["fsi"]["fungible_percent"] / 100)

        total = base + fungible
        bua = plot_area * total

        return {
            "base": base,
            "fungible": round(fungible, 2),
            "total": round(total, 2),
            "bua": round(bua, 2)
        }

    # -----------------------------------
    # PARKING CALCULATION
    # -----------------------------------
    def calculate_parking(self, bua, scheme):

        scheme_data = self.get_scheme(scheme)

        ecs_rate = scheme_data["parking"]["residential"]["ecs_per_sqm"]

        ecs = bua * ecs_rate

        return {
            "ecs": round(ecs),
            "visitor": round(ecs * 0.1),
            "total": round(ecs * 1.1)
        }

    # -----------------------------------
    # APPROVAL CHECK
    # -----------------------------------
    def check_approvals(self, height, scheme):

        scheme_data = self.get_scheme(scheme)

        approvals = []

        if height > scheme_data["height_rules"]["fire_noc"]:
            approvals.append("Fire NOC required")

        if height > scheme_data["height_rules"]["high_rise"]:
            approvals.append("High-rise compliance required")

        approvals.append("Local authority approval")

        return approvals
