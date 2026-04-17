class StructuredLookup:

    def __init__(self):
        self.base_fsi = 3.0
        self.fungible_percent = 35

    def calculate_fsi(self, plot_area):
        base = self.base_fsi
        fungible = base * (self.fungible_percent / 100)

        total = base + fungible
        bua = plot_area * total

        return {
            "base": base,
            "fungible": round(fungible, 2),
            "total": round(total, 2),
            "bua": round(bua, 2)
        }

    def parking(self, bua):
        ecs = bua / 100
        visitor = ecs * 0.05

        return {
            "ecs": round(ecs),
            "visitor": round(visitor),
            "total": round(ecs + visitor)
        }

    def approvals(self, height):
        approvals = []

        if height > 24:
            approvals.append("Fire NOC required")

        if height > 45:
            approvals.append("High-rise compliance required")

        approvals.append("Local authority approval")

        return approvals
