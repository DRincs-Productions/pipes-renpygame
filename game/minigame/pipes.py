from enum import Enum


class RotatedEnum(Enum):
    ZERO = 0
    NINETY = 1
    ONE_EIGHTY = 2
    TWO_SEVENTY = 3


class Way:
    image = None
    image_water = None
    image_source = None
    image_receiver = None
    image_water = None

    def __init__(
        self,
        image: str,
        up: bool,
        down: bool,
        right: bool,
        left: bool,
        is_source: bool = False,
        is_receiver: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        self._up = up
        self._down = down
        self._right = right
        self._left = left
        self.is_source = is_source
        self.is_receiver = is_receiver
        self.position = rotate
        self.image = image
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
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        super().__init__(
            "Four_Way",
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
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        super().__init__(
            "Three_Way",
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
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        super().__init__(
            "Two_Way",
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
        is_source: bool = False,
        rotate: RotatedEnum = RotatedEnum.ZERO,
    ):
        super().__init__(
            "One_Way",
            True,
            False,
            False,
            False,
            is_source,
            False,
            rotate,
        )


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
