import math
import pickle
import pygame
import os
from pygame.sprite import Sprite
from pygame.locals import *

#######################################################################
#main idea for this program is it will load a system and display a    #
#simulation on how it should look. Using the parents position and the #
#bodies own information it will recursively generate their positions. #
#I will also include a way to generate a system from user input.      #
#######################################################################


#TODO
#save/load needs refinement and a user interface
#A way to use sprites as the planets instead of monocolor circles
#Improve user interface the skeleton of this program is pretty much done just missing
######a lot of QOL features
#follow method needs refinement add a way for the user to enter a body to follow
#create a gui for creating and editing systems using the terminal is cumbersom
def main():

    config = Config("config.txt")
    config.load()
    cons = Console(config)

    debug = bool(config.retrieve("is_debug"))

    #sysbuild = SystemBuilder(debug)

    #sysbuild.loadSystem("solarTest.pk1")

    cons.run()

    #runSim(sysbuild.getSystem())


#####################################################################################
#Allow for the camera to move either follow a body or be moved by arrows            #
#This will be achieved by having a set of system coordinates and camera coordinates #
#Will only need to draw things within the frame but could probably manage to render #
#the whole thing at once this isn't that intensive                                  #
#####################################################################################
def runSim(sysIn):
    print("RUN SIM")
    global FPS, clock, screen, WIDTH, HEIGHT
    FPS = 60
    WIDTH, HEIGHT = 1200, 1000

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    run = True
    cam = Camera(WIDTH, HEIGHT)

    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key==K_a:
                    cam.x += 5
                elif event.key==K_d:
                    cam.x += -5
                elif event.key==K_w:
                    cam.y += 5
                elif event.key==K_s:
                    cam.y += -5
                elif event.key==K_t:
                    cam.text = not cam.text
            if event.type==KEYUP:
                if event.key==K_a:
                    cam.x += 0
                elif event.key==K_d:
                    cam.x += 0
                elif event.key==K_w:
                    cam.y += 0
                elif event.key==K_s:
                    cam.y += 0

        screen.fill((0,0,0))
        sysIn.update()
        #TODO
        #test for follow method needs to be fixed
        #cam.follow(sysIn.getBody("earth"))
        sysIn.draw(cam)
        pygame.display.update()
        clock.tick(FPS)



#used to build and then save a system
#could also be used to load a system instead
#building is currently working but I still need a way to save it
#as well as load it
class SystemBuilder():

    def __init__(self, db=False):
        self.systemName = None
        self.currSystem = None

        if (db):
            self.SystemName = "Solar"
            self.currSystem = System(self.systemName)
            self.testBuild()

    def buildSystem(self, sysName=""):
        keepRun = True;

        if(sysName != ""):
            self.systemName = sysName
            self.currSystem = System(self.systemName)
        else:
            self.systemName = input("enter system name: ")
            self.currSystem = System(self.systemName)

        #section for adding primary star
        print("this is the primary star of the system ")
        rotSpeed = input("enter rot speed: ")
        bodyName = input("enter body name: ")
        radius = input("enter planetary radius: ")


        body = Body(bodyName, "null", int(radius), float(0), float(0), float(rotSpeed))

        self.currSystem.addBody(body)

        print("Add first body to system")

        while(keepRun):
            parentName = input("enter parent name: ")

            if(parentName == "null"):
                orbitalRadius = 0
                startRad = 0
            else:
                orbitalRadius = input("enter orbital radius: ")
                startRad = input("enter start radians: ")

            rotSpeed = input("enter rot speed; ")
            bodyName = input("enter body name: ")
            radius = input("enter planetary radius: ")


            body = Body(bodyName, parentName, int(radius), float(orbitalRadius), float(startRad), float(rotSpeed))

            self.currSystem.addBody(body)

            addAnother = input("add another body (y/n?): ")

            if (addAnother == "n"):
                keepRun = False
                print(self.currSystem.systemToString())

        saveSys = input("Save System (y/n)")

        if (saveSys == "y"):
            if(self.systemName != "" and self.systemName != None):
                self.saveSystem(self.systemName)
            else:
                sysName = input("enter system name: ")
                self.saveSystem(sysName)

    def editSystem(self):
        keepRun = True;

        if(self.currSystem == None):
            print("Cannot edit an empty system please add a new one: ")
            return

        print(self.systemName)
        print(self.currSystem.systemToString())

        while(keepRun):
            parentName = input("enter parent name: ")

            if(parentName == "null"):
                orbitalRadius = 0
                startRad = 0
            else:
                orbitalRadius = input("enter orbital radius: ")
                startRad = input("enter start radians: ")

            rotSpeed = input("enter rot speed; ")
            bodyName = input("enter body name: ")
            radius = input("enter planetary radius: ")


            body = Body(bodyName, parentName, int(radius), float(orbitalRadius), float(startRad), float(rotSpeed))

            self.currSystem.addBody(body)

            addAnother = input("add another body (y/n?): ")

            if (addAnother == "n"):
                keepRun = False
                print(self.currSystem.systemToString())

        saveSys = input("Save System (y/n)")

        if (saveSys == "y"):
            if(self.systemName != "" and self.systemName != None):
                self.saveSystem(self.systemName)
            else:
                sysName = input("enter system name: ")
                self.saveSystem(sysName)

    def getSystem(self):
        return (self.currSystem)

    def saveSystem(self, fileName):
        if fileName[len(fileName)-4:] != ".pk1":
            fileName += ".pk1"

        with open(fileName, 'wb') as output:
            pickle.dump(self.currSystem, output, pickle.HIGHEST_PROTOCOL)

    def loadSystem(self, fileName):
        e = None

        try:
            f = open(fileName, 'rb')
        except OSError:
            print ("Could not open/read file:", fileName)
            return e

        with open(fileName, "rb") as input_file:
            e = pickle.load(input_file)
            self.currSystem = e
            return e
            

    def testBuild(self):
        body1 = Body("Sol", "null", 100, 0, 0, 0, (255,255,0))
        bodyp1 = Body("Mercury", "Sol", 7, 150, 10, .5, (169,169,169))
        bodyp2 = Body("Venus", "Sol", 5, 230, 5, .2, (255,140,0))
        bodyp3 = Body("Earth", "Sol", 10, 350, 3, .125, (95,158,160))
        bodyp3m1 = Body("Moon", "Earth", 5, 30, 3, .5, (211,211,211))
        bodyp4 = Body("Mars", "Sol", 6, 400, 8, .2, (255,0,0))


        self.currSystem.addBody(body1)
        self.currSystem.addBody(bodyp3)
        self.currSystem.addBody(bodyp3m1)
        self.currSystem.addBody(bodyp1)
        self.currSystem.addBody(bodyp2)
        self.currSystem.addBody(bodyp4)

        self.saveSystem("solarTest.pk1")

        #testSys = self.load_system("solarTest.pk1")
        #print(testSys.systemToString())

        #self.currSystem.printSystem()
        #print(self.currSystem.systemToString())

###################################################################################################
#Camera class will be used to help with the drawing of objects and should allow for a moving view #
###################################################################################################
class Camera():

    def __init__(self, sWidth, sHeight):
        self.center = (sWidth//2, sHeight//2)
        self.x = sWidth//2
        self.y = sHeight//2
        self.zoom = 1 #zoom factor how far out the camera iis
        self.text = True

    def getCoords(self):
        return((self.x, self.y))

    #method designed to follow the body passed to it, currently works needs a better way of being
    #called
    def follow(self, bodyIn, toFollow = False):
        if(toFollow):
            self.x = -bodyIn.x + self.center[0]
            self.y = -bodyIn.y + self.center[1]


################################################################################
#System: will need to add System coordinates in order to get the camera working#
#correctly. Add a System max size and then find a way to pass information to   #
#the graphics handler                                                          #
################################################################################
class System():

    def __init__(self, name):
        self.name = name
        self.root = None
        #bodies is a hashmap of celeestial bodies with key=body, value= children
        self.bodies = {}

    #def addBody(self, bodyIn, parentName):
    #    if(parentName == "null" or parentName == "root"):
    #        bodyIn.setRoot()
    #        self.bodies[bodyIn.name.lower()] =  bodyIn
    #        self.root = bodyIn
    #    else:
    #        print("added " + bodyIn.name + " as child of " + parentName)
    #        self.bodies[bodyIn.name.lower()] = bodyIn
    #        self.bodies[parentName.lower()].addChild(bodyIn)

    #improved add body method, if parent name is not found add it to roots children
    def addBody(self, bodyIn):
        pName = bodyIn.parentName.lower()

        if (pName.lower() == "null" or pName.lower() == "root"):
            bodyIn.setRoot()
            self.bodies[bodyIn.name.lower()] = bodyIn
            self.root = bodyIn
        elif(pName in self.bodies.keys()):
            self.bodies[bodyIn.name.lower()] = bodyIn
            self.bodies[pName.lower()].addChild(bodyIn)
        else:
            self.bodies[bodyIn.name.lower()] = bodyIn
            self.bodies[self.root.name.lower()].addChild(bodyIn)

    #updates the planets positions recursively done through planets
    def update(self):
        self.root.update(self.root.x, self.root.y)

    #draws the objects in system uses camera to calculate object positions
    #could be updated to only draw objects that are in frame
    def draw(self, cam):
        self.root.draw(cam)
        self.drawCamCoords(cam)

    def drawCamCoords(self, cam):
        font = pygame.font.SysFont(None, 24)
        img = font.render("{}, {}".format(int(cam.x), int(cam.y)), True, (0,0,255))
        screen.blit(img, ((cam.center[0]*2) -75, (cam.center[1]*2) -30))

    def printSystem(self):
        print(self.bodies)

    def systemToString(self):
        return(self.root.bodyToString())

    def getBody(self, name):
        return(self.bodies[name.lower()])


#class for a celestial body, really is the meat of the program
#lots of work remaining here still need a way to recursively calculate the positions
#of each body relative to it's parent
class Body():

    #parentPos: position of parent body
    #radius: radius of body used to draw size
    #orbitalRadius: distance from center of parent to center of self
    #startRad: starting radians used to calculate initial pos
    #orbitSpeed: the change in radians per cycle
    def __init__(self, name, parentName, parentPos, radius, orbitalRadius, startRad, orbitSpeed):
        self.name = name
        self.parentName = parentName
        self.radius = int(radius)
        self.orbitalRadius = int(orbitalRadius)
        self.rootSW = False
        self.x, self.y = 0.0, 0.0

        if (parentName.lower() == "null"):
            print("is null")
            self.x, self.y = 0, 0
            rootSW = True
        else:
            self.getPos(startRad)

        self.speed = float(orbitSpeed) * .01
        self.children = []
        self.radians = startRad

    def __init__(self, name, parentName, radius, orbitalRadius, startRad, orbitSpeed, color=(0,0,255)):
        self.name = name
        self.parentName = parentName
        self.radius = radius
        self.orbitalRadius = orbitalRadius
        self.rootSW = False
        self.color = color
        self.x, self.y = 0.0, 0.0

        if (parentName.lower() == "null"):
            self.x, self.y = 0, 0
            self.rootSW = True
        else:
            self.getPos(startRad)

        self.speed = orbitSpeed * .01
        self.children = []
        self.radians = startRad

    def setRoot(self):
        self.root = True

    #updates the body and calls update on all of it's children
    def update(self, parentX, parentY):
        self.radians += self.speed

        if ( self.rootSW == False):
            self.getPos(self.radians)
            self.x += parentX
            self.y += parentY

        for child in self.children:
            child.update(self.x, self.y)

    #used to draw the body, drawn position is different than actual position hence
    #different methods
    def draw(self, cam):

        pygame.draw.circle(screen, self.color, (self.x + (cam.x/cam.zoom) , self.y + (cam.y/cam.zoom )), self.radius*cam.zoom)

        if (cam.text):
            self.drawText(cam)

        for child in self.children:
            child.draw(cam)

    #TODO find a better way to center the text, specifically the body name
    def drawText(self, cam):
        coords = cam.getCoords()

        font = pygame.font.SysFont(None, 24)
        xcord = self.x + (cam.x/cam.zoom) - (self.radius*.15)-20
        ycord = self.y + (cam.y/cam.zoom) - (self.radius * 1.25) -15
        camx , camy = (cam.x/cam.zoom) + self.x, (cam.y/cam.zoom) + self.y

        #draws the planets coords
        img = font.render("{}, {}".format(int(camx), int(camy)), True, (0,0,255))
        screen.blit(img, (xcord, ycord))

        #draws the planets name
        img2 = font.render("{}".format(self.name), True, (0,0,255))
        screen.blit(img2, (xcord, (self.y+ (cam.y/cam.zoom) + self.radius * 1.25 + 15) ))

    def getPos(self, angle):
        self.x = self.orbitalRadius * math.cos(angle)
        self.y = self.orbitalRadius * math.sin(angle)

    def addChild(self, childIn):
        self.children.append(childIn)

    def childrenToString(self):
        outString = ""

        for child in self.children:
            outString += child.bodyToString()

        return (outString)

    def bodyToString(self):
        out = self.name + "\n radius:" + str(self.radius) + "\n orbital radius:" + str(self.orbitalRadius) + "\n x cord: " + str(self.x) + " y cord" + str(self.y) + "\n"
        out += str(self.speed)

        out += "\n{" + self.childrenToString() + "}"

        return (out)

###################################################################################################
#Basic config reader utility. given a file name it will load items from that file splitting on '='#
#it generates a dictionary the desired field name can be retrieved from that.                     #
###################################################################################################
class Config():

    def __init__(self, fname = "null"):
        self.confs = {}
        self.fName = fname

    def load(self, fName = "null"):
        if fName != "null":
            self.fName = fName

        f = open(self.fName, 'r')

        for line in f:
            if (len(line.strip()) > 0):
                l = line.strip().split("=")
                self.confs[l[0]] = l[1]

    def retrieve(self, key):
        return(self.confs[key])

###################################################################################################
#Console class can be used to run the main program, better way of doing things than modifying the #
#config in order to change stuff like I was doing before
#WIP
#TODO add a help command
####change edit to allow for editing of the planets themselves
##################################################################################################
class Console():
    #constructor if config passed builds using that
    def __init__(self, config=None):
        self.config = config
        self.system = None
        self.sysBuild = SystemBuilder(bool(self.config.retrieve("is_debug")))

    def run(self):
        isRunning = True

        while(isRunning):
            inp = input("> ")
            args = inp.split()

            if args[0] == "load":
                self.load(args)
            elif args[0] == "run":
                self.runSim(args)
            elif args[0] == "edit":
                self.edit(args)
            elif args[0] == "save":
                self.save(args)
            elif args[0] == "new":
                self.newSys(args)
            elif args[0] == "help":
                print("commands: \nload\nrun\nedit\nsave")
            else:
                print("command {} not recognized".format(args[0]))

    def load(self, args):
        print("LOAD")
        self.system = self.sysBuild.loadSystem(args[1])

    def runSim(self, args):
        if (self.system != None):
            runSim(self.system)
        else:
            self.system = self.sysBuild.loadSystem(args[1])
            runSim(self.system)

    def edit(self, args):
        if (self.system != None):
            self.sysBuild.editSystem()
            return
        else:
            self.system = self.load(args)
            self.system = self.sysBuild.loadSystem(args[1])
            self.sysBuild.editSystem()

    def save(self, args):
        if (self.system != None):
            if(self.system.systemName != None and self.system.systemName != ""):
                self.sysBuild.saveSystem()
                return
            else:
                sysName = input("Enter system name: ")
                self.system.systemName = sysName
                self.sysbuild/saveSystem()

    def newSys(self, args):
        self.sysBuild.buildSystem(args[1])


if __name__ == "__main__":
    main()
