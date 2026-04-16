class StructuredLookup:

    def __init__(self):
        self.base_fsi = 3.0
        self.fungible_percent = 35

    def calculate_fsi(self, plot_area):
        base = self.base_fsi
        fungible = base * (self.fungible_percent / 100)

        total_fsi = base + fungible
        bua = plot_area * total_fsi

        return {
            "base": base,
            "fungible": fungible,
            "total": total_fsi,
            "bua": bua
        }

    def parking(self, bua):
        # simplified ECS logic
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

        approvals.append("Authority approval")

        return approvals
