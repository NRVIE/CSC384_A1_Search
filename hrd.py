"""CSC384-Assignment 1"""

"Structure that stores a state of the puzzle"

from ast import main
from asyncio.windows_events import NULL
from heapq import heappush


class State:
    """
    This class record a state of puzzle in lists.

    Attributes:
    map: A dictionary stores the position of each space (treat it as coordinates) as key and
    the cooresponding value of each key is a tuple.
    In the tuple, we store the type of piece (3 repesents vertical, 2 represents horizontal,
    4 represents singular, 1 represents 2by2, or 0 represents empty) as int, and
    store the other spaces that piece covered store as a list of tuple.
    NOTE: Domain of coordinates: {(x, y)| 0 <= x <= 3, 0 <= y <= 4}.

    Example: # TODO: Write an example here.

    coordinate of each piece, type of each piece(vertical, horizontal, singular, or 2by2),


    NOTE: The list of each row of puzzle can only included integer greater or equal to 0, and less
    or equal to 4!

    Method:
    - move_up(position: tuple):
        Move the piece on the position up (assume the piece we moved is a empty space).
    - move_down(position: tuple):
        Similar to above
    - move_left(position: tuple):
        Similar to above
    - move_right(position: tuple):
        Similar to above
    - display():
        print the state information (where is each piece at) as "matrix-like" form to console.

    """
    map: dict[tuple, tuple[int, list[tuple]]]

    def __init__(self) -> None:

        self.map = {(0, 0): (3, []), (1, 0): (1, [(1, 1), (2, 0), (2, 1)]),
                    (2, 0): (1, [(1, 0), (1, 1), (2, 1)]), (3, 0): (3, []),
                    (0, 1): (3, []), (1, 1): (1, [(1, 0), (2, 0), (2, 1)]),
                    (2, 1): (1, [(1, 0), (1, 1), (2, 0), (2, 1)]), (3, 1): (3, []),
                    (0, 2): (3, []), (1, 2): (0, []), (2, 2): (0, []), (3, 2): (3, []),
                    (0, 3): (3, []), (1, 3): (4, []), (2, 3): (4, []), (3, 3): (3, []),
                    (0, 4): (4, []), (1, 4): (2, []), (2, 4): (2, []), (3, 4): (4, []), }

    def __str__(self) -> str:
        result = ""
        for y in range(5):
            for x in range(4):
                result += f"{self.map[(x, y)][0]} "
            result += "\n"
        return result

    def move_up(self, position: tuple) -> None:
        """
        Move the piece on the position up (assume the piece we moved is a empty space).
        - We need to check what kind of piece above the position:
            - if is vertical, the empty space we moved move up 2 units.
            - if is horizontal, there should be another empty space adjacent to
            the empty space at position
            (we could figure out another empty space should be on the left
            or right of the current empty space by checking the dictionary of the piece above).
            - if is singular/singular, then just swap the empty space at position to the target.
        """
        x = position[0]  # x-axis value for the coordinate above the position
        if self.map[position][0] != 0:
            print("Please move empty space.")
            return
        if position[1] > 0:
            y = position[1] - 1  # y-axis value for the coordinate above the position
        else:
            print("Error: out of range")
            return

        # Check what kind of piece upward the position
        if self.map[(x, y)][0] == 1:
            # Check the adjacent space of position to know the area the piece covered and
            # check is there has enough empty space to move
            if x > 0 and self.map[(x - 1, y)][0] == 1 and self.map[(x - 1, y + 1)][0] == 0:
                # move empty spaces up
                self.map[position] = self.map[(x, y)]
                self.map[(x - 1, y + 1)] = self.map[(x - 1, y)]
                self.map[(x, y)] = self.map[(x, y - 1)]
                self.map[(x - 1, y)] = self.map[(x - 1, y - 1)]

                # update the corrdinates of neighbours
                for p in [(x - 1, y), (x, y), (x - 1, y + 1), (x, y + 1)]:
                    new_neighbour = []
                    for t in self.map[p][1]:
                        new_neighbour.append((t[0], t[1] + 1))
                    self.map[p] = (self.map[p][0], new_neighbour)

                # move empty space up
                self.map[(x, y - 1)] = (0, [])
                self.map[(x - 1, y - 1)] = (0, [])

            elif x < 3 and self.map[(x + 1, y)][0] == 1 and self.map[(x + 1, y + 1)][0] == 0:
                # move 2x2 spaces down
                self.map[position] = self.map[(x, y)]
                self.map[(x + 1, y + 1)] = self.map[(x + 1, y)]
                self.map[(x, y)] = self.map[(x, y - 1)]
                self.map[(x + 1, y)] = self.map[(x + 1, y - 1)]

                # update the corrdinates of neighbours
                for p in [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]:
                    new_neighbour = []
                    for t in self.map[p][1]:
                        new_neighbour.append((t[0], t[1] + 1))
                    self.map[p] = (self.map[p][0], new_neighbour)

                # move empty space up
                self.map[(x, y - 1)] = (0, [])
                self.map[(x + 1, y - 1)] = (0, [])

        elif self.map[(x, y)][0] == 2:
            # Check the position of neighbour and space below the neighbour
            neighbour = self.map[(x, y)][1][0]
            assert self.map[neighbour][0] == 2

            if self.map[(neighbour[0], neighbour[1] + 1)][0] == 0:
                # Move 1x2 down and empty space up
                ...
        elif self.map[(x, y)][0] == 3:
            ...
        elif self.map[(x, y)][0] == 4:
            ...
        else:
            # It is zero as well above, then do nothing
            return

    def move_down() -> None:
        """
        Move the piece on the position down (assume the piece we moved is a empty space).
            - Constraints are same as move_up()
        """

    def move_left() -> None:
        """
        Move the piece on the position down (assume the piece we moved is a empty space).
            - Constraints are same as move_up()
        """

    def move_right() -> None:
        """
        Move the piece on the position down (assume the piece we moved is a empty space).
            - Constraints are same as move_up()
        """

    def print() -> None:
        """
        print the state information (where is each piece at) as "matrix-like" form to console.

        Example:
        initial state:
        3113
        3113
        3223
        3443
        4004
        """


def txt_to_state() -> State:
    """Return a State that convert input form to output form"""
    ...


if __name__ == "__main__":
    s = State()
    print(s)
    s.move_up((2, 2))
    print(s)
