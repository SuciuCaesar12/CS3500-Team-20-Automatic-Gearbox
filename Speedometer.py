class Speedometer:
    def __init__(self):
        self.speed = 0

    def calculate_speed(self, bus, gear, rpm):
        self.speed = (gear * 2 * rpm) / 100
        bus["speed"] = self.speed
        return bus