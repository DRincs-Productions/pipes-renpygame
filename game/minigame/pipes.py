from enum import Enum
from typing import Union
import pythonpackages.renpygame as pygame
from pythonpackages.renpygame.event import EventType


class RotatedEnum(Enum):
    ZERO = 0
    NINETY = 1
    ONE_EIGHTY = 2
    TWO_SEVENTY = 3


class Way(pygame.sprite.Sprite):
    image: pygame.Surface
    image_water = None
    image_source = None
    image_receiver = None
    image_water = None

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
        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = self.image.get_rect()
        self._up = up
        self._down = down
        self._right = right
        self._left = left
        self.is_source = is_source
        self.is_receiver = is_receiver
        self.position = rotate
        self.image = image
        self.image_water = image_water
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
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        image = pygame.image.load("Straight_Tube_With_Water.webp").convert(st, at)
        image_water = pygame.image.load("Straight_Tube_Without_Water.webp").convert(
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
            False,
            True,
            rotate,
        )


class SharedData:
    def __init__(self):
        self.all = None


a = [
    [OneWay(), TwoWay(), ThreeWay(), FourWay()],
    [OneWay(), TwoWay(), ThreeWay(), FourWay()],
    [OneWay(), TwoWay(), ThreeWay(), FourWay()],
    [OneWay(), TwoWay(), ThreeWay(), FourWay()],
    [OneWay(), TwoWay(), ThreeWay(), FourWay()],
]


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


def main():
    # # Initialize a shared data
    global sh

    if not sh:
        sh = SharedData()

    # Initialize a game
    displayable_with_logic = pygame.RenpyGameByEvent(
        render_lambda=my_game_first_step,
        event_lambda=game_event,
    )
    # show amd start the game
    displayable_with_logic.show()

    # * after show() the game will be running when the game is over

    # clean up the shared data
    score = sh.score
    sh = None
    # return to renpy
    return score


def my_game_first_step(width: int, height: int, st: float, at: float) -> pygame.Surface:
    bestdepth = pygame.display.mode_ok((0, 0), 0, 32)
    screen = pygame.display.set_mode((0, 0), 0, bestdepth)

    return screen


def game_event(ev: EventType, x: int, y: int, st: float):
    # TODO https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
    return
