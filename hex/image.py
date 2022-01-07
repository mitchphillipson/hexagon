#! usr/bin/env python
"""    This class is very useful, but as of yet incomplete. This class loads images into memory for later use and 
    resizing. This allows images to be resized once instead of each time that they are used, meaning faster 
    running times as images don't have to be resized upwards of 1000 times. 

    Still to do in this module:

        1. Create a method to add more images to the ImageHandler
    
        2. Include proper exceptions

        3. Write documentation.

        4. I'm sure I'll think of more

    Note that this module has a hidden dependecy on the pygame package.
"""

from constants import *


class ImageHandler(object):    
    """
ImageHandler(terrain,armies,highlights,invisible_color = (255,255,255))

Description of Inputs:
 1. images - Images to be loaded.
 4. invisible_color - The transparent background color.

Local Variables:
 1,4 - Same as above
 5. images - Basically a list of [terrain,armies]. I don't have highlights in here because they 
             need alpha values and so must be converted separately. 
 6. fullSizeImages - A dictionary containing with keys of the images and values of the actual
                     images, loaded full size.
 7. loadedImages - A dictionary of images that are the correct size for the zoom ratio.


What this class should do:
 
    """
    def __init__(self,images,invisible_color = INVISIBLE):
        self.images = images
        self.invisible_color = invisible_color
        self.fullSizeImages = {}
        self.loadedImages = {}
        for img in self.images:
            try:
                self.fullSizeImages[img] = pygame.image.load(img).convert()
            except:
                raise
        
    def get_image_list(self):
        """
        Return the images list
        """
        return self.images

    def get_image(self,key):
        """
        Return the image with name key. This will raise a KeyError if the image does not exist.
        """
        try:
            return self.loadedImages[key]
        except:
            raise

    def get_rect(self,key):
        """
        Return the bounding rectangle of the key image. If the image does not exist a KeyError will be raised.
        """
        try:
            return self.loadedImages[key].get_rect()
        except:
            raise

    def resize_images(self,width,height,invisible_color = None):
        """
        Resize all images to the new width and height.
        """
        w = int(width)
        h = int(height)
        color = self.invisible_color if invisible_color is None else invisible_color
        for img in self.images:
            self.loadedImages[img] = pygame.transform.scale(self.fullSizeImages[img],(w,h)).convert_alpha()
            #self.loadedImages[img].set_colorkey(INVISIBLE)

    def draw(self,surface,image):
        """
        Draw an image to the surface.
        """
        try:
            surface.blit(self.get_image(image),self.get_rect(image))
        except pygame.error:
            print(1)
            screen = pygame.display.get_surface()
            print(screen,self.get_image(image))
            screen.blit(self.get_image(image),self.get_rect(image))

    def get_order(self,dict_in):
        """
        The input must be a boolean dictionary. The output is a list of images that are True in the 
        dictionary, and are ordered according to the initial input.
        """
        out = []
        for image in self.images:
            try:
                if dict_in[image]:
                    out.append(image)
            except KeyError:
                pass
        return out


if __name__=='__main__':

    help(ImageHandler)

