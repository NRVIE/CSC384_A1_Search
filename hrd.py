"""CSC384-Assignment 1"""
from dataclasses import dataclass, field
from typing import Any

"Structure that stores a state of the puzzle"

from heapq import heappush, heappop
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

        self.map = {(0, 0): (3, [(0, 1)]), (1, 0): (1, [(1, 1), (2, 0), (2, 1)]),
                    (2, 0): (1, [(1, 0), (1, 1), (2, 1)]), (3, 0): (3, [(3, 1)]),
                    (0, 1): (3, [(0, 0)]), (1, 1): (1, [(1, 0), (2, 0), (2, 1)]),
                    (2, 1): (1, [(1, 0), (1, 1), (2, 0)]), (3, 1): (3, [(3, 0)]),
                    (0, 2): (3, [(0, 3)]), (1, 2): (2, [(2, 2)]), (2, 2): (2, [(1, 2)]),
                    (3, 2): (3, [(3, 3)]),
                    (0, 3): (3, [(0, 2)]), (1, 3): (4, []), (2, 3): (4, []), (3, 3): (3, [(3, 2)]),
                    (0, 4): (4, []), (1, 4): (0, []), (2, 4): (0, []), (3, 4): (4, [])}

    def __str__(self) -> str:
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
        result = ""
        for y in range(5):
            for x in range(4):
                result += f"{self.map[(x, y)][0]} "
            result += "\n"
        return result

    def __eq__(self, other):
        """
        Return Ture if all items in other's map are same as self's
        """
        for y in range(5):
            for x in range(4):
                if self.map[(x, y)] != other.map[(x, y)]:
                    return False

        return True

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
        # Get the coordinate of the space below position
        x = position[0]  # x-axis value for the coordinate above the position
        if self.map[position][0] != 0:
            print("Please move empty space.")
            return

        if 0 < position[1] <= 4:
            y = position[1] - 1  # y-axis value for the coordinate above the position
        else:
            # print("Error: out of range")
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
                self.map[(x, y + 1)] = (self.map[(x, y)][0], [(self.map[(x, y)][1][0][0],
                                                               self.map[(x, y)][1][0][1] + 1)])
                self.map[(neighbour[0], neighbour[1] + 1)] = (self.map[neighbour][0],
                                                              [(self.map[neighbour][1][0][0],
                                                                self.map[neighbour][1][0][1] + 1)])
                self.map[(x, y)] = (0, [])
                self.map[neighbour] = (0, [])

        elif self.map[(x, y)][0] == 3:
            neighbour = self.map[(x, y)][1][0]
            assert self.map[neighbour][0] == 3

            # Move 2x1 down and empty space up
            self.map[(x, y + 1)] = (self.map[(x, y)][0], [(self.map[(x, y)][1][0][0],
                                                           self.map[(x, y)][1][0][1] + 1)])
            self.map[(neighbour[0], neighbour[1] + 1)] = (self.map[neighbour][0],
                                                          [(self.map[neighbour][1][0][0],
                                                            self.map[neighbour][1][0][1] + 1)])
            self.map[(x, y - 1)] = (0, [])

        elif self.map[(x, y)][0] == 4:
            # Swap the singular piece with empty space
            self.map[position] = self.map[(x, y)]
            self.map[(x, y)] = (0, [])
        else:
            # It is zero as well above, then do nothing
            return

    def move_down(self, position) -> None:
        """
        Move the piece on the position down (assume the piece we moved is a empty space).
            - Constraints are same as move_up()
        """
        # Get the coordinate of the space below position
        x = position[0]  # x-axis value for the coordinate below the position
        if self.map[position][0] != 0:
            print("Please move empty space.")
            return

        if 0 <= position[1] < 4:
            y = position[1] + 1  # y-axis value for the coordinate below the position
        else:
            # print("Error: out of range")
            return

        # Check what kind of piece upward the position
        if self.map[(x, y)][0] == 1:
            # Check the adjacent space of position to know the area the piece covered and
            # check is there has enough empty space to move
            if x > 0 and self.map[(x - 1, y)][0] == 1 and self.map[(x - 1, y - 1)][0] == 0:
                # move empty spaces up
                self.map[position] = self.map[(x, y)]
                self.map[(x - 1, y - 1)] = self.map[(x - 1, y)]
                self.map[(x, y)] = self.map[(x, y + 1)]
                self.map[(x - 1, y)] = self.map[(x - 1, y + 1)]

                # update the corrdinates of neighbours
                for p in [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)]:
                    new_neighbour = []
                    for t in self.map[p][1]:
                        new_neighbour.append((t[0], t[1] - 1))
                    self.map[p] = (self.map[p][0], new_neighbour)

                # move empty space up
                self.map[(x, y + 1)] = (0, [])
                self.map[(x - 1, y + 1)] = (0, [])

            elif x < 3 and self.map[(x + 1, y)][0] == 1 and self.map[(x + 1, y - 1)][0] == 0:
                # move 2x2 spaces down
                self.map[position] = self.map[(x, y)]
                self.map[(x + 1, y - 1)] = self.map[(x + 1, y)]
                self.map[(x, y)] = self.map[(x, y + 1)]
                self.map[(x + 1, y)] = self.map[(x + 1, y + 1)]

                # update the corrdinates of neighbours
                for p in [(x, y - 1), (x + 1, y - 1), (x, y), (x + 1, y)]:
                    new_neighbour = []
                    for t in self.map[p][1]:
                        new_neighbour.append((t[0], t[1] - 1))
                    self.map[p] = (self.map[p][0], new_neighbour)

                # move empty space up
                self.map[(x, y + 1)] = (0, [])
                self.map[(x + 1, y + 1)] = (0, [])

        elif self.map[(x, y)][0] == 2:
            # Check the position of neighbour and space below the neighbour
            neighbour = self.map[(x, y)][1][0]
            assert self.map[neighbour][0] == 2

            if self.map[(neighbour[0], neighbour[1] - 1)][0] == 0:
                # Move 1x2 up and empty space down
                self.map[(x, y - 1)] = (self.map[(x, y)][0], [(self.map[(x, y)][1][0][0],
                                                               self.map[(x, y)][1][0][1] - 1)])
                self.map[(neighbour[0], neighbour[1] - 1)] = (self.map[neighbour][0],
                                                              [(self.map[neighbour][1][0][0],
                                                                self.map[neighbour][1][0][1] - 1)])
                self.map[(x, y)] = (0, [])
                self.map[neighbour] = (0, [])

        elif self.map[(x, y)][0] == 3:
            neighbour = self.map[(x, y)][1][0]
            assert self.map[neighbour][0] == 3

            # Move 2x1 up and empty space down
            self.map[(x, y - 1)] = (self.map[(x, y)][0], [(self.map[(x, y)][1][0][0],
                                                           self.map[(x, y)][1][0][1] - 1)])
            self.map[(neighbour[0], neighbour[1] - 1)] = (self.map[neighbour][0],
                                                          [(self.map[neighbour][1][0][0],
                                                            self.map[neighbour][1][0][1] - 1)])
            self.map[(x, y + 1)] = (0, [])

        elif self.map[(x, y)][0] == 4:
            # Swap the singular piece with empty space
            self.map[position] = self.map[(x, y)]
            self.map[(x, y)] = (0, [])
        else:
            # It is zero as well above, then do nothing
            return

    def move_left(self, position) -> None:
        """
        Move the piece on the position down (assume the piece we moved is a empty space).
            - Constraints are same as move_up()
        """
        # Get the coordinate of the space below position
        if self.map[position][0] != 0:
            print("Please move empty space.")
            return

        y = position[1]  # y-axis value for the coordinate on the left of the position
        if 0 < position[0] <= 3:
            x = position[0] - 1  # x-axis value for the coordinate on the left of the position
        else:
            # print("Error: out of range")
            return

        # Check what kind of piece upward the position
        if self.map[(x, y)][0] == 1:
            # Check the adjacent space of position to know the area the piece covered and
            # check is there has enough empty space to move
            if 0 < y <= 4 and self.map[(x, y - 1)][0] == 1 and self.map[(x + 1, y - 1)][0] == 0:
                # move 2x2 spaces right
                self.map[position] = self.map[(x, y)]
                self.map[(x, y)] = self.map[(x - 1, y)]
                self.map[(x + 1, y - 1)] = self.map[(x, y - 1)]
                self.map[(x, y - 1)] = self.map[(x - 1, y - 1)]

                # update the corrdinates of neighbours
                for p in [(x, y - 1), (x + 1, y - 1), (x, y), (x + 1, y)]:
                    new_neighbour = []
                    for t in self.map[p][1]:
                        new_neighbour.append((t[0] + 1, t[1]))
                    self.map[p] = (self.map[p][0], new_neighbour)

                # move empty space up
                self.map[(x - 1, y - 1)] = (0, [])
                self.map[(x - 1, y)] = (0, [])

            elif 0 <= y < 4 and self.map[(x, y + 1)][0] == 1 and self.map[(x + 1, y + 1)][0] == 0:
                # move 2x2 spaces right
                self.map[position] = self.map[(x, y)]
                self.map[(x, y)] = self.map[(x - 1, y)]
                self.map[(x + 1, y + 1)] = self.map[(x, y + 1)]
                self.map[(x, y + 1)] = self.map[(x - 1, y + 1)]

                # update the corrdinates of neighbours
                for p in [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]:
                    new_neighbour = []
                    for t in self.map[p][1]:
                        new_neighbour.append((t[0] + 1, t[1]))
                    self.map[p] = (self.map[p][0], new_neighbour)

                # move empty space left
                self.map[(x - 1, y)] = (0, [])
                self.map[(x - 1, y + 1)] = (0, [])

        elif self.map[(x, y)][0] == 2:
            # Check the position of neighbour and space below the neighbour
            neighbour = self.map[(x, y)][1][0]
            assert self.map[neighbour][0] == 2
            # Move 1x2 up and empty space right
            self.map[(x + 1, y)] = (self.map[(x, y)][0], [(self.map[(x, y)][1][0][0] + 1,
                                                           self.map[(x, y)][1][0][1])])
            self.map[(neighbour[0] + 1, neighbour[1])] = (self.map[neighbour][0],
                                                          [(self.map[neighbour][1][0][0] + 1,
                                                            self.map[neighbour][1][0][1])])
            self.map[neighbour] = (0, [])

        elif self.map[(x, y)][0] == 3:
            neighbour = self.map[(x, y)][1][0]
            assert self.map[neighbour][0] == 3

            if self.map[(neighbour[0] + 1, neighbour[1])][0] == 0:
                # Move 2x1 up and empty space down
                self.map[(x + 1, y)] = (self.map[(x, y)][0], [(self.map[(x, y)][1][0][0] + 1,
                                                               self.map[(x, y)][1][0][1])])
                self.map[(neighbour[0] + 1, neighbour[1])] = (self.map[neighbour][0],
                                                              [(self.map[neighbour][1][0][0] + 1,
                                                                self.map[neighbour][1][0][1])])
                self.map[(x, y)] = (0, [])
                self.map[neighbour] = (0, [])
            else:
                return

        elif self.map[(x, y)][0] == 4:
            # Swap the singular piece with empty space
            self.map[position] = self.map[(x, y)]
            self.map[(x, y)] = (0, [])
        else:
            # It is zero as well above, then do nothing
            return

    def move_right(self, position) -> None:
        """
        Move the piece on the position down (assume the piece we moved is a empty space).
            - Constraints are same as move_up()
        """
        # Get the coordinate of the space below position
        if self.map[position][0] != 0:
            print("Please move empty space.")
            return

        y = position[1]  # y-axis value for the coordinate on the left of the position
        if 0 <= position[0] < 3:
            x = position[0] + 1  # x-axis value for the coordinate on the left of the position
        else:
            # print("Error: out of range")
            return

        # Check what kind of piece upward the position
        if self.map[(x, y)][0] == 1:
            # Check the adjacent space of position to know the area the piece covered and
            # check is there has enough empty space to move
            if 0 < y <= 4 and self.map[(x, y - 1)][0] == 1 and self.map[(x - 1, y - 1)][0] == 0:
                # move 2x2 spaces left
                self.map[position] = self.map[(x, y)]
                self.map[(x, y)] = self.map[(x + 1, y)]
                self.map[(x - 1, y - 1)] = self.map[(x, y - 1)]
                self.map[(x, y - 1)] = self.map[(x + 1, y - 1)]

                # update the corrdinates of neighbours
                for p in [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)]:
                    new_neighbour = []
                    for t in self.map[p][1]:
                        new_neighbour.append((t[0] - 1, t[1]))
                    self.map[p] = (self.map[p][0], new_neighbour)

                # move empty space up
                self.map[(x + 1, y - 1)] = (0, [])
                self.map[(x + 1, y)] = (0, [])

            elif 0 <= y < 4 and self.map[(x, y + 1)][0] == 1 and self.map[(x + 1, y + 1)][0] == 0:
                # move 2x2 spaces right
                self.map[position] = self.map[(x, y)]
                self.map[(x, y)] = self.map[(x - 1, y)]
                self.map[(x + 1, y + 1)] = self.map[(x, y + 1)]
                self.map[(x, y + 1)] = self.map[(x - 1, y + 1)]

                # update the corrdinates of neighbours
                for p in [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]:
                    new_neighbour = []
                    for t in self.map[p][1]:
                        new_neighbour.append((t[0] + 1, t[1]))
                    self.map[p] = (self.map[p][0], new_neighbour)

                # move empty space left
                self.map[(x - 1, y)] = (0, [])
                self.map[(x - 1, y + 1)] = (0, [])

        elif self.map[(x, y)][0] == 2:
            # Check the position of neighbour and space below the neighbour
            neighbour = self.map[(x, y)][1][0]
            assert self.map[neighbour][0] == 2
            # Move 1x2 up and empty space right
            self.map[(x - 1, y)] = (self.map[(x, y)][0], [(self.map[(x, y)][1][0][0] - 1,
                                                           self.map[(x, y)][1][0][1])])
            self.map[(neighbour[0] - 1, neighbour[1])] = (self.map[neighbour][0],
                                                          [(self.map[neighbour][1][0][0] - 1,
                                                            self.map[neighbour][1][0][1])])
            self.map[neighbour] = (0, [])

        elif self.map[(x, y)][0] == 3:
            neighbour = self.map[(x, y)][1][0]
            assert self.map[neighbour][0] == 3

            if self.map[(neighbour[0] - 1, neighbour[1])][0] == 0:
                # Move 2x1 up and empty space down
                self.map[(x - 1, y)] = (self.map[(x, y)][0], [(self.map[(x, y)][1][0][0] - 1,
                                                               self.map[(x, y)][1][0][1])])
                self.map[(neighbour[0] - 1, neighbour[1])] = (self.map[neighbour][0],
                                                              [(self.map[neighbour][1][0][0] - 1,
                                                                self.map[neighbour][1][0][1])])
                self.map[(x, y)] = (0, [])
                self.map[neighbour] = (0, [])
            else:
                return

        elif self.map[(x, y)][0] == 4:
            # Swap the singular piece with empty space
            self.map[position] = self.map[(x, y)]
            self.map[(x, y)] = (0, [])
        else:
            # It is zero as well above, then do nothing
            return


@dataclass(order=True)
class Item:
    """
    Let heapq module to ignore to compare the State class element
    """
    priority: int
    item: Any = field(compare=False)


def txt_to_state() -> State:
    """Return a State that convert input form to output form"""
    ...


def expand(state: State) -> list[State]:
    """Return all the possible successors of s
    NOTE: The list would not include any State same as s.
    """
    result = []
    # Find empty spaces
    empty_spaces = [(x, y) for x in range(4) for y in range(5) if state.map[(x, y)][0] == 0]

    # Execute move up, down, left, and right for each empty space
    for p in empty_spaces:
        s1 = s_clone(state)
        s2 = s_clone(state)
        s3 = s_clone(state)
        s4 = s_clone(state)
        s1.move_up(p)
        s2.move_down(p)
        s3.move_left(p)
        s4.move_right(p)
        for i in [s1, s2, s3, s4]:
            if i != state and i not in result:
                result.append(i)

    return result


def s_clone(state: State) -> State:
    """
    Return a same State without aliasing.
    """
    clone = State()
    for y in range(5):
        for x in range(4):
            clone.map[(x, y)] = state.map[(x, y)]
    return clone


def is_goal(state: State) -> bool:
    """
    Return True if 2x2 piece are in the bottom of the puzzle
    (covered (1, 3), (2, 3), (1, 4), (2, 4))
    """
    for i in [(1, 3), (2, 3), (1, 4), (2, 4)]:
        if state.map[i][0] != 1:
            return False
    return True


def cost(state: State, explored: dict) -> int:
    """Return how many step we moved to reach the state."""
    parent = explored[state.__str__()]  # Previous state
    cost = 0
    while parent is not None:
        cost += 1
        parent = explored[parent]

    return cost


def h_value(state: State) -> int:
    """Return the heuristic estimate value of the given state."""
    # Find the coordinate of the top-left corner of the 2x2 piece
    coor = find_2x2(state)
    # Calculate the distance from coor to (1, 3)
    return abs(1 - coor[0]) + abs(3 - coor[1])


def h_value_advanced(state: State) -> int:
    """ Return the heuristic estimate value of the given state that
    greater or equal to h_value()'s estimate value.
    IDEA: Based on Manhattan distance, add more consideration for the estimation
        - Find out the path to move from given state to goal state
            - Two situation: move horizontal first or move vertical first
        - Calculate the number of obstacles on the two path we found
          (each obstacle makes the value +1)
        - Choose the sum value from the two path
    """
    # Find the coordinate of the top-left corner of the 2x2 piece
    coor = find_2x2(state)
    coors = [coor, (coor[0] + 1, coor[1]),
             (coor[0], coor[1] + 1), (coor[0] + 1, coor[1] + 1)]
    path = (1 - coor[0], 3 - coor[1])  # Store how many step and what is the direction for
                                       # horizontal and vertical move, respectively
    result = abs(path[0]) + abs(path[1])
    x_domain = []
    y_domain = [y for y in range(5) if coor[1] <= y <= coor[1] + path[1] + 1]

    if path[0] < 0:
        x_domain = [x for x in range(4) if (coor[0] + path[0]) <= x <= coor[0] + 1]
    else:
        x_domain = [x for x in range(4) if coor[0] <= x <= coor[0] + path[0] + 1]

    for y in y_domain:
        for x in x_domain:
            if state.map[(x, y)][0] != 0 and state.map[(x, y)][0] != 1:
                result += 1
    return result


def find_2x2(state: State) -> tuple:
    """ Helper function to find the coordinate of
    top-left corner of 2x2 piece in a given state
    """
    for y in range(5):
        for x in range(4):
            if state.map[(x, y)][0] == 1:
                return (x, y)


def as_search(init_s: State) -> list[str]:
    """ Return a optimal solution (list of str)"""
    frontier = []
    explored = dict()
    heappush(frontier, Item(0, init_s))
    explored[init_s.__str__()] = None
    total_cost = None
    solution = []
    sol_key = None

    # Start searching
    while bool(frontier):
        curr = heappop(frontier)

        # Check is it a goal state
        if is_goal(curr.item):
            total_cost = cost(curr.item, explored)
            sol_key = curr.item.__str__()
            break

        # Expanding states with pruning
        for successor in expand(curr.item):
            cost_so_far = cost(curr.item, explored) + 1
            if successor.__str__() not in explored:
                explored[successor.__str__()] = curr.item.__str__()
                priority = cost_so_far + h_value(successor)
                heappush(frontier, Item(priority, successor))

    # Interpret the solution from explored
    while sol_key is not None:
        solution.append(sol_key)
        sol_key = explored[sol_key]
    solution.append(f'Cost of the solution: {total_cost}')
    solution.reverse()

    # print out the solution
    print(f'{solution[0]}')
    for step in solution[1:]:
        print(step)
    return solution


if __name__ == "__main__":
    s = State()
    print(s)
