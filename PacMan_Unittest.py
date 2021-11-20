import unittest
from PacManOfficial import Arena, Ghost, PacMan, Biscuit, SpecialBiscuit, PacmanGame, PacmanGui, generation
from pacman_map import in_wall, in_biscuit, in_special_biscuit

# "#main()" in the main program (PacManOfficial.py) to run the test and not the game.

class PacManTest(unittest.TestCase):
    
    def test_stand_by(self):
        '''
        PacMan stand-by at the beginning of the game.
        '''
        a= Arena((232,256))
        b= PacMan(a,(112,184))
        b.move()
        self.assertTrue(b.position() == (112,184))
        
    def test_move_right(self): 
        '''
        Right movement of PacMan starting from the initial position.
        '''
        a= Arena((232,256))
        b= PacMan(a,(112,184))
        b.control("d")
        b.move()
        self.assertTrue(b.position() == (114,184))
        
    def test_move_right(self):
        '''
        Left movement of PacMan starting from the initial position.
        '''
        a= Arena((232,256))
        b= PacMan(a,(112,184))
        b.control("a")
        b.move()
        self.assertTrue(b.position() == (110,184))
        
    def test_move_up(self):
        '''
        Up movement of PacMan starting from the initial position. PacMan collision with the wall supposed.
        '''
        a= Arena((232,256))
        b= PacMan(a,(112,184))
        b.control("w")
        b.move()
        self.assertTrue(b.position() == (112,184))
    
    def test_move_down(self):
        '''
        Down movement of PacMan starting from the initial position. PacMan collision with the wall supposed.
        '''
        a= Arena((232,256))
        b= PacMan(a,(112,184))
        b.control("s")
        b.move()
        self.assertTrue(b.position() == (112,184))
        
    def test_corner(self):
        '''
        Right down corner test. PacMan cant' keep going right and will stop in the corner.
        '''
        a= Arena((232,256))
        b= PacMan(a,(208,232))
        b.control("d") 
        b.move()
        self.assertTrue(b.position() == (208,232))
        
    def test_PacManGhost_collision(self):
        '''
        PacMan and Ghost collision check. If PacMan collide with the Ghost, he loses a life.
        PacMan starts with 3 lives, so 2 are expected to remain after the collision.
        '''
        a= Arena((232,256))
        b= PacMan(a,(112,184))
        c= Ghost(a, (114,184))
        b.control("d")
        a.move_all()
        self.assertTrue(b.lives() == 2)
        
    
    def test_PacManBiscuit_collision(self):
        '''
        PacMan and Biscuit collision check. If PacMan collide with the Biscuit, game score increases by 1 point.
        PacMan starts from position (114,230) so score is expected to increase by 1 points if he goes down one time.
        In this test a Biscuit is generated and the increasing of the score is checked.
        '''
        a= Arena((232,256))
        b= PacMan(a,(114,214))
        
        Biscuit(114, 216, a)
        
        b.control("s")
        a.move_all()
        
        self.assertTrue(b.score() == 1)
        
        
    def test_PacManSpecialBiscuit_collision(self):
        '''
        PacMan and SpecialBiscuit collision check. If PacMan collide with the SpecialBiscuit, PacMan enters in the
        Power mode and can eat Ghosts in the map. In this test a SpecialBiscuit is generated and his collision
        with PacMan is checked. 
        '''
        a= Arena((232,256))
        b= PacMan(a,(206,184))
        
        SpecialBiscuit(208,184, a)
        
        b.control("d")
        a.move_all()
        
        self.assertTrue(b.power_mode())
        
        
class GhostTest(unittest.TestCase):
    
    def test_move(self):
        '''
        Ghost movement test. If Ghost starts from position (206,232), after one tick he must change his position.
        '''
        a= Arena((232,256))
        b= Ghost(a, (206,232))
        
        b.move()
        
        self.assertTrue(b.position() != (206,232))

    
    def test_corner(self):
        '''
        In this test a Ghost is generated in the right-down corner.
        He can take 2 possible directions, not 4 as in the others positions of the arena.
        '''
        a= Arena((232,256))
        b= Ghost(a, (208,232))
        
        b.move()
        self.assertTrue((b.position() != (210,232)) and (b.position() != (208,234)))
        


if __name__ == '__main__':
    unittest.main()
    

