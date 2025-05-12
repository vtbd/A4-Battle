from collections.abc import Callable
import pygame
import os.path

def loadimagefromfile(file: str, pos: tuple[float], mode: tuple[int]= (1, 1), size: tuple[float]|float=(-1, -1), alpha: bool = False, notfound: str='res/picture_not_found.png') -> tuple[pygame.Surface, pygame.Rect]:
    surf = pygame.image.load(file) if os.path.exists(file) else pygame.image.load(notfound)
    if type(size) == tuple:
        alsize = list(size)
        if -1 in size:
            if size[0] == -1:
                alsize[0] = surf.get_width()
            if size[1] == -1:
                alsize[1] = surf.get_height()
        alsize = tuple(alsize)
        if size != (-1, -1):
            surf = pygame.transform.scale(surf, alsize)
    elif type(size) in (float, int):
        if size != 1:
            surf = pygame.transform.scale(surf, (surf.get_width()*size, surf.get_height()*size))
        alsize = surf.get_size()
    else:
        raise TypeError
    if alpha:
        surf = surf.convert_alpha()
    else:
        surf = surf.convert()
    rect = surf.get_rect(center=tuple(pos[i]+alsize[i]*mode[i]//2 for i in range(2)))
    return surf, rect

class Moving:
    def __init__(self, time, func: Callable[[int], tuple[float, float]]):
        self._time = time
        self._func = func

    def next(self) -> tuple[int, tuple[float, float]]:
        if self._time >= 1:
            self._time -= 1
            return (1, self._func(self._time))
        else:
            return (0, (0, 0))

class Movings:
    def __init__(self):
        self._movinglist:list[Moving] = []
    
    def newmove(self, moving_t: Moving) -> None:
        self._movinglist.append(moving_t)

    def next(self) -> tuple[float, float]:
        movementsum = (0, 0)
        for i, move in enumerate(self._movinglist.copy()):
            movement = move.next()
            if movement[0] == 0:
                del self._movinglist[i]
            else:
                movementsum = tuple([movement[1][j] + movementsum[j] for j in range(2)])
        return movementsum
 

class PlaObj:
    def __init__(self) -> None:
        self._movability = False
        self._movement = (0, 0)

    def move(self, offset: tuple[float, float]):
        if self._movability:
            self._movement = tuple(self._movement[i] + offset[i] for i in range(2))

    def movenext(self):
        self.move(self._movings.next())

    def newmoving(self, moving: Moving):
        self._movings.newmove(moving)

    def setpos(self, pos: tuple[float], mode: tuple[int] = (1, 1)) -> None:
        '''mode: 
        1: left/top
        0:center
        -1: right/bottom'''
        self._rect.center = tuple(pos[i]+self._rect.size[i]*mode[i]/2 for i in range(2))

    def getabspos(self):
        if self.objtype == 'root':
            return (0, 0)
        pabs = self._parent.getabsrect().topleft
        return tuple(pabs[i] + self._rect.topleft[i] + (self.movement[i] if self.movability else 0) for i in range(2))

    def getrect(self) -> pygame.Rect:
        return self._rect
    
    def setrect(self, rect_t: pygame.Rect) -> None:
        self._rect = rect_t

    def getabsrect(self) -> pygame.Rect:
        newrect = self._rect.copy()
        newrect.topleft = self.getabspos()
        if self.movability == False:
            return newrect
        return newrect.move(*self.movement)

    def getparent(self):
        return self._parent
    
    def setparent(self, parent_t) -> None:
        self._parent = parent_t

    def getmovability(self) -> bool:
        return self._movability
    
    def setmovability(self, movability_t) -> None:
        self._movability = movability_t
        if movability_t:
            self._movings = Movings()
            self._movement = (0, 0)
        else:
            self._movings = []

    def getmovement(self) -> tuple[int]:
        return self._movement

    def setmovement(self, movement_t):
        self._movement = movement_t

    rect = property(getrect, setrect)
    absrect = property(getabsrect)
    parent = property(getparent, setparent)
    movability = property(getmovability, setmovability)
    movement = property(getmovement, setmovement)


class RootObj(PlaObj):
    objtype = 'root'
    def __init__(self, w: float, h: float):
        self._rect = pygame.Rect(0, 0, w, h)
        self._movability = False
        self._movement = (0, 0)


class ImageObj(PlaObj):
    objtype = 'image'
    def __init__(self, screen: pygame.Surface, parent_t: PlaObj, file: str|pygame.Surface|int, pos: tuple[float], mode: tuple[int]= (1, 1), size: tuple[float]=(-1, -1), alpha: bool = False, notfound=None) -> None:
        '''mode: 1: l/h 0:c -1: r/d'''
        self.parent = parent_t
        self._screen = screen
        if type(file) == str:
            self.setimagefromfile(file, pos, mode, size, alpha, notfound)
        elif type(file) == pygame.Surface:
            self._surf = file.copy()
            self._rect = self._surf.get_rect(center=tuple(pos[i]+self._surf.get_size()[i]*mode[i]//2 for i in range(2)))
        elif type(file) == int and file == 0:
            self._surf = pygame.Surface((0, 0))
            self._rect = self._surf.get_rect(center=tuple(pos[i] for i in range(2)))
        else:
            raise TypeError
        self._movability = False
        self._movement = (0, 0)

    def setimagefromfile(self, file: str, pos: tuple[float], mode: tuple[int]= (1, 1), size: tuple[float]=(-1, -1), alpha: bool = False, notfound=None) -> None:
        if notfound is None:
            self._surf, self._rect = loadimagefromfile(file, pos, mode, size, alpha)
        else:
            self._surf, self._rect = loadimagefromfile(file, pos, mode, size, alpha, notfound)
        self._originalsurf = self._surf.copy()
        self._originalrect = self._rect.copy()

    def draw(self) -> None:
        self.screen.blit(self._surf, self.absrect)

    def regress(self) -> None:
        self.surf = self._originalsurf.copy()
        self.rect = self._originalrect.copy()

    def getsurf(self) -> pygame.Surface:
        return self._surf
    
    def setsurf(self, surf_t: pygame.Surface) -> None:
        self._surf = surf_t

    def getscreen(self) -> pygame.Surface:
        return self._screen

    surf = property(getsurf, setsurf)
    screen = property(getscreen)


class MtpApprObj(ImageObj):
    objtype = 'mtpappr'
    def setimagelist(self, images:list[str], align:int = 0, attrs:list[tuple] = None, alpha=False, notfound=None) -> None:
        '''When align is 0 (default), the new images aligns with the top and left of the initial picture; \n
        when align is 1, the new images aligns with the center of the initial picture; \n
        when align is 2, the position and size of the new images will be given in sequence in the list attrs, \n
        with each item correspond to the arguments of the function loadimagefromfile'''
        self._imagecount = len(images)
        if align == 0:
            pos = self.rect.topleft
            self._imagelist = [loadimagefromfile(image, pos, alpha=alpha) for image in images]
        elif align == 1:
            pos = self.rect.center
            self._imagelist = [loadimagefromfile(image, self.rect.center, (0, 0), alpha=alpha) for image in images]
        elif align == 2:
            self._imagelist = [loadimagefromfile(image, *attrs[i]) for i, image in enumerate(images)]
        self._imageserial = -1
        self._movability = False
        self._movement = (0, 0)


    def refresh(self):
        if self._imageserial == -1:
            self.regress()
        else:
            self.surf = self._imagelist[self._imageserial][0]
            self.rect = self._imagelist[self._imageserial][1]

    def next(self) -> int:
        """
        Moves to the next image in the sequence and returns the index of the new image.
        Returns:
            int: The index of the new image.
        """

        if self._imageserial == -1:
            return -1
        elif self._imageserial == (self._imagecount - 1):
            self._imageserial = 0
        else:
            self._imageserial += 1
        self.refresh()
        return self._imageserial
    
    def setappr(self, seri:int) -> None:
        self._imageserial = seri
        self.refresh()

    def start(self, seri:int = 0) -> None:
        self._imageserial = seri
        self.refresh()

    def end(self):
        self._imageserial = -1
        self.refresh()
        


class ButtonObj(MtpApprObj):
    objtype = 'button'
    def __init__(self, screen: pygame.Surface, parent_t: PlaObj, file: str|pygame.Surface, pos: tuple[float], mode: tuple[int]= (1, 1), size: tuple[float]=(-1, -1), alpha: bool = False) -> None:
        super().__init__(screen, parent_t, file, pos, mode, size, alpha)
        self.__status = 0

    def setalternatepicture(self, file: str, pos: tuple[float], mode: tuple[int]= (1, 1), size: tuple[float]=(-1, -1), alpha: bool = False) -> None:
        self.__alternatesurf, self.__alternaterect = loadimagefromfile(file, pos, mode, size, alpha)

    def surveil(self, pos: tuple[float]) -> bool:
        if self.__status in (0, 1):
            if self.absrect.collidepoint(pos):
                return True
        return False

    def surveil_hover(self, pos: tuple[float]) -> None:
        if self.__status in (0, 1):
            if self.absrect.collidepoint(pos):
                if self.__status == 0:
                    self.__status = 1
                    self.surf = self.__alternatesurf
                    self.rect = self.__alternaterect
            else:
                if self.__status == 1:
                    self.__status = 0
                    self.regress()

    def surveil_click(self, pos: tuple[float]) -> bool:
        if self.__status in (0, 1):
            if self.absrect.collidepoint(pos):
                self.__status = 2
                self.start()
                return True
        return False
    
    def update(self):
        if self.__status == 2:
            if self.next() == 0:
                self.end()
                self.__status = 0

class LayoutObj(PlaObj):
    objtype = 'layout'
    def __init__(self, parent_t: PlaObj, pos: tuple[float], mode: tuple[int]= (1, 1), size: tuple[float]=(0, 0)) -> None:
        self.parent = parent_t
        self._rect = pygame.Rect(tuple(pos[i]+size[i]*mode[i]//2 for i in range(2)), size)


class TextImagifier:
    def __init__(self, screen: pygame.Surface, parent_t: PlaObj, font: pygame.font.Font, text: str, color: tuple[int], pos: tuple[float], mode: tuple[int]= (1, 1), length:float=-1, height:float=-1) -> None:
        self._parent = parent_t
        self._screen = screen
        self._font = font
        self._text = text
        self._color = color
        self._pos = pos
        self._mode = mode
        self._length = length
        self._height = height

    def imagify(self) -> ImageObj:
        if self._length == -1:
            surf = self._font.render(self._text, True, self._color)
            return ImageObj(self._screen, self._parent, surf, self._pos, self._mode, alpha=True)
        if self._length != -1:
            h0 = self._font.size(self._text)[1]
            h = h0 if self._height == -1 else self._height
            l = 0
            n = 0
            textlist = []
            for i in range(1, len(self._text)+1):
                if self._text[i-1] == '\n':
                    textlist.append(self._text[l:i])
                    l = i
                    n += 1
                elif self._font.size(self._text[l:i])[0] > self._length:
                    if i-l == 1:
                        raise ValueError('Length set too small')
                    else:
                        textlist.append(self._text[l:i-1])
                        l = i-1
                        n += 1
            textlist.append(self._text[l:])
            surf = pygame.Surface((self._length, h*n+h0), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 0))
            for n, singletext in enumerate(textlist):
                singlesurf = self._font.render(singletext, True, self._color)
                surf.blit(singlesurf, singlesurf.get_rect(topleft=(0, h*n)))
            return ImageObj(self._screen, self._parent, surf, self._pos, self._mode, alpha=True)
    
    def getcolor(self):
        return self._color
    
    def setcolor(self, color):
        self._color = color

    def gettext(self) -> tuple[int]:
        return self._text

    def settext(self, text_t):
        self._text = text_t

    text = property(gettext, settext)
    color = property(getcolor, setcolor)


class ObjSet:
    def __init__(self, objs:list[PlaObj]):
        self._objs = objs.copy()

    def updateall(self):
        for obj in self._objs:
            if obj.movability:
                obj.movenext()
            match obj.objtype:
                case 'root':
                    pass
                case 'image':
                    obj.draw()
                case 'mtpappr':
                    obj.next()
                    obj.draw()
                case 'button':
                    obj.update()
                    obj.draw()