#! usr/bin/python

#from hex.constants import *

import pygame
from hex.constants import WHITE,INVISIBLE,BLACK

import numpy as np

class RegularPolygon(object):
    
    def __init__(self,center,radius,numofsides):
        self.theta = 2*np.pi / numofsides
        self.radius = radius
        self.center = center
        self.sides = numofsides    
        self.points = self.create_points()#self.radius,self.theta,self.center,self.sides)

    def create_points(self,center = None):#,radius,theta,center,sides):
        "Numpy array of the boundary points. The shape is 2xN"
        
        if center is None:
            center = self.center
        
        theta = np.linspace(0,2*np.pi,self.sides+1)[:-1]
        
        return np.stack([self.radius*np.cos(theta)+center[0], self.radius*np.sin(theta)+center[1]]).T
        
    
        #return [(self.radius*np.cos(i*self.theta)+self.center[0],self.radius*np.sin(i*self.theta)+self.center[1]) for i in range(self.sides)]
    
    def get_affine_points(self):
        affineCenter = [self.radius , np.sqrt(3)*self.radius/2]
        return self.create_points(affineCenter)

    def get_points(self):
        return self.points

    def move(self,newCenter):
        self.center = newCenter
        self.points = self.createPoints()

    def expand(self,newRadius):
        self.radius = newRadius
        self.points = self.createPoints()


    def __contains__(self,point):
        edge_vectors = np.roll(self.points,1,axis=0) - self.points
        test_vectors = np.array(point) - self.points
        
        matrices = np.stack([edge_vectors,test_vectors],axis=1)
        
        return all(np.linalg.det(matrices)<0)
        


class Tile(RegularPolygon):

    def __init__(self,w,h,radius,center):
        super(Tile,self).__init__(center,radius,6)
        self.position = (w,h)
        self.tile = None
        
        self.full_image = "./hex1.png"
        
        #self.full_image = pygame.image.load('./hex1.png').convert()        

        self.build()
    
    #def __contains__(self,point):
    #    x,y = self.position
    #    shifted_point = [point[0] - x,point[1] - y]
        
    #    return super(Tile,self).__contains__(shifted_point)
        

    def build(self):
        self.make_tile()
        self.draw_border()
        self.draw()

    def make_tile(self):
        width,height = self.get_size()
        self.tile = pygame.Surface((int(width),int(height))).convert()
        self.tile.fill(WHITE)
        self.tile.set_colorkey(INVISIBLE)

        self.add_to_tile(self.full_image)
        
        self.set_rect()

    def draw(self,update = None):
        screen = pygame.display.get_surface()
        screen.blit(self.tile,self.get_location())
        if update is None:
            pygame.display.update(self.get_location())

    def draw_border(self,color = BLACK,size = 2):
        """
        Gets the points of the hexagon and draws them to the tile.
        """
        points = self.get_affine_points()
        pygame.draw.polygon(self.tile,color,points,size)

    def get_position(self):
        return self.position

    def get_size(self):
        """
        Return the current dimensions of the tile. Typically called if the dimensions are changing.
        """
        return 2*self.radius,np.sqrt(3)*self.radius

    def shift(self,new_location):
        tile_rect = self.get_rect()
        dx,dy = new_location
        self.location_rect = tile_rect.move(-dx,-dy)

    def get_location(self):
        try:
            return self.location_rect
        except AttributeError:
            self.shift((0,0))
            return self.location_rect

    def set_rect(self):
        width,height = self.get_size()
        w,h = self.get_position()
        x = w*width*3/4
        y = h*height
        if w%2 == 1:
            y += height/2
        self.rect = pygame.Rect( x, y , width , height)
    
    def get_rect(self):
        return self.rect
    

    def add_to_tile(self,image = None):
        width,height = self.get_size()
        if image is None:
            image = self.full_image
        nimage = pygame.image.load(image).convert()            
        nimage = pygame.transform.scale(nimage,(int(width),int(height))).convert()
        
        self.tile.blit(nimage,(0,0))
        
        self.draw_border()




if __name__ == "__main__":
    
    S = Tile(70,70,10)
