from collections import deque
from enum import Enum
import random


class Dir(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Player:
    def __init__(self, name):
        self.name = name
        
    def welcome(self):
        print(f"Hello {self.name}!!")
        print()
        
    # Render latest grid for the player.
    def render(self, size, snake, food):
        for x in range(size):
            for y in range(size):
                if snake.headPresent(x, y):
                    match snake.getDir():
                        case Dir.RIGHT.value:
                            print("\u25B6", end = " ")
                        case Dir.UP.value:
                            print("\u25B2", end = " ")
                        case Dir.LEFT.value:
                            print("\u25C0", end = " ")
                        case _:
                            print("\u25BC", end = " ")
                elif snake.present(x, y):
                    print("*", end = " ")
                elif food.present(x, y):
                    print("#", end = " ")
                else:
                    print("_", end = " ")
            print()
        print()


class Snake:
    def __init__(self, x = 0, y = 0, dir = Dir.RIGHT.value):
        self.cells = deque([(x, y)])
        self.cells_taken = set([(x, y)])
        self.dir = dir
        
    def getLength(self):
        return len(self.cells)
        
    def getDir(self):
        return self.dir
        
    # Snake's present is present at the given position.
    def headPresent(self, x, y):
        head_x, head_y = self.cells[-1]
        return x == head_x and y == head_y
        
    # Snake's body is present at the given position.
    def present(self, x, y):
        return (x, y) in self.cells_taken
    
    # Advance the snake in the given direction by 1 position.
    def advance(self, dir, size, food):
        if self.getLength() != 1 and (dir + self.dir) % 2 == 0:
            dir = self.dir

        head_x, head_y = self.cells[-1]
        tail_x, tail_y = self.cells[0]
        
        # Compute the next position of head.
        match dir:
            case Dir.RIGHT.value:
                head_y += 1
            case Dir.UP.value:
                head_x -= 1
            case Dir.LEFT.value:
                head_y -= 1
            case Dir.DOWN.value:
                head_x += 1
            
        # Head is going out of the grid.
        if head_x < 0 or head_x >= size or head_y < 0 or head_y >= size:
            return False
           
        # If food is present, eat it.
        if food.present(head_x, head_y):
            food.eat()
        # Otherwise, move the tail.
        else:
            self.cells.popleft()
            self.cells_taken.remove((tail_x, tail_y))
        
        # Head is colliding with the body.
        if (head_x, head_y) in self.cells_taken:
            return False
        
        # Move the head forward.
        self.cells.append((head_x, head_y))
        self.cells_taken.add((head_x, head_y))
        # Set the head's direction.
        self.dir = dir
        return True


class Food:
    def __init__(self, x = -1, y = -1, eaten = True):
        self.x = x
        self.y = y
        self.eaten = eaten
      
    # Eat the current food.
    def eat(self):
        self.eaten = True
        
    # Food is present at the given position.
    def present(self, x, y):
        return x == self.x and y == self.y
        
    # Regenerate food at random location if current food was eaten.
    def regenerateIfRequired(self, size, snake):
        if self.eaten:
            lower_limit, upper_limit = 0, size * size - 1
            r = random.randint(lower_limit, upper_limit)
            x = r // size
            y = r % size
            
            while snake.present(x, y):
                r = random.randint(lower_limit, upper_limit)
                x = r // size
                y = r % size

            self.x = x
            self.y = y
            self.eaten = False

        
class Game:
    def __init__(self, size, player):
        self.size = size
        self.player = player
        self.snake = Snake()
        self.food = Food()
        self.regenerateFoodIfRequired()

    def executeNextStep(self, dir):
        if self.snake.advance(dir, self.size, self.food):
            self.regenerateFoodIfRequired()
            self.renderGridForPlayer()
            return True
        else:
            return False
            
    def renderGridForPlayer(self):
        self.player.render(self.size, self.snake, self.food)
        
    def regenerateFoodIfRequired(self):
        if not self.snakeAtMaxLength():
            self.food.regenerateIfRequired(self.size, self.snake)
        
    def snakeAtMaxLength(self):
        return self.snake.getLength() == (self.size ** 2)
            
    def play(self):
        self.player.welcome()
        self.renderGridForPlayer()
        # 0 is exit, 1 is win, 2 is lose
        result = 2
        
        while True:
            key = input("Input direction: ").lower()
            print()
            
            match key:
                case "r":
                    if not self.executeNextStep(Dir.RIGHT.value):
                        break
                case "u":
                    if not self.executeNextStep(Dir.UP.value):
                        break
                case "l":
                    if not self.executeNextStep(Dir.LEFT.value):
                        break
                case "d":
                    if not self.executeNextStep(Dir.DOWN.value):
                        break
                case "exit":
                    result = 0
                    break
                case _:
                    pass
            
            if self.snakeAtMaxLength():
                result = 1
                break
            
        if result == 0:
            print("Stopped!!")
        elif result == 1:
            print("You won!!")
        else:
            print("You lose!!")


name = input("Enter your name: ")
player = Player(name)
size = int(input("Enter grid size: "))
game = Game(size, player)
game.play()
