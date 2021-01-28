import pygame

#class for wrapping sprite properties
class Image():
    def __init__(self, sprite_ref, pos=(0,0)):
        #sprite_ref is either an image directory or a surface
        if type(sprite_ref) == pygame.Surface:
            self.sprite = sprite_ref
        elif type(sprite_ref) == str:
            self.sprite = pygame.image.load(sprite_ref)
        self.pos = pos
        
    def change_rect(self, attr, value):
        #changes position by changing its rect attributes("topleft", "bottomleft", etc)
        sprite_rect = self.sprite.get_rect()
        setattr(sprite_rect, attr, value)
        self.pos = sprite_rect.topleft

    def allign_to_screen(self, attr):
        #allign sprites rect attribute to screens rect attribute
        screen_rect = self.display.get_surface().get_rect()
        screen_value = getattr(self, attr)
        self.change_rect(attr, screen_value)

    def blit(self, surface):
        #blits its sprite at its position at given surface
        surface.blit(self.sprite, self.pos)


        

        


