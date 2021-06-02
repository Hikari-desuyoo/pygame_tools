import pygame
arial_fp = "res/others/arial.ttf"
#class for wrapping sprite properties    
class Image():
    def __init__(self, sprite_ref, pos=[0,0]):
        #sprite_ref is either an image directory or a surface
        if type(sprite_ref) == pygame.Surface:
            self.sprite = sprite_ref
        elif type(sprite_ref) == str:
            self.sprite = pygame.image.load(sprite_ref)
        else:
            print(sprite_ref)
            raise ValueError("Image recebeu algum negócio esquisito")
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def get_x(self):
        return self.pos[0]
    
    def set_x(self, value):
        self.pos = (value, self.pos[1])

    x = property(get_x, set_x)
        
    def get_y(self):
        return self.pos[1]
    
    def set_y(self, value):
        self.pos = (self.pos[0], value)

    y = property(get_y, set_y)
        
    def change_rect(self, attr, value):
        #changes position by changing its rect attributes("topleft", "bottomleft", etc)
        sprite_rect = self.sprite.get_rect()
        setattr(sprite_rect, attr, value)
        self.pos = sprite_rect.topleft

    def allign(self, image, attr):
        image_rect = image.get_rect()
        image_value = getattr(image_rect, attr)
        self.change_rect(attr, image_value)

    def allign_to_screen(self, attr):
        #allign sprites rect attribute to screens rect attribute
        screen_rect = pygame.display.get_surface().get_rect()
        screen_value = getattr(screen_rect, attr)
        self.change_rect(attr, screen_value)

    def get_rect(self):
        rect = self.sprite.get_rect()
        rect.topleft = self.pos
        return rect

    def tile(self, index, size=None):
        if not size:
            size = self.tile_size
        final_surface = pygame.Surface(size, pygame.SRCALPHA)
        final_surface.blit(self.sprite, (0,0), area=pygame.Rect(index*size[0],0,size[0],size[1]))
        return final_surface

    def copy(self):
        return Image(self.sprite.copy(), self.pos[:])

    def blit(self, surface=None, allign = None):
        if not surface:
            surface = pygame.display.get_surface()

        if type(surface) != pygame.Surface:
            print(surface)
            raise Exception("blit recebeu "+str(surface))
        if allign:
            surface_rect = surface.get_rect()
            screen_value = getattr(surface_rect, allign)
            self.change_rect(allign, screen_value)
            
        #blits its sprite at its position at given surface
        surface.blit(self.sprite, self.pos)


#WRITING

class Text():
    def __init__(self, size, font_fp, color = (0,0,0)):
        self.font_fp = font_fp
        self.size = size
        self.reset_font()
        self.set_color(color)
        
    def set_color(self, color):
        self.color = color
        
    def reset_font(self, size = None):
        if not size:
            size = self.size
        self.font_obj = pygame.font.Font(self.font_fp, size)
        
    def get_text(self, text, pos = None, surface = None, max_width = None):
        
        #linebreaking
        width, height = self.font_obj.size(text)
        text = text.split("<br>")
        solved = False
        if max_width:
            if width > max_width:
                chunks = []
                for par in text:
                    text_words = par.split(" ")
                    chunk = ""
                    for word in text_words:
                        last_chunk = chunk
                        chunk += word+" "
                        if self.font_obj.size(chunk)[0] > max_width:
                            chunks.append(last_chunk)
                            chunk = word+" "

                    chunks.append(chunk)

                print(chunks)
                        
                text_surface = pygame.Surface((max_width, height*len(chunks)), pygame.SRCALPHA)
                
                for i in range(len(chunks)):
                    chunk_surface = self.font_obj.render(chunks[i], False, self.color)
                    text_surface.blit(chunk_surface, (0, height*i))
                solved = True
            else:
                solved = False
            
        if not solved:
            text_sorted = sorted(text, key = lambda e: self.font_obj.size(e))
            if len(text_sorted)>1:
                input(text_sorted)
            text_surface = pygame.Surface((self.font_obj.size(text_sorted[-1])[0], height*len(text)), pygame.SRCALPHA)
            for i in range(len(text)):
                chunk_surface = self.font_obj.render(text[i], False, self.color)
                text_surface.blit(chunk_surface, (0, height*i))
        
        if surface:
            surface.blit(text_surface, pos)
        else:
            return text_surface

hinwil_fp = "res/others/hinwil.ttf"
class Hinwil(Text):
    def __init__(self, size = 10, color = (255,255,255)):
        Text.__init__(self, size, hinwil_fp, color)

heart_fp = "res/others/heart.ttf"
class Heart(Text):
    def __init__(self, size = 10, color = (255,255,255)):
        Text.__init__(self, size, heart_fp, color)

class Outlined_arial():
    def __init__(self, size = 10, color = (255,255,255)):            
        font_fp = arial_fp
        self.color = color
        self.text_obj = Text(size, font_fp)
        self.in_text_obj = Text(size, font_fp, color=color)
        
    def get_text(self, text):        
        surface_size = list(self.text_obj.font_obj.size(text))
        surface_size[0] += 2
        surface_size[1] += 2
        
        text_surface = pygame.Surface(surface_size, pygame.SRCALPHA)
        for pos in [(0,1),(2,1),(1,0),(1,2)]:
            self.text_obj.get_text(text, pos, surface = text_surface)
            
        self.in_text_obj.get_text(text, (1,1), surface = text_surface)

        return text_surface




        


