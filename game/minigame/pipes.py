from enum import Enum
import random
from typing import Union
import pythonpackages.renpygame as pygame
from pythonpackages.renpygame.event import EventType

game_screen_size: tuple[int, int] = (0, 0)
game_margin = 0


class RotatedEnum(Enum):
    ZERO = 0
    NINETY = 1
    ONE_EIGHTY = 2
    TWO_SEVENTY = 3


class PuzzleEnum(Enum):
    OneWay = 10
    OneWaySource = 11
    TwoWay = 20
    TwoWaySource = 21
    ThreeWay = 30
    ThreeWaySource = 31
    FourWay = 40
    FourWaySource = 41


class Way(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.Surface,
        image_water: pygame.Surface,
        containers: list[
            Union[
                pygame.sprite.AbstractGroup,
                pygame.sprite.Group,
                pygame.sprite.RenderUpdates,
                pygame.sprite.GroupSingle,
            ]
        ],
        up: bool,
        down: bool,
        right: bool,
        left: bool,
        is_source: bool = False,
        is_receiver: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        self.image = image
        self.image_water = image_water

        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = self.image.get_rect()

        self._up = up
        self._down = down
        self._right = right
        self._left = left
        self.is_source = is_source
        self.is_receiver = is_receiver
        self.position = rotate
        self.have_water = False

    @property
    def up(self):
        if self.position == RotatedEnum.ZERO:
            return self._up
        elif self.position == RotatedEnum.NINETY:
            return self._right
        elif self.position == RotatedEnum.ONE_EIGHTY:
            return self._down
        elif self.position == RotatedEnum.TWO_SEVENTY:
            return self._left

    @property
    def down(self):
        if self.position == RotatedEnum.ZERO:
            return self._down
        elif self.position == RotatedEnum.NINETY:
            return self._left
        elif self.position == RotatedEnum.ONE_EIGHTY:
            return self._up
        elif self.position == RotatedEnum.TWO_SEVENTY:
            return self._right

    @property
    def right(self):
        if self.position == RotatedEnum.ZERO:
            return self._right
        elif self.position == RotatedEnum.NINETY:
            return self._down
        elif self.position == RotatedEnum.ONE_EIGHTY:
            return self._left
        elif self.position == RotatedEnum.TWO_SEVENTY:
            return self._up

    @property
    def left(self):
        if self.position == RotatedEnum.ZERO:
            return self._left
        elif self.position == RotatedEnum.NINETY:
            return self._up
        elif self.position == RotatedEnum.ONE_EIGHTY:
            return self._right
        elif self.position == RotatedEnum.TWO_SEVENTY:
            return self._down

    def rotate(self):
        if self.position == RotatedEnum.ZERO:
            self.position = RotatedEnum.NINETY
        elif self.position == RotatedEnum.NINETY:
            self.position = RotatedEnum.ONE_EIGHTY
        elif self.position == RotatedEnum.ONE_EIGHTY:
            self.position = RotatedEnum.TWO_SEVENTY


class FourWay(Way):
    def __init__(
        self,
        containers: list[
            Union[
                pygame.sprite.AbstractGroup,
                pygame.sprite.Group,
                pygame.sprite.RenderUpdates,
                pygame.sprite.GroupSingle,
            ]
        ],
        st: float,
        at: float,
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        if is_source:
            image = pygame.image.load("Four_Way_Source_Node.webp").convert(st, at)
            image_water = image
        else:
            image = pygame.image.load("Four_Way_Tube_Without_Water.webp").convert(
                st, at
            )
            image_water = pygame.image.load("Four_Way_Tube_With_Water.webp").convert(
                st, at
            )
        super().__init__(
            image,
            image_water,
            containers,
            True,
            True,
            True,
            True,
            is_source,
            False,
            rotate,
        )


class ThreeWay(Way):
    def __init__(
        self,
        containers: list[
            Union[
                pygame.sprite.AbstractGroup,
                pygame.sprite.Group,
                pygame.sprite.RenderUpdates,
                pygame.sprite.GroupSingle,
            ]
        ],
        st: float,
        at: float,
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        if is_source:
            image = pygame.image.load("Three_Way_Source_Node.webp").convert(st, at)
            image_water = image
        else:
            image = pygame.image.load("Three_Way_Tube_Without_Water.webp").convert(
                st, at
            )
            image_water = pygame.image.load("Three_Way_Tube_With_Water.webp").convert(
                st, at
            )
        super().__init__(
            image,
            image_water,
            containers,
            True,
            True,
            True,
            False,
            is_source,
            False,
            rotate,
        )


class TwoWay(Way):
    def __init__(
        self,
        containers: list[
            Union[
                pygame.sprite.AbstractGroup,
                pygame.sprite.Group,
                pygame.sprite.RenderUpdates,
                pygame.sprite.GroupSingle,
            ]
        ],
        st: float,
        at: float,
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        if is_source:
            image = pygame.image.load("Two_Way_Source_Node.webp").convert(st, at)
            image_water = image
        else:
            image = pygame.image.load("Two_Way_Tube_Without_Water.webp").convert(st, at)
            image_water = pygame.image.load("Two_Way_Tube_With_Water.webp").convert(
                st, at
            )
        super().__init__(
            image,
            image_water,
            containers,
            True,
            True,
            False,
            False,
            is_source,
            False,
            rotate,
        )


class OneWay(Way):
    def __init__(
        self,
        containers: list[
            Union[
                pygame.sprite.AbstractGroup,
                pygame.sprite.Group,
                pygame.sprite.RenderUpdates,
                pygame.sprite.GroupSingle,
            ]
        ],
        st: float,
        at: float,
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        if is_source:
            image = pygame.image.load("One_Way_Source_Node.webp").convert(st, at)
            image_water = image
        else:
            image = pygame.image.load("Receiver_Node_With_Water.webp").convert(st, at)
            image_water = pygame.image.load("Receiver_Node_Without_Water.webp").convert(
                st, at
            )
        super().__init__(
            image,
            image_water,
            containers,
            True,
            False,
            False,
            False,
            is_source,
            not is_source,
            rotate,
        )


class SharedData:
    def __init__(self):
        self.all = None


first_puzzle = [
    [
        PuzzleEnum.OneWay,
        PuzzleEnum.ThreeWay,
        PuzzleEnum.FourWay,
        PuzzleEnum.ThreeWay,
    ],
    [
        PuzzleEnum.FourWay,
        PuzzleEnum.TwoWay,
        PuzzleEnum.OneWay,
        PuzzleEnum.FourWay,
    ],
    [
        PuzzleEnum.TwoWaySource,
        PuzzleEnum.FourWaySource,
        PuzzleEnum.FourWaySource,
        PuzzleEnum.ThreeWaySource,
    ],
    [
        PuzzleEnum.FourWay,
        PuzzleEnum.OneWay,
        PuzzleEnum.OneWaySource,
        PuzzleEnum.FourWay,
    ],
    [
        PuzzleEnum.ThreeWay,
        PuzzleEnum.FourWaySource,
        PuzzleEnum.OneWaySource,
        PuzzleEnum.ThreeWaySource,
    ],
]


def convert_puzzle(
    puzzle: list[list[PuzzleEnum]],
    containers: list[
        Union[
            pygame.sprite.AbstractGroup,
            pygame.sprite.Group,
            pygame.sprite.RenderUpdates,
            pygame.sprite.GroupSingle,
        ]
    ],
    st: float,
    at: float,
) -> list[list[Way]]:
    res: list[list[Way]] = []
    for i in range(len(puzzle)):
        res.append([])
        for j in range(len(puzzle[i])):
            rotate = random.choice(
                [
                    RotatedEnum.ZERO,
                    RotatedEnum.NINETY,
                    RotatedEnum.TWO_SEVENTY,
                    RotatedEnum.ONE_EIGHTY,
                ]
            )
            if puzzle[i][j] == PuzzleEnum.OneWay:
                res[i].append(OneWay(containers, st, at, False, rotate))
            elif puzzle[i][j] == PuzzleEnum.OneWaySource:
                res[i].append(OneWay(containers, st, at, True, rotate))
            elif puzzle[i][j] == PuzzleEnum.TwoWay:
                res[i].append(TwoWay(containers, st, at, False, rotate))
            elif puzzle[i][j] == PuzzleEnum.TwoWaySource:
                res[i].append(TwoWay(containers, st, at, True, rotate))
            elif puzzle[i][j] == PuzzleEnum.ThreeWay:
                res[i].append(ThreeWay(containers, st, at, False, rotate))
            elif puzzle[i][j] == PuzzleEnum.ThreeWaySource:
                res[i].append(ThreeWay(containers, st, at, True, rotate))
            elif puzzle[i][j] == PuzzleEnum.FourWay:
                res[i].append(FourWay(containers, st, at, False, rotate))
            elif puzzle[i][j] == PuzzleEnum.FourWaySource:
                res[i].append(FourWay(containers, st, at, True, rotate))
    return res


def findSource(matrix: list[list[Way]]) -> list[tuple[int, int]]:
    sources = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j].is_source:
                sources.append((i, j))
    return sources


def check_connections(
    matrix: list[list[Way]], sources: list[tuple[int, int]]
) -> list[list[bool]]:
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for source in sources:
        visited[source[0]][source[1]] = True
        check_connections_helper(matrix, source[0], source[1], visited)
    return visited


def check_connections_helper(
    matrix: list[list[Way]], i: int, j: int, visited: list[list[bool]]
) -> None:
    if matrix[i][j].up and not visited[i - 1][j]:
        visited[i - 1][j] = True
        check_connections_helper(matrix, i - 1, j, visited)
    if matrix[i][j].down and not visited[i + 1][j]:
        visited[i + 1][j] = True
        check_connections_helper(matrix, i + 1, j, visited)
    if matrix[i][j].left and not visited[i][j - 1]:
        visited[i][j - 1] = True
        check_connections_helper(matrix, i, j - 1, visited)
    if matrix[i][j].right and not visited[i][j + 1]:
        visited[i][j + 1] = True
        check_connections_helper(matrix, i, j + 1, visited)


def main(size: tuple[int, int], margin=0):
    global game_screen_size
    game_screen_size = size
    global game_margin
    game_margin = margin
    # # Initialize a shared data
    global sh

    if not sh:
        sh = SharedData()

    # Initialize a game
    displayable_with_logic = pygame.RenpyGameByEvent(
        render_lambda=my_game_first_step,
        event_lambda=game_event,
    )
    # show and start the game
    displayable_with_logic.show()

    # * after show() the game will be running when the game is over

    # clean up the shared data
    sh = None
    # return to renpy
    return


def my_game_first_step(width: int, height: int, st: float, at: float) -> pygame.Surface:
    bestdepth = pygame.display.mode_ok((0, 0), 0, 32)
    screen = pygame.display.set_mode((0, 0), 0, bestdepth)

    return screen


def game_event(ev: EventType, x: int, y: int, st: float):
    # TODO https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
    return
