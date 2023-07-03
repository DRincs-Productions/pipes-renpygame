from enum import Enum
import random
from typing import Callable, Union
import pythonpackages.renpygame as pygame
from pythonpackages.renpygame.event import EventType
import renpy.exports as renpy

from pythonpackages.renpygame.image import Image

CHECK_CONNECTIONS_EVENT = 423536456
SEND_WATER_EVENT = 365685678
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
        position: tuple[int, int],
        st: float,
        at: float,
        is_source: bool = False,
        is_receiver: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        self.image = image
        self.image_water = image_water

        pygame.sprite.Sprite.__init__(self, containers)

        self._up = up
        self._down = down
        self._right = right
        self._left = left
        self.position = position
        self.is_source = is_source
        self.is_receiver = is_receiver
        self.rotate_position = rotate
        self.have_water = False

        self.update_image(st, at)

    def update(self, ev: EventType, x: int, y: int, st: float):
        if ev.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint((x, y)):
                self.rotate()
                myevent = pygame.event.Event(CHECK_CONNECTIONS_EVENT)
                pygame.event.post(myevent)
        elif ev.type == SEND_WATER_EVENT:
            if ev.visited[self.position[1]][self.position[0]]:
                self.have_water = True
            else:
                self.have_water = False
            # self.update_image()

    @property
    def up(self):
        if self.rotate_position == RotatedEnum.ZERO:
            return self._up
        elif self.rotate_position == RotatedEnum.NINETY:
            return self._right
        elif self.rotate_position == RotatedEnum.ONE_EIGHTY:
            return self._down
        elif self.rotate_position == RotatedEnum.TWO_SEVENTY:
            return self._left

    @property
    def down(self):
        if self.rotate_position == RotatedEnum.ZERO:
            return self._down
        elif self.rotate_position == RotatedEnum.NINETY:
            return self._left
        elif self.rotate_position == RotatedEnum.ONE_EIGHTY:
            return self._up
        elif self.rotate_position == RotatedEnum.TWO_SEVENTY:
            return self._right

    @property
    def right(self):
        if self.rotate_position == RotatedEnum.ZERO:
            return self._right
        elif self.rotate_position == RotatedEnum.NINETY:
            return self._down
        elif self.rotate_position == RotatedEnum.ONE_EIGHTY:
            return self._left
        elif self.rotate_position == RotatedEnum.TWO_SEVENTY:
            return self._up

    @property
    def left(self):
        if self.rotate_position == RotatedEnum.ZERO:
            return self._left
        elif self.rotate_position == RotatedEnum.NINETY:
            return self._up
        elif self.rotate_position == RotatedEnum.ONE_EIGHTY:
            return self._right
        elif self.rotate_position == RotatedEnum.TWO_SEVENTY:
            return self._down

    def rotate(self):
        if self.rotate_position == RotatedEnum.ZERO:
            self.rotate_position = RotatedEnum.NINETY
        elif self.rotate_position == RotatedEnum.NINETY:
            self.rotate_position = RotatedEnum.ONE_EIGHTY
        elif self.rotate_position == RotatedEnum.ONE_EIGHTY:
            self.rotate_position = RotatedEnum.TWO_SEVENTY

    def update_image(self, st: float, at: float):
        if self.have_water:
            self.rect = self.image.get_rect()
        else:
            self.rect = self.image_water.get_rect()
        x_rectangle, y_rectangle = self.rect.get_size()
        self.rect.left = self.position[0] * (x_rectangle + game_margin)
        self.rect.top = self.position[1] * (y_rectangle + game_margin)


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
        position: tuple[int, int],
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
            position,
            st,
            at,
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
        position: tuple[int, int],
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
            position,
            st,
            at,
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
        position: tuple[int, int],
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
            position,
            st,
            at,
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
        position: tuple[int, int],
        st: float,
        at: float,
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        if is_source:
            image = pygame.image.load("One_Way_Source_Node.webp").convert(st, at)
            image_water = image
        else:
            image = pygame.image.load("Receiver_Node_Without_Water.webp").convert(
                st, at
            )
            image_water = pygame.image.load("Receiver_Node_With_Water.webp").convert(
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
            position,
            st,
            at,
            is_source,
            not is_source,
            rotate,
        )


class SharedData:
    def __init__(self):
        self.all = pygame.sprite.RenderUpdates()
        self.matrix: list[list[Way]] = []


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
    for y in range(len(puzzle)):
        res.append([])
        for x in range(len(puzzle[y])):
            rotate = random.choice(
                [
                    RotatedEnum.ZERO,
                    RotatedEnum.NINETY,
                    RotatedEnum.TWO_SEVENTY,
                    RotatedEnum.ONE_EIGHTY,
                ]
            )
            if puzzle[y][x] == PuzzleEnum.OneWay:
                res[y].append(OneWay(containers, (x, y), st, at, False, rotate))
            elif puzzle[y][x] == PuzzleEnum.OneWaySource:
                res[y].append(OneWay(containers, (x, y), st, at, True, rotate))
            elif puzzle[y][x] == PuzzleEnum.TwoWay:
                res[y].append(TwoWay(containers, (x, y), st, at, False, rotate))
            elif puzzle[y][x] == PuzzleEnum.TwoWaySource:
                res[y].append(TwoWay(containers, (x, y), st, at, True, rotate))
            elif puzzle[y][x] == PuzzleEnum.ThreeWay:
                res[y].append(ThreeWay(containers, (x, y), st, at, False, rotate))
            elif puzzle[y][x] == PuzzleEnum.ThreeWaySource:
                res[y].append(ThreeWay(containers, (x, y), st, at, True, rotate))
            elif puzzle[y][x] == PuzzleEnum.FourWay:
                res[y].append(FourWay(containers, (x, y), st, at, False, rotate))
            elif puzzle[y][x] == PuzzleEnum.FourWaySource:
                res[y].append(FourWay(containers, (x, y), st, at, True, rotate))
    return res


def findSource(matrix: list[list[Way]]) -> list[tuple[int, int]]:
    sources = []
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x].is_source:
                sources.append((y, x))
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
    matrix: list[list[Way]], x: int, y: int, visited: list[list[bool]]
) -> None:
    matrix_min = 0
    matrix_max_x = len(matrix) - 1
    matrix_max_y = len(matrix[0]) - 1

    if x - 1 >= matrix_min and matrix[x][y].up and not visited[x - 1][y]:
        visited[x - 1][y] = True
        check_connections_helper(matrix, x - 1, y, visited)
    if x + 1 <= matrix_max_x and matrix[x][y].down and not visited[x + 1][y]:
        visited[x + 1][y] = True
        check_connections_helper(matrix, x + 1, y, visited)
    if y - 1 >= matrix_min and matrix[x][y].left and not visited[x][y - 1]:
        visited[x][y - 1] = True
        check_connections_helper(matrix, x, y - 1, visited)
    if y + 1 <= matrix_max_y and matrix[x][y].right and not visited[x][y + 1]:
        visited[x][y + 1] = True
        check_connections_helper(matrix, x, y + 1, visited)


sh = SharedData()


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
        redraw_lambda=redraw,
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

    sh.matrix = convert_puzzle(first_puzzle, [sh.all], st, at)

    # draw the scene
    dirty = sh.all.draw(screen)
    pygame.display.update(dirty)

    return screen


def game_event(ev: EventType, x: int, y: int, st: float, redraw: Callable[[int], None]):
    if ev.type == pygame.MOUSEBUTTONUP:
        sh.all.update(ev, x, y, st)

    if ev.type == CHECK_CONNECTIONS_EVENT:
        visited = check_connections(sh.matrix, findSource(sh.matrix))
        myevent = pygame.event.Event(SEND_WATER_EVENT, visited=visited)
        pygame.event.post(myevent)

    if ev.type == SEND_WATER_EVENT:
        sh.all.update(ev, x, y, st)
        redraw(0)
    return


def redraw(
    cur_screen: pygame.Surface,
    st: float,
    at: float,
):
    # draw the scene
    dirty = sh.all.draw(cur_screen)
    pygame.display.update(dirty)
