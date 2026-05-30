from dataclasses import dataclass


LEFT_TURN = {
    "N": "W",
    "W": "S",
    "S": "E",
    "E": "N",
}

RIGHT_TURN = {
    "N": "E",
    "E": "S",
    "S": "W",
    "W": "N",
}

MOVE_FORWARD = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


@dataclass
class Robot:
    x: int
    y: int
    orientation: str
    lost: bool = False


class MarsWorld:
    def __init__(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y
        self.scents = set()

    def is_off_grid(self, x: int, y: int) -> bool:
        return x < 0 or y < 0 or x > self.max_x or y > self.max_y

    def execute(self, robot: Robot, instructions: str) -> Robot:
        command_handlers = {
            "L": self.turn_left,
            "R": self.turn_right,
            "F": self.move_forward,
        }

        for command in instructions.strip():
            if robot.lost:
                break
            handler = command_handlers.get(command)
            if handler:
                handler(robot)

        return robot

    def turn_left(self, robot: Robot) -> None:
        robot.orientation = LEFT_TURN[robot.orientation]

    def turn_right(self, robot: Robot) -> None:
        robot.orientation = RIGHT_TURN[robot.orientation]

    def move_forward(self, robot: Robot) -> None:
        dx, dy = MOVE_FORWARD[robot.orientation]
        next_x = robot.x + dx
        next_y = robot.y + dy

        if self.is_off_grid(next_x, next_y):
            scent_key = (robot.x, robot.y, robot.orientation)
            if scent_key in self.scents:
                return
            self.scents.add(scent_key)
            robot.lost = True
            return

        robot.x = next_x
        robot.y = next_y
