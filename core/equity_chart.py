class EquityCurveASCII:
    def __init__(self, width=50, height=10):
        self.width = width
        self.height = height
        self.values = []

    def update(self, balance):
        self.values.append(balance)
        return self.render()

    def render(self):
        if len(self.values) < 2:
            return "(waiting for data...)"

        # Normalize values to fit chart height
        min_v = min(self.values)
        max_v = max(self.values)
        span = max_v - min_v if max_v != min_v else 1

        scaled = [
            int((v - min_v) / span * (self.height - 1))
            for v in self.values[-self.width:]
        ]

        # Build grid
        grid = [[" " for _ in range(len(scaled))] for _ in range(self.height)]

        for i, y in enumerate(scaled):
            grid[self.height - 1 - y][i] = "█"

        # Convert to lines
        lines = ["".join(row) for row in grid]
        return "\n".join(lines)
