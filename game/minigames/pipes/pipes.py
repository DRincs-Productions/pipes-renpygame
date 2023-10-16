from enum import Enum
import random
from typing import Callable, Optional, Union
import pythonpackages.renpygame as pygame
from pythonpackages.renpygame.event import EventType
import renpy.exports as renpy

from pythonpackages.renpygame.image import Image

CHECK_CONNECTIONS_EVENT = 423536456
SEND_WATER_EVENT = 365685678
UPDATE_IMAGE = 893457893457
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
        image_without_water: Image,
        image_water: Image,
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
        self.image_without_water = image_without_water
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

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def rotate(self):
        if self.is_receiver:
            return
        if self.rotate_position == RotatedEnum.ZERO:
            self.rotate_position = RotatedEnum.NINETY
        elif self.rotate_position == RotatedEnum.NINETY:
            self.rotate_position = RotatedEnum.ONE_EIGHTY
        elif self.rotate_position == RotatedEnum.ONE_EIGHTY:
            self.rotate_position = RotatedEnum.TWO_SEVENTY
        elif self.rotate_position == RotatedEnum.TWO_SEVENTY:
            self.rotate_position = RotatedEnum.ZERO

    def update(
        self, ev: EventType, x: int, y: int, st: Optional[float], at: Optional[float]
    ):
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
        elif ev.type == UPDATE_IMAGE:
            if st is not None and at is not None:
                self.update_image(st, at)
            else:
                print("ERROR: st or at is None")
        super().update()

    def update_image(self, st: float, at: float):
        # * INFO: self.image is a special variable in pygame.sprite.Sprite
        if self.have_water:
            pre_image = self.image_water
        else:
            pre_image = self.image_without_water

        if self.rotate_position == RotatedEnum.ZERO:
            # * I rotate the image for 1 degree because if I rotate it for 0
            pre_image = pygame.transform.rotate(pre_image, 1)
        elif self.rotate_position == RotatedEnum.NINETY:
            pre_image = pygame.transform.rotate(pre_image, 90)
        elif self.rotate_position == RotatedEnum.ONE_EIGHTY:
            pre_image = pygame.transform.rotate(pre_image, 180)
        elif self.rotate_position == RotatedEnum.TWO_SEVENTY:
            pre_image = pygame.transform.rotate(pre_image, 270)

        self.image = pre_image.convert(st, at)
        self.rect = self.image.get_rect()
        x_rectangle, y_rectangle = self.rect.get_size()
        # * I don't know why but when I rotate the image -> the x and y are changed, so need -70
        self.rect.left = self.x * (x_rectangle + game_margin) - 70
        self.rect.top = self.y * (y_rectangle + game_margin) - 70


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
            image = pygame.image.load("Four_Way_Source_Node.webp")
            image_water = image
        else:
            image = pygame.image.load("Four_Way_Tube_Without_Water.webp")
            image_water = pygame.image.load("Four_Way_Tube_With_Water.webp")
        super().__init__(
            image_without_water=image,
            image_water=image_water,
            containers=containers,
            up=True,
            down=True,
            right=True,
            left=True,
            position=position,
            st=st,
            at=at,
            is_source=is_source,
            is_receiver=False,
            rotate=rotate,
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
            image = pygame.image.load("Three_Way_Source_Node.webp")
            image_water = image
        else:
            image = pygame.image.load("Three_Way_Tube_Without_Water.webp")
            image_water = pygame.image.load("Three_Way_Tube_With_Water.webp")
        super().__init__(
            image_without_water=image,
            image_water=image_water,
            containers=containers,
            up=True,
            down=True,
            right=True,
            left=False,
            position=position,
            st=st,
            at=at,
            is_source=is_source,
            is_receiver=False,
            rotate=rotate,
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
            image = pygame.image.load("Two_Way_Source_Node.webp")
            image_water = image
        else:
            image = pygame.image.load("Two_Way_Tube_Without_Water.webp")
            image_water = pygame.image.load("Two_Way_Tube_With_Water.webp")
        super().__init__(
            image_without_water=image,
            image_water=image_water,
            containers=containers,
            up=True,
            down=False,
            right=True,
            left=False,
            position=position,
            st=st,
            at=at,
            is_source=is_source,
            is_receiver=False,
            rotate=rotate,
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
            image = pygame.image.load("One_Way_Source_Node.webp")
            image_water = image
        else:
            image = pygame.image.load("Receiver_Node_Without_Water.webp")
            image_water = pygame.image.load("Receiver_Node_With_Water.webp")
        super().__init__(
            image_without_water=image,
            image_water=image_water,
            containers=containers,
            up=True,
            down=False,
            right=False,
            left=False,
            position=position,
            st=st,
            at=at,
            is_source=is_source,
            is_receiver=not is_source,
            rotate=rotate,
        )


class SharedData:
    def __init__(self):
        self.all = pygame.sprite.RenderUpdates()
        self.matrix: list[list[Way]] = []
        self.source_list: list[tuple[int, int]] = []


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
    """Convert a puzzle to a matrix of Way"""
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
    """
    Return a matrix of visited nodes.
    source: is water source
    """
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


def send_have_water_event():
    visited = check_connections(sh.matrix, sh.source_list)
    myevent = pygame.event.Event(SEND_WATER_EVENT, visited=visited)
    pygame.event.post(myevent)


def my_game_first_step(width: int, height: int, st: float, at: float) -> pygame.Surface:
    bestdepth = pygame.display.mode_ok((0, 0), 0, 32)
    screen = pygame.display.set_mode((0, 0), 0, bestdepth)

    sh.matrix = convert_puzzle(first_puzzle, [sh.all], st, at)
    sh.source_list = findSource(sh.matrix)

    send_have_water_event()

    # draw the scene
    dirty = sh.all.draw(screen)
    pygame.display.update(dirty)

    return screen


def game_event(ev: EventType, x: int, y: int, st: float, redraw: Callable[[int], None]):
    if ev.type == pygame.MOUSEBUTTONUP:
        sh.all.update(ev, x, y, None, None)

    if ev.type == CHECK_CONNECTIONS_EVENT:
        send_have_water_event()

    if ev.type == SEND_WATER_EVENT:
        sh.all.update(ev, x, y, None, None)
        redraw(0)
    return


def redraw(
    cur_screen: pygame.Surface,
    st: float,
    at: float,
):
    myevent = pygame.event.Event(UPDATE_IMAGE)
    sh.all.update(myevent, 0, 0, st, at)
    # draw the scene
    dirty = sh.all.draw(cur_screen)
    pygame.display.update(dirty)
