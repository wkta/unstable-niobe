import os

import demolib.dialogue as dialogue
import katagames_engine as kengi
from defs import MyEvTypes


pygame = kengi.pygame
evmodule = kengi.event
CgmEvent = kengi.event.CgmEvent


class Character(kengi.isometric.model.IsometricMapObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.name = "PC"
        self.surf = pygame.image.load("assets/sys_icon.png").convert_alpha()

    def __call__(self, dest_surface, sx, sy, mymap):
        mydest = self.surf.get_rect(midbottom=(sx, sy))
        dest_surface.blit(self.surf, mydest)


class Door(kengi.isometric.model.IsometricMapObject):
    def bump(self):
        # Call this method when the PC bumps into this portal.
        if "dest_map" in self.properties:
            dest_map = int(self.properties.get("dest_map", 0))
            dest_door = self.properties.get("dest_door")
            # lets use the event manager, so we achive low-coupling
            evmodule.EventManager.instance().post(
                CgmEvent(MyEvTypes.MapChanges, new_map=dest_map, gate_name=dest_door)
            )


class GlowingPortal(Door):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)
        self.surf = pygame.image.load("assets/portalRings2.png").convert_alpha()
        self.frame = 0

    def __call__(self, dest_surface, sx, sy, mymap):
        mydest = pygame.Rect(0,0,32,32)
        mydest.midbottom = (sx, sy)
        dest_surface.blit(self.surf, mydest, pygame.Rect(self.frame*32,0,32,32))
        self.frame = (self.frame + 1) % 5


class NPC(kengi.isometric.model.IsometricMapObject):
    def bump(self):
        # Call this method when the PC bumps into this NPC.
        if "conversation" in self.properties:
            conversation_ongoing = True
            myconvo = dialogue.Offer.load_json(os.path.join("assets", self.properties["conversation"]))
            evmodule.EventManager.instance().post(
                CgmEvent(MyEvTypes.ConvStarts, convo_obj=myconvo, portrait=self.properties.get("portrait"))
            )


class Terminal(kengi.isometric.model.IsometricMapObject):
    def bump(self):
        # Call this method when the PC bumps into this terminal.
        pass


OBJECT_CLASSES = {
    "Door": Door,
    "NPC": NPC,
    "GlowingPortal": GlowingPortal,
    "Terminal": Terminal
}