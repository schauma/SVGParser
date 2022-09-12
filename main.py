import os
import xml.etree.ElementTree as ET
import numpy as np
DATA_PATH = "simple.svg"

# Need to calculate that
MM_PER_STEP = 1
MM_PEN_WIDTH = 0.7


class Path():

    def __init__(self, target, usePen, style):
        self.target = target
        self.usePen = usePen
        self.style = style

    def set_curve(self, start, curve, usePen, style):
        pass

    def __repr__(self):
        drawn = " Drawn" if self.usePen else " Not Drawn"
        return "\n" + str(self.target) + drawn


class ParseError(NameError):
    pass


def formDict(strList):
    tplist = [x.split(":") for x in strList]
    for tp in tplist:
        try:
            tp[1] = float(tp[1])
        except ValueError:
            pass

    ret = dict(tplist)
    return ret


def filterDict(dic, char):
    ret = {}
    for key, value in dic.items():
        newKey = key[key.find(char) + 1:]
        try:
            ret[newKey] = float(value)
        except ValueError:
            ret[newKey] = value

    assert (len(dic) == len(ret))

    return ret


def driveToStart(posX, posY, listofPaths):
    p = Path((posX, posY), False, None)
    listofPaths.append(p)


def drawRect(obj, style, listofPaths):
    posX = float(obj.attrib["x"])
    posY = float(obj.attrib["y"])
    width = float(obj.attrib["width"])
    height = float(obj.attrib["height"])
    driveToStart(posX, posY, listofPaths)
    p1 = Path((posX + width, posY), True, None)
    p2 = Path((posX + width, posY + height), True, None)
    p3 = Path((posX, posY + height), True, None)
    p4 = Path((posX, posY), True, None)

    listofPaths.extend([p1, p2, p3, p4])

    if style["fill"] is not "none":
        pass


def drawEllipse(obj, style, listofPaths):
    pass


def drawPath(obj, style, listofPaths):
    pass


def parseObj(obj):
    obj.attrib = filterDict(obj.attrib, "}")
    style = obj.attrib["style"].split(";")
    style = formDict(style)
    return obj, style


def main():
    listOfPaths = []

    svgNamespace = ".//{http://www.w3.org/2000/svg}"
    tree = ET.parse(DATA_PATH)
    root = tree.getroot()
    graphics = root.find(svgNamespace + "g")

    for obj in graphics:
        obj, style = parseObj(obj)
        entity = obj.tag[obj.tag.find("}") + 1:]

        if entity == "path":
            drawPath(obj, style, listOfPaths)
        elif entity == "ellipse":
            drawEllipse(obj, style, listOfPaths)
        elif entity == "rect":
            drawRect(obj, style, listOfPaths)
        else:
            raise ParseError

    print(listOfPaths)


if __name__ == "__main__":
    main()
