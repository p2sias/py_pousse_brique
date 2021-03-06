from .box import Box
import copy

from os import walk
import json


class Map:

    playerStr = 'S'
    boxStr = 'O'

    level = 1
    max_level = 0

    started = True
    finished = False

    game_status = False

    doneBoxes = 0

    box_number = 0
    all_done_boxes = 0

    boxes_loc = []

    boxes_objects = []

    maps = []

    def __init__(self):

        self.getMaps()

        self.game_status = True
        for map in self.maps:
            self.max_level += 1
        self.init_box()

        for boxes in self.boxes_loc:
            for box in boxes:
                self.box_number += 1

    def getMaps(self):
        f = []

        newMaps = []
        newBoxes = []

        orderCpt = 1
        for (dirpath, dirnames, filenames) in walk('./maps/'):
            f.extend(filenames)
            break

        for filePath in f:
            with open('./maps/' + filePath) as file:
                data = json.load(file)

                while not len(newMaps) == len(data['maps']):
                    for map in data['maps']:
                        if map['order'] == orderCpt:
                            orderCpt += 1
                            newBoxes.append(map['boxes'])
                            newMaps.append(map['map'])

            for boxes in newBoxes:
                self.boxes_loc.append(boxes)
            for map in newMaps:
                self.maps.append(map)      

            newBoxes = []
            newMaps = []

    def init_box(self):

        if not len(self.boxes_loc) == len(self.maps):
            print('Maps an Boxes number are different')
            return

        self.boxes_objects = []
        for box_loc in self.boxes_loc[self.level - 1]:
            box = Box(box_loc[1], box_loc[0], self.getMap())
            self.boxes_objects.append(box)

        self.doneBoxes = 0

    def getMap(self):
        return copy.deepcopy(self.maps[self.level-1])

    def applyMap(self, player):
        map = self.getMap()

        map[player.posY][player.posX] = self.playerStr

        newBoxes = []

        for box in self.boxes_objects:
            if not box.on_objective:
                map[box.posY][box.posX] = self.boxStr
                newBoxes.append(box)
            else:
                self.doneBoxes += 1
                self.all_done_boxes += 1

        self.boxes_objects = newBoxes

        if len(self.boxes_objects) < 1 and not self.finished:
            self.nextLevel()

        print('\nNiveau : ' + str(self.level))
        for y in range(len(map)):
            print(*map[y])
        print('_______________________')
        print('* Rejouer le Niveau (r)')
        print('* Recommencer (ctrl + r)')
        print('* Quitter (q)')

        return map

    def playByLevel(self, level):
        if level > self.max_level:
            print("Unknown level " + str(level))
        else:
            self.level = level
            self.finish()
            self.init_box()

    def finish(self):
        self.finished = True

    def endGame(self):
        self.finish()
        self.game_status = False

    def getBoxes(self):
        return self.boxes_objects

    def nextLevel(self):
        if not self.level + 1 > self.max_level:
            self.level += 1
            self.finish()
            self.init_box()
        else:
            self.endGame()
