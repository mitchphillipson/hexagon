#! usr/bin/env python

from hex.engine import Engine


game = Engine()

if __name__ == '__main__':
    
    try:
        game.play()
    except:
        game.on_QUIT()





