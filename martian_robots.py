class Robot:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.lost = False


class MarsWorld:
    LEFT = {"N": "W", "W": "S", "S": "E", "E": "N"}
    RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}
    MOVE = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.scents = set()

    def is_outside(self, x, y):
        return x < 0 or y < 0 or x > self.max_x or y > self.max_y

    def run(self, robot, instructions):
        for command in instructions:
            if robot.lost:
                break

            if command == "L":
                robot.direction = self.LEFT[robot.direction]

            elif command == "R":
                robot.direction = self.RIGHT[robot.direction]

            elif command == "F":
                self.move(robot)

    def move(self, robot):
        dx, dy = self.MOVE[robot.direction]
        next_x = robot.x + dx
        next_y = robot.y + dy

        if self.is_outside(next_x, next_y):
            scent = (robot.x, robot.y, robot.direction)

            if scent in self.scents:
                return

            self.scents.add(scent)
            robot.lost = True
            return

        robot.x = next_x
        robot.y = next_y


def solve(input_text):
    lines = [line.strip() for line in input_text.splitlines() if line.strip()]
    max_x, max_y = map(int, lines[0].split())

    world = MarsWorld(max_x, max_y)
    results = []

    i = 1
    while i < len(lines):
        x, y, direction = lines[i].split()
        instructions = lines[i + 1]

        robot = Robot(int(x), int(y), direction)
        world.run(robot, instructions)

        result = f"{robot.x} {robot.y} {robot.direction}"
        if robot.lost:
            result += " LOST"

        results.append(result)
        i += 2

    return "\n".join(results)
