#!/usr/bin/env python3

import sys
from dataclasses import dataclass

def turn(current_direction, turn_direction):
    if turn_direction == 'L':
        directions = ['N', 'W', 'S', 'E']
    elif turn_direction == 'R':
        directions = ['E', 'S', 'W', 'N']
    current_direction_index = directions.index(current_direction)
    new_direction_index = current_direction_index + 1
    return directions[new_direction_index % len(directions)]
   

def move(position):
    (x, y, direction) = (position.x, position.y, position.heading)
    moves = {'N': lambda x, y: Position(x, y+1, direction),
             'W': lambda x, y: Position(x-1, y, direction),
             'S': lambda x, y: Position(x, y-1, direction),
             'E': lambda x, y: Position(x+1, y, direction),
            }
    return moves[direction](x, y)  

@dataclass
class Position:
    x : int
    y : int
    heading : str

@dataclass
class Plateau:
    max_x : int
    max_y : int
    def __init__(self, max_x, max_y):
        if max_x <= 0 and max_y <= 0:
            raise ValueError("cannot construct zero or negative sized plateau")
        self.max_x = max_x
        self.max_y = max_y
 
    def contains(self, position):
        return 0 <= position.x <= self.max_x and \
               0 <= position.y <= self.max_y

class Rover:
    def __init__(self, position, plateau):
        self.position = position
        self.plateau = plateau
        
    def move(self):
        new_position = move(self.position)
        if not self.plateau.contains(new_position):
            raise ValueError(f"Cannot move to {new_position} since it is off edge of plateau")
        self.position = new_position        

    def turn(self, direction):
        new_heading = turn(self.position.heading, direction)
        self.position = Position(self.position.x, self.position.y, new_heading)
        
    def __repr__(self):
        return f"Rover({self.position}, {self.plateau})"
    
    def report_position(self):
        return f"{self.position.x} {self.position.y} {self.position.heading}\n"
        
class World:
    def __init__(self, plateau):
        self.plateau = plateau
        self.rovers = []
        self.instructions = []
        
    def add_rover(self, rover):
        self.rovers.append(rover)
        
    def add_instructions(self, instructions):
        self.instructions.append(instructions)
        
    def follow_instructions(self):
        for index, rover in enumerate(self.rovers):
            instructions = self.instructions[index]
            for c in instructions:
                if c == 'M':
                    rover.move()
                elif c in ['L', 'R']:
                    rover.turn(c)
                    

def parse(input):
    lines = filter(lambda l: l.strip(), input.splitlines())
    max_x, max_y = next(lines).split()
    plateau = Plateau(int(max_x), int(max_y))
    world = World(plateau)
    while lines:
        try:
            x, y, heading = next(lines).split()
            instructions = next(lines)
            world.add_rover(Rover( Position(int(x), int(y), heading), plateau))
            world.add_instructions(instructions)
        except StopIteration:
            break
    return world


def main(input):
    world = parse(input)
    world.follow_instructions()
    output = "\n".join([rover.report_position() for rover in world.rovers])
    return output


if __name__ == "__main__":
    input = sys.stdin.read()
    output = main(input)
    print(output)
