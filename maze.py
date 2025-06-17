class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if (self.empty()):
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if (self.empty()):
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if (contents.count("A") != 1):
            raise Exception("Maze must have exactly one start point")
        if (contents.count("B") != 1):
            raise Exception("Maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = [[False] * self.width for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                    if (contents[i][j] == "A"):
                        self.start = (i, j)
                    elif (contents[i][j] == "B"):
                        self.goal = (i, j)
                    elif (contents[i][j] == "#"):
                        self.walls[i][j] = True
                    else:
                        if (contents[i][j] != " "):
                            raise ValueError

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        
        for i in range(len(self.walls)):
            for j in range(len(self.walls[i])):
                if (self.walls[i][j]):
                    print("#", end="")
                elif ((i, j) == self.start):
                    print("A", end="")
                elif ((i, j) == self.goal):
                    print("B", end="")
                elif (solution is not None and (i, j) in solution):
                    print(".", end="")
                else:
                    print(" ", end="")
            print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if ((0 <= r < self.height) and (0 <= c < self.width) and (not self.walls[r][c])):
                result.append((action, (r, c)))
        return result


    def solve(self, type):
        """Finds a solution to maze, if one exists."""
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        if (type == "DFS"):
            frontier = StackFrontier()
        elif (type == "BFS"):
            frontier = QueueFrontier()
        else:
            raise ValueError
        
        frontier.add(start)
        self.explored = set()

        while (True):
            if (frontier.empty()):
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if (node.state == self.goal):
                actions = []
                cells = []
                while (node.parent is not None):
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if (not frontier.contains_state(state) and state not in self.explored):
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new("RGBA", (self.width * cell_size, self.height * cell_size), "black")
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i in range(len(self.walls)):
            for j in range(len(self.walls[i])):
                # Walls
                if (self.walls[i][j]):
                    fill = (40, 40, 40)
                # Start
                elif ((i, j) == self.start):
                    fill = (255, 0, 0)
                # Goal
                elif ((i, j) == self.goal):
                    fill = (0, 171, 28)
                # Solution
                elif ((solution is not None) and show_solution and ((i, j) in solution)):
                    fill = (220, 235, 113)
                # Explored
                elif ((solution is not None) and show_explored and ((i, j) in self.explored)):
                    fill = (212, 97, 85)
                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


m = Maze("Maze\\maze.txt")
print("Maze:\n")
m.print()
print("\nSolving...")
m.solve(type="DFS")
print("States Explored:", m.num_explored)
print("Solution:\n")
m.print()
m.output_image("Maze\\maze.png", show_explored=True)
