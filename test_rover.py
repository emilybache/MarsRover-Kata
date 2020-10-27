from rover import turn, move, Position, Plateau, Rover, parse, World, main
import pytest

def test_turn_left():
    assert turn('N', 'L') == 'W'
    assert turn('W', 'L') == 'S'
    assert turn('S', 'L') == 'E'
    assert turn('E', 'L') == 'N'    
    

def test_turn_right():
    assert turn('N', 'R') == 'E'
    assert turn('W', 'R') == 'N'
    assert turn('S', 'R') == 'W'
    assert turn('E', 'R') == 'S'    
 

def test_move():
    assert move( Position(1,2,'N') ) == Position(1,3,'N')
    assert move( Position(1,2,'W')) == Position(0,2,'W')
    assert move( Position(1,2,'S')) == Position(1,1,'S')
    assert move( Position(1,2,'E')) == Position(2,2,'E')
   

def test_illegal_plateau():
    with pytest.raises(ValueError):
        Plateau(0,0)
        
def test_ok_plateau():
    assert Plateau(1,2).max_x == 1
    assert Plateau(1,2).max_y == 2
    
def test_plateau_contains():
    assert Plateau(1,0).contains(Position(0, 0, 'W'))
    assert Plateau(1,0).contains(Position(1, 0, 'W'))
    assert Plateau(1,0).contains(Position(-1, 0, 'W')) is False
    assert Plateau(1,0).contains(Position(0, -1, 'W')) is False
    assert Plateau(1,0).contains(Position(1, 1, 'W')) is False
    assert Plateau(1,0).contains(Position(0, 1, 'W')) is False

def test_move_rover_on_plateau():
    plateau = Plateau(5,5)
    rover = Rover( Position(1,2,'N'), plateau)
    rover.move()
    assert rover.position == Position(1,3, 'N')
  

def test_move_rover_over_edge():
    plateau = Plateau(0,1)
    rover = Rover( Position(0,1,'N'), plateau)
    with pytest.raises(ValueError):
        rover.move()
 
def test_parse_input():
    input = """\
5 5

1 2 N

LMLMLMLMM

3 3 E

MMRMMRMRRM
"""
    world = parse(input)
    assert world.plateau == Plateau(5,5)
    assert str(world.rovers) == "[Rover(Position(x=1, y=2, heading='N'), Plateau(max_x=5, max_y=5)), Rover(Position(x=3, y=3, heading='E'), Plateau(max_x=5, max_y=5))]"
    assert str(world.instructions) == "['LMLMLMLMM', 'MMRMMRMRRM']"
 
def test_move_world():
    rovers = [Rover(Position(x=1, y=2, heading='N'), Plateau(max_x=5, max_y=5)), Rover(Position(x=3, y=3, heading='E'), Plateau(max_x=5, max_y=5))]
    world = World(Plateau(5, 5))
    world.rovers = rovers
    world.instructions = ["LMLMLMLMM", "MMRMMRMRRM"]
    world.follow_instructions()
    assert world.rovers[0].position == Position(1, 3, 'N')
    assert world.rovers[1].position == Position(5, 1, 'E')
    
def test_report_position():
    plateau = Plateau(0,1)
    rover = Rover( Position(0,1,'N'), plateau)
    assert "0 1 N\n" == rover.report_position()
    
def test_main():
    input = """\
5 5

1 2 N

LMLMLMLMM

3 3 E

MMRMMRMRRM
"""
    output = main(input)
    expected_output = """\
1 3 N

5 1 E
"""
    assert output == expected_output
    