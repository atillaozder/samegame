import random

class Tile:
    def __init__(self, *args, **kwargs):
        self.value = args[0]

    def __str__(self):
        if (self.value == 1):
            return 'R'
        elif (self.value == 2):
            return 'Y'
        elif (self.value == 3):
            return 'G'
        elif (self.value == 4):
            return 'B'
        else:
            return ' '


class Game:
    # DEFAULT CONSTRUCTOR
    def __init__(self, *args, **kwargs):
        self.rows = args[0]
        self.cols = args[1]
        self.board = [[Tile(random.randint(1, 4)) for j in range(self.cols)] for i in range(self.rows)]

    # BFS ALGORITHM TO FIND SAME TILES STARTING WITH GIVEN COORDINATES
    def BFS(self, x, y):
        if self.board[x][y].value == 0:
            return []

        queue = []
        queue.append([x, y])

        visited = []
        visited.append([x, y])

        connected = []
        connected.append([x, y])

        xDir = [-1, 1, 0, 0]
        yDir = [0, 0, -1, 1]

        while len(queue) > 0:
            cell = queue.pop(0)
            x = cell[0]
            y = cell[1]

            for i in range(0, 4):
                dx = xDir[i]
                dy = yDir[i]
                nx = x + dx
                ny = y + dy

                if nx > -1 and nx < self.rows and ny > -1 and ny < self.cols:
                    if not visited.count([nx, ny]):
                        visited.append([nx, ny])

                        if self.board[nx][ny] == self.board[x][y]:
                            queue.append([nx, ny])
                            connected.append([nx, ny])
        return connected

    # DFS ALGORITHM TO FIND SAME TILES STARTING WITH GIVEN COORDINATES
    def DFS(self, x, y, prev):
        if (x < 0 or x >= self.rows or y < 0 or y >= self.cols or prev != self.board[x][y].value):
            return 0
        else:
            self.board[x][y].value = 0
            return 1 + self.DFS(x - 1, y, prev) \
                   + self.DFS(x + 1, y, prev) \
                   + self.DFS(x, y - 1, prev) \
                   + self.DFS(x, y + 1, prev)

    # A SUPPORTING METHOD FOR GAME OVER - CHECKS IF REMAINING MOVES EXIST
    def remaining_moves(self, x, y, prev, visited):
        if (x < 0 or x >= self.rows or y < 0 or y >= self.cols
                or prev != self.board[x][y].value or visited[x][y] == 1):
            return 0
        else:
            visited[x][y] = 1
            return 1 + self.remaining_moves(x - 1, y, prev, visited) \
                   + self.remaining_moves(x + 1, y, prev, visited) \
                   + self.remaining_moves(x, y - 1, prev, visited) \
                   + self.remaining_moves(x, y + 1, prev, visited)

    # ITERATES OVER ROWS AND CHANGE EACH TO ABOVE THAT IS NOT EMPTY
    def shift_rows(self):
        for i in range(self.rows)[::-1]:
              for j in range(self.cols):
                  if self.board[i][j].value == 0:
                    row = self.find_needed_row(i, j)
                    self.swap_rows(i, j, row)

    def swap_rows(self, i, j, row):
        while i >= 0 and row >= 0:
            self.board[i][j].value = self.board[row][j].value
            self.board[row][j].value = 0
            i -= 1
            row -= 1

    def find_needed_row(self, x, y):
        above = 1
        needed_row = x - above
        while needed_row >= 0 and self.board[needed_row][y].value == 0:
            above += 1
            needed_row = x - above

        return needed_row

    # FINDS APPROPRIATE COLUMN AND SEND IT TO CHANGE WITH CURRENT EMPTY COLUMN
    def shift_columns(self):
        for j in range(self.cols):
            count = 0
            for i in range(self.rows):
                if self.board[i][j].value == 0:
                    count += 1
                if count == self.rows:
                    col = self.find_needed_column(j + 1)
                    self.rec_shift_cols(self.rows - 1, j, col)
                    break

    # SHIFTS COLUMNS RECURSIVELY - FOR EACH ROW WITH NON EMPTY NEAREST
    def rec_shift_cols(self, x, y, col):
        if (x < 0 or x >= self.rows or y < 0 or y >= self.cols):
            return
        else:
            self.board[x][y].value = self.board[x][col].value
            self.board[x][col].value = 0
            self.rec_shift_cols(x - 1, y, col)

    # GIVEN COLUMN IF NEXT COLUMN (ENTIRE) IS EMPTY FINDS APPROPRIATE COLUMN THAT WILL BE CHANGED
    def find_needed_column(self, y):
        if (y < self.cols):
            count = 0
            for i in range(self.rows):
                if self.board[i][y].value == 0:
                    count += 1

            if count == self.rows:
                return self.find_needed_column(y + 1)
            else:
                return y
        else:
            return y - 1

    # IF GAME IS OVER CHECKS REMAINING TILES TO DETERMINE SCORE
    def remaining_tiles(self):
        count = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j].value != 0:
                    count += 1
        return count

    # CHECKS IF GAME IS OVER
    def game_over(self):
        visited = [[0 for j in range(self.cols)] for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j].value != 0 and self.remaining_moves(i, j, self.board[i][j].value, visited) > 1:
                    return False
        return True

    # A DISPLAY METHOD FOR PRINTING BOARD TO CONSOLE
    def display(self):
        print()
        for i in range(self.rows):
            print(i, end="  ")
            for j in range(self.cols):
                print(self.board[i][j], end="  ")
            print()

            if i == (self.rows - 1):
                print(end="   ")
                for k in range(self.cols):
                    if k < 10:
                        print(k, end="  ")
                    else:
                        print(k, end=" ")
        print()


if __name__ == '__main__':
    game = Game(5, 5)

    x, y, score = 0, 0, 0
    while (x != -1 and y != -1):
        game.display()
        print("Score: ", score)
        x = int(input("X: "))
        y = int(input("Y: "))

        # BASED ON DFS ALGORITHM
        if (x >= 0 and x < game.rows and y >= 0 and y < game.cols and game.board[x][y].value != 0):
            temp = game.board[x][y].value
            sum = game.DFS(x, y, temp)

            if (sum > 1):
                score += (sum - 2) * (sum - 2)
                game.shift_rows()
                game.shift_columns()

                if (game.game_over()):
                    break
            else:
                game.board[x][y].value = temp

    remains = game.remaining_tiles()
    if (remains > 0):
        score -= remains
    else:
        score *= 5

    game.display()
    print("Total Score: ", score)
