'''
PacMan by Davide Reverberi
'''

import g2d
from time import time
from random import choice, randrange, randint
from pacman_map import in_wall, in_biscuit, in_special_biscuit

X = 3 #Seconds of vulnerability of the ghosts after PacMan ate special biscuit.
#It can be modified at will to change the difficulty of the game.

color_list= [1,2,3,4]  #4 color possibilities of the ghosts

class Actor():
    def move(self):
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int):
        raise NotImplementedError('Abstract method')

    def size(self) -> (int, int):
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int):
        raise NotImplementedError('Abstract method')


class Arena():
    def __init__(self, size: (int, int)):
        self._w, self._h = size
        self._count = 0
        self._actors = []
        self._ghosts_out = 0

    def add(self, a: Actor):
        if a not in self._actors:
            self._actors.append(a)

    def remove(self, a: Actor):
        if a in self._actors:
            self._actors.remove(a)

    def move_all(self):
        actors = list(reversed(self._actors))
        for a in actors:
            if not isinstance(a, Biscuit) and not isinstance(a, SpecialBiscuit):
                a.move()
                for other in actors:
                # reversed order, so actors drawn on top of others
                # (towards the end of the cycle) are checked first
                    if other is not a and self.check_collision(a, other):
                        a.collide(other)
                        other.collide(a)
                        if isinstance(a, PacMan) and isinstance(other, SpecialBiscuit):
                            for c in actors:
                                if isinstance(c, Ghost):
                                    c.collide_special()
        self._count += 1

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        x1, y1, w1, h1 = a1.position() + a1.size()
        x2, y2, w2, h2 = a2.position() + a2.size()
        return (y2 < y1 + h1 and y1 < y2 + h2
            and x2 < x1 + w1 and x1 < x2 + w2
            and a1 in self._actors and a2 in self._actors)

    def actors(self) -> list:
        return list(self._actors)

    def size(self) -> (int, int):
        return (self._w, self._h)

    def count(self) -> int:
        return self._count
    
    def add_ghost_out(self):
        self._ghosts_out += 1
    
    def remove_ghost_out(self):
        self._ghosts_out -= 1
    
    def ghosts_out(self):
        return self._ghosts_out


class PacMan(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._speed = 2
        self._dx, self._dy = 0, 0
        self._lives = 3
        self._symbol = (16,0)
        self._last_collision = 20
        self._arena = arena
        self._mounth_open = False
        self._count=0
        self._score = 0                 #Game score (1 Biscuit = 1 Point)
        self._power_mode = False
        self._power_time = X*30 +1
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        
        if in_wall(self._x+self._dx,self._y+self._dy):
            self._dx=0
            self._dy=0

        self._y += self._dy
        if self._y < 0:
            self._y = 0
            self._dy=-self._dy
        elif self._y > arena_h - self._h:
            self._y = arena_h - self._h
            self._dy=-self._dy

        self._x += self._dx
        if self._x < 0:
            self._x = arena_w - self._w
        elif self._x > arena_w - self._w:
            self._x = 0 
         
        self._count = self._count +1
        self._last_collision+=1
        
        if self._count == 8:
            self._mounth_open = not self._mounth_open
            self._count=0
            
        self._power_time += 1
            
        if self._power_time == X*30: #x seconds of vulnerability after eating the special biscuit
            self._power_mode = not self._power_mode
                   
    def control(self, keys):
        u, d, l, r = "w", "s", "a", "d"
        
        dx, dy = self._dx, self._dy
        
        if self._x%8 == 0 and self._y%8 == 0:
            if u in keys:
                    self._dy = -self._speed
                    self._dx = 0
            elif d in keys:
                self._dy = self._speed
                self._dx = 0
            if l in keys:
                self._dx = -self._speed
                self._dy = 0 
            elif r in keys:
                self._dx = self._speed
                self._dy = 0
                
            if in_wall(self._x + self._dx, self._y+ self._dy):
                self._dx, self._dy = dx, dy
            
    
    def collide(self, other):
        if self._last_collision > 20:        #If last collision occured at least 20 ticks ago
            if isinstance(other, Ghost):
                if not self._power_mode:
                    self._x, self._y = 112,184
                    self._dx, self._dy = 0,0
                    self._symbol = (16,0)
                    self._lives-=1
                    self._last_collision = 0
        if isinstance(other, Biscuit):
            self._score +=1
        if isinstance(other, SpecialBiscuit):
            self._power_mode = True
            self._power_time= 0

    def position(self):
        return self._x, self._y
    
    def size(self):
        return self._w, self._h
    
    def lives(self):
        return self._lives
    
    def score(self):
        return self._score
    
    def power_mode(self):
        return self._power_mode
    
    def power_time(self):
        return self._power_time
    
    def symbol(self):
        if self._mounth_open:
            if self._dy>0:
                self._symbol = (0,48)
            if self._dy<0:
                self._symbol = (0,32)
            if self._dx>0:
                self._symbol = (0,0)
            if self._dx<0:
                self._symbol = (0,16)
        else:
            if self._dy>0:
                self._symbol = (16,48)
            if self._dy<0:
                self._symbol = (16,32)
            if self._dx>0:
                self._symbol = (16,0)
            if self._dx<0:
                self._symbol = (16,16)
        return self._symbol

class Ghost(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._arena = arena
        self._speed=2
        self._not_visible = False
        self._visible_count = X*30 +1
        self._dx, self._dy = self._speed, 0
        self._color= choice(color_list)
        color_list.remove(self._color)
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        
        scelta = [(self._speed,0),(-self._speed,0),(0,self._speed),(0,-self._speed)]
        
        if self._x%8==0 and self._y%8==0:
            scelta.remove((-self._dx,-self._dy))
            self._dx, self._dy = choice(scelta)
            
            if in_wall(self._x+self._dx, self._y+self._dy):
                scelta.remove((self._dx,self._dy))
                self._dx, self._dy = choice(scelta)
                
        if in_wall(self._x+self._dx, self._y+self._dy):
            scelta.remove((self._dx,self._dy))
            self._dx, self._dy = choice(scelta)
         
        self._visible_count += 1
            
        if self._visible_count == X*30:
            self._not_visible = False
            
        self._y += self._dy
        if self._y < 0:
            self._y = 0
            self._dy=-self._dy
        elif self._y > arena_h - self._h:
            self._y = arena_h - self._h
            self._dy=-self._dy

        self._x += self._dx
        if self._x < 0:
            self._x = arena_w - self._w
        elif self._x > arena_w - self._w:
            self._x = 0 
            
        
    def collide(self, other):
        if isinstance(other, PacMan) and other.power_mode():
            color_list.append(self._color)
            self._arena.remove(self)
            self._arena.add_ghost_out()
            
    def collide_special(self):
        self._not_visible = True
        self._visible_count = 0

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
        if self._not_visible:
            if self._dy>0:
                return 176,80
            if self._dy<0:
                return 160,80
            if self._dx>0:
                return 128,80
            if self._dx<0:
                return 144,80
            return 120,80
        
        if self._color == 1 : #Red Ghost
            if self._dy>0:
                return 96,64
            if self._dy<0:
                return 64,64
            if self._dx>0:
                return 16,64
            if self._dx<0:
                return 32,64
            return 16,64
            
        elif self._color == 2:  #Pink Ghost
            if self._dy>0:
                return 96,80
            if self._dy<0:
                return 64,80
            if self._dx>0:
                return 16,80 
            if self._dx<0:
                return 32,80
            return 16,80
            
        elif self._color == 3:  #Light-Blue Ghost
            if self._dy>0:
                return 96,96
            if self._dy<0:
                return 64,96
            if self._dx>0:
                return 16,96
            if self._dx<0:
                return 32,96
            return 16,96
            
        elif self._color == 4:  #Orange Ghost
            if self._dy>0:
                return 96,112
            if self._dy<0:
                return 64,112
            if self._dx>0:
                return 16,112
            if self._dx<0:
                return 32,112
            return 16,112
        
        
class Biscuit(Actor):
    def __init__(self, x , y , arena):
        self._arena = arena
        self._x, self._y = x,y
        self._w, self._h = 16,16
        arena.add(self)
        
    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)
    
    def move(self):
        pass
    
    def position(self):
        return self._x, self._y
    
    def size(self):
        return self._w, self._h
        
    def symbol(self):
        return 160,48
    
class SpecialBiscuit(Actor):
    def __init__(self, x , y , arena):
        self._arena = arena
        self._x, self._y = x,y
        self._w, self._h = 16,16
        arena.add(self)
        
    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)
    
    def move(self):
        pass
    
    def position(self):
        return self._x, self._y
    
    def size(self):
        return self._w, self._h
        
    def symbol(self):
        return 176,48
        

def generation(arena: Arena):
    '''
    Special function used to generate Biscuit and SpecialBiscuit object at the beginning of the game.
    The function is called in the game initialization, in PacManGame
    '''
    for i in range(0,31):
        for j in range(0,29):
            if in_biscuit(j,i):  
                Biscuit(j*8-8,i*8-8,arena)
            if in_special_biscuit(j,i):
                SpecialBiscuit(j*8-8,i*8-8,arena)
                  
class PacmanGame:
    def __init__(self):
        self._arena = Arena((232, 256))
        g1=Ghost(self._arena,(160,160))
        g2=Ghost(self._arena,(40,40))
        g3=Ghost(self._arena,(100,40))
        g4=Ghost(self._arena,(160,40))
        self._hero = PacMan(self._arena,(112,184))
        generation(self._arena)
        
    def new_ghosts(self):
        if self._hero.power_time() == X*30:
            if self._arena.ghosts_out() != 0:
                for i in range(0,self._arena.ghosts_out()):
                    Ghost(self._arena,(112,88))
                    self._arena.remove_ghost_out()
        
    def arena(self) -> Arena:
        return self._arena

    def hero(self) -> PacMan:
        return self._hero

    def game_over(self) -> bool:
        return self._hero.lives() <= 0 

    def game_won(self) -> bool:
        return self._hero.score() == 240 #240 biscuits in the arena. Eat all of them to win

def game_lostGUI(arena: Arena):
    '''
    Function that allows to create an interface when the game is lost. The funcion is linked to the main GUI.
    '''
    arena_w, arena_h = arena.size()
    g2d.set_color((0,0,0))
    g2d.fill_rect((0, 0),(arena_w,arena_h +30))
    g2d.set_color((255,255,255))
    j = 64
    w = arena_w/2 -42
    for i in range(0,4):
        g2d.draw_image_clip("pac-man.png", (0,j), (16,16), (w, 60))
        j += 16
        w += 16 + 10
    g2d.draw_text_centered("GAME OVER", (arena_w/2, arena_h/2), 30)
    
def game_wonGUI(arena: Arena):
    '''
    Function that allows to create an interface when the game is won. The funcion is linked to the main GUI.
    '''
    arena_w, arena_h = arena.size()
    g2d.set_color((0,0,0))
    g2d.fill_rect((0, 0),(arena_w,arena_h +30))
    g2d.set_color((255,255,255))
    j = 64
    w = arena_w/2 -42
    for i in range(0,4):
        g2d.draw_image_clip("pac-man.png", (0,j), (16,16), (w, 60))
        j += 16
        w += 16 + 10
    g2d.draw_text_centered("YOU WON!", (arena_w/2, arena_h/2), 30)
    g2d.draw_text_centered("Congratulations", (arena_w/2, arena_h/2+20), 30)
    g2d.draw_text_centered("Press Esc to exit! ", (arena_w/2, arena_h/2+60), 22)

class PacmanGui:
    def __init__(self):
        self._game = PacmanGame()
        self._W,self._H = self._game.arena().size()
        g2d.init_canvas((self._W,self._H+30))
        self._sprites = g2d.load_image("pac-man.png")
        self._menu = True
        self._count_time_end_game = 0
        g2d.main_loop(self.tick)

    def tick(self):
        g2d.set_color((0,0,0))
        g2d.fill_rect((0, 0),(self._W,self._H +30))
        g2d.set_color((255,255,255))
        j = 64
        w = self._W/2 -42
        for i in range(0,4):
            g2d.draw_image_clip(self._sprites, (0,j), self._game.hero().size(), (w, 60))
            j += 16
            w += 16 + 10
        g2d.draw_text_centered("PacMan Game", (self._W/2, self._H/2), 30)
        g2d.draw_text_centered("Press Space to start", (self._W/2, self._H/2+30), 30)
        g2d.draw_text_centered("Press Esc to exit! ", (self._W/2, self._H/2+60), 22)
        g2d.draw_image_clip(self._sprites, (16,0), self._game.hero().size(), (self._W/2, self._H-20))
        
        key = g2d.current_keys()
        
        if "Spacebar" in key:
            self._menu = False
            
        elif "Escape" in key:
            g2d.close_canvas()
            
        if not self._menu:
            self._game.hero().control(g2d.current_keys())
            arena = self._game.arena()
            arena.move_all()
            self._game.new_ghosts()

            g2d.clear_canvas()
            g2d.set_color((0,0,0))
            g2d.fill_rect((0, self._H),(self._W,30)) 
            g2d.draw_image_clip("pac-man-bg.png",(0,0),arena.size(),((0,0)))
            for a in arena.actors():
                if a.symbol() != None:
                    g2d.draw_image_clip(self._sprites, a.symbol(), a.size(), a.position())
                else:
                    g2d.fill_rect(a.position(), a.size())
                    
            lives = "Lives: " + str(self._game.hero().lives())
            points = "Points: " + str(self._game.hero().score())
            
            g2d.set_color((255,255,255))
            g2d.draw_text_centered(lives + "    " + points, (self._W/2, self._H +10), 24)

            if self._game.game_over():
                game_lostGUI(self._game.arena())
                self._count_time_end_game += 1
                if self._count_time_end_game == 3*30: #The interface shows up for 3 seconds.
                    g2d.close_canvas()
                
            elif self._game.game_won():
                game_wonGUI(self._game.arena())
                self._game.arena().remove(self._game.hero())
                self._count_time_end_game += 1
                if self._count_time_end_game == 3*30: #The interface shows up for 3 seconds.
                    g2d.close_canvas()
    
def main():
    gui = PacmanGui()
    
main()


                
              




 

