import os
import random
import pygame
import shutil
import requests
from random import randint
import base64
import time
import ctypes
from pathlib import Path


sizeCube=30
scripts=[]
for p in Path('scripts\\').glob('*.pds'):
    scripts.append(str(p.read_text()).split("!2*6"))
    print(f"{p.name}:\n{scripts[-1]}\n")
print(scripts)
texts=[]
screenW=600
fontTextInGame="candara"
breakpointcount=0
breakpointcountneed=10

screenH=450
code=""
yCube=screenH-30
xCube=screenW//2-15
hp=3
velCube=0
moveDirection=0
cameraRotate=0
cameraZoom=0
cameraX=0
cameraY=0
TextType=""
cameraToPlayer=False
try:
    with open("color.txt", "r") as fh:
        cRgbC = fh.read().split(",")
        fontColor = (int(cRgbC[0]), int(cRgbC[1]), int(cRgbC[2]))
except:
    fontColor = (255,255,255)
def rotate_image(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect().center)
    return rotated_image, new_rect
def transition(to):
    if to==False:
        zoomR=5050
        tmpScreen = pygame.transform.scale(screen, (screenW, screenH))
        for zoom in range(100):

            pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(0, 0, screenW, screenH), 0)
            screen.blit(tmpScreen,(0,0))
            zoomR-=100-zoom
            time.sleep(0.005)
            pygame.draw.circle(screen, (255, 255, 255), (screenW / 2, screenH/2), zoomR)
            pygame.display.flip()
        print(zoomR)
        return

    if to == True:
        zoomR = 0
        for zoom in range(100):
            zoomR += zoom
            time.sleep(0.005)
            pygame.draw.circle(screen, (255, 255, 255), (screenW / 2, screenH / 2), zoomR)
            pygame.display.flip()
        print(zoomR)
        return








def WriteInFakeConsole(finaltexts):

    for finalText in range(len(finaltexts)):
        screen.blit(pygame.font.SysFont("candara", 40).render(finaltexts[finalText], True,
                                                               (255, 255, 255)),
                    (0, finalText * 40))
        pygame.display.flip()
        time.sleep(0.5)
def CharDie():
    global yCube, xCube, velCube, moveDirection, texts, fontColor, breakpointcountneed, breakpointcount,hp
    if hp > 0:
        hp-=1
        PlaySound("die.mp3")
        texts=[]
        return

    # yCube = screenH-50
    # xCube = screenW // 2 - 15
    # velCube = 0
    # moveDirection = 0
    # vsleep(5)
    texts=[]

    render()
    pygame.mixer.pause()
    PlaySound("die.mp3")
    #time.sleep(3)
    for textInd in range(100):
        time.sleep(0.005)
        #vsleep(0.003)
        sizeCube = 30
        mulDirectionCube = 5
        fallVel = 0.5
        mulVelDrawOnCube = 3
        texts.append([xCube + random.randint(0,30), yCube + random.randint(0,30), random.choice(["#","@","%","&"]), 10 + randint(-3, 3), randint(-3, 3)])
        indexText=0
        for text in texts:

            text[3] -= 0.5
            text[1] -= text[3]
            text[0] -= text[4]

            if text[1] >= screenH:
                text[4] = 0
                text[1] = screenH - 20
                text[3] = 0
                if len(text[2]) > 1:
                    for part in range(len(text[2])):
                        texts.append([text[0] + 5 * part, text[1], text[2][part], 10 + randint(-3, 3), randint(-3, 3)])
                    move = True

                texts.pop(indexText)
            indexText += 1
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screenW, screenH), 0)

        pygame.draw.polygon(screen, (255, 45, 45),
                            [[0 + xCube + moveDirection * mulDirectionCube, 0 + yCube + velCube * mulVelDrawOnCube],
                             [sizeCube + xCube + moveDirection * mulDirectionCube,
                              0 + yCube + velCube * mulVelDrawOnCube],
                             [sizeCube + xCube, sizeCube + yCube], [0 + xCube, sizeCube + yCube]])
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, yCube-100+textInd//2, screenW, 100), 0)
        for text in texts:
            screen.blit(pygame.font.SysFont(fontTextInGame, 20).render(str(text[2]), True, (255, 0, 0)), (text[0], text[1]))

        pygame.display.flip()
    time.sleep(2)
    WriteInFakeConsole(["You die!", "", f"You breaks: {breakpointcount}", "", "Thank you for play!"])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

standartDownloadUrl="https://raw.githubusercontent.com/MrCubeCode/PythonInterGame/refs/heads/main/"
exec(open("settings.txt","r",encoding="utf-8").read())

def _get_request(url: str) -> dict:
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
        })
        if response.ok:
            return response.text
        else:
            return {"status_error": True, "message": "Ошибка при получении данных."}
    except requests.exceptions.RequestException as e:
        return {"status_error": True, "message": str(e)}
def UnpackLevel(data):
    global fontColor
    with open("main.py", "w+", encoding='utf-8') as f:
        f.write(data[0])
        print(f"Code is unpack")
    with open("sound.mp3", "wb") as fh:
        fh.write(base64.decodebytes(bytes(data[1], "utf-8")))
        print(f"Music is unpack")
    if len(data)>=3:
        with open("color.txt", "w+") as fh:
            fh.write(f'{data[2].split(",")[0]},{data[2].split(",")[1]},{data[2].split(",")[2]}')

        #fontColor=(int(data[2].split(",")[0]),int(data[2].split(",")[1]),int(data[2].split(",")[2]))
        print(f"Color {fontColor} set")
    else:
        with open("color.txt", "w+") as fh:
            fh.write(f"255,255,255")
    if len(data) >= 4:
        with open("BackGround.png", "wb") as fh:
            fh.write(base64.decodebytes(bytes(data[3], "utf-8")))
            print(f"Back ground is unpack")

        # fontColor=(int(data[2].split(",")[0]),int(data[2].split(",")[1]),int(data[2].split(",")[2]))

    else:
        print("Replase old BackGround")
        with open("BackGround.png", "wb") as fh:
            fh.write(base64.decodebytes(bytes("iVBORw0KGgoAAAANSUhEUgAAAlkAAAHDCAYAAAAX7Q//AAAACXBIWXMAAAsSAAALEgHS3X78AAAIIUlEQVR4nO3WQQ1CUQADwUIQgoHvCSdowxESCB7e3maSGuhpb9d1Pbf9BwDAGd/Htte2t0MBAI753H0JAHCeyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAICAyAIACIgsAIDTtv0AVNkG3+E+q88AAAAASUVORK5CYII=", "utf-8")))

def DownloadLevel(url):
    global fontColor
    try:
        os.remove('replace.py')
        os.remove('main.py')
        os.remove('color.txt')
        os.remove('BackGround.png')
    except:
        print("", end="")
    data=str(_get_request(standartDownloadUrl+url)).split("&*$")
    UnpackLevel(data)

def DownloadLevelFromFile(file):
    global fontColor
    try:
        os.remove('replace.py')
        os.remove('main.py')
        os.remove('color.txt')
        os.remove('BackGround.png')
    except:
        print("",end="")
    with open(f"{file}", "r+", encoding='utf-8') as f:

        data=f.read().split("&*$")
    UnpackLevel(data)

def PlaySound(file):
    try:
        pygame.mixer.Sound(file).play()
    except:
        print("Fail play sound")

breakpointX=random.randint(20,screenW-20)
def render():

    global texts, screenW, screenH, code,xCube,yCube,moveDirection,velCube,fontColor,backGroundImage,hp,breakpointcount,breakpointX,cameraZoom,cameraRotate,cameraX,cameraY,cameraToPlayer
    #time.sleep(0.02)

    mulDirectionCube=5
    fallVel = 0.5
    mulVelDrawOnCube=3
    playerColBox = pygame.Rect(xCube, yCube, sizeCube, sizeCube)
    for codeExec in scripts:
        exec(codeExec[1])
    if cameraToPlayer==True:
        cameraX=-(xCube-screenW/2)
        cameraY=screenH/1.2-yCube

    xCube += moveDirection * mulDirectionCube

    velCube -= fallVel
    if yCube >= screenH - sizeCube:
        if velCube != -fallVel:
            moveDirection = 0
        yCube = screenH - sizeCube
        velCube = 0


    # try:
    #     if screen.get_at((int(xCube+sizeCube//2 + moveDirection), int(yCube))) == (255,255,255):
    #         moveDirection = -moveDirection
    #         velCube += 2
    #
    #
    #     elif  screen.get_at((int(xCube+sizeCube//2+-moveDirection), int(yCube+sizeCube + velCube))) == (255,255,255):
    #         #yCube-=-velCube
    #         if velCube != -fallVel:
    #             moveDirection = 0
    #
    #         velCube = 0
    #
    # except:
    #     print("",end="")
    indexText=0

    yCube -= velCube
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screenW, screenH), 0)
    screen.blit(backGroundImage, (0, 0))
    pygame.draw.polygon(screen, (65, 216, 250),
                        [[0+xCube+moveDirection*mulDirectionCube, 0+yCube+velCube*mulVelDrawOnCube], [sizeCube+xCube+moveDirection*mulDirectionCube, 0+yCube+velCube*mulVelDrawOnCube],
                         [sizeCube+xCube, sizeCube+yCube], [0+xCube, sizeCube+yCube]])
    for text in texts:

        text[3] -= 0.2
        text[1] -= text[3]
        text[0] -= text[4]

        if text[1] >= screenH:
            rangeWake = len(text[2])
            # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screenW, screenH))

            screen.blit(screen, (random.randint(-rangeWake, rangeWake), random.randint(-rangeWake, rangeWake)))
            text[4] = 0
            text[1] = screenH - 20
            text[3] = 0
            if len(text[2].replace(" ","")) > 1:
                for part in range(len(text[2].replace(" ",""))):
                    texts.append([text[0] + 5 * part, text[1], text[2].replace(" ","")[part], 10 + randint(-3, 3), randint(-3, 3)])
                move = True

            texts.pop(indexText)
        indexText+=1
    indextext = 0
    for textcod in code.split("\n")[0:10]:
        screen.blit(pygame.font.SysFont(None, 20).render(str(textcod), True, (100, 100, 100)),
                    (10, 10 + 20 * indextext))
        indextext += 1

    for textIn in range(len(texts)):
        text=texts[textIn]

        screen.blit(pygame.font.SysFont(fontTextInGame, 20).render(str(text[2]), True, fontColor), (text[0], text[1]))
        if playerColBox.collidepoint((text[0], text[1])):

            CharDie()
            break
    breakRect=pygame.Rect(breakpointX,screenH-30,20,20)
    pygame.draw.rect(screen, (255,10,10), breakRect,border_radius=5)
    if playerColBox.colliderect(breakRect):
        pygame.mixer.pause()
        breakpointX = random.randint(20, screenW - 20)
        breakpointcount += 1
        PlaySound("destroy.mp3")
        for wake in range(20):
            rangeWake=3


            screen.blit(screen, (random.randint(-rangeWake,rangeWake), random.randint(-rangeWake,rangeWake)))
            pygame.display.flip()
            time.sleep(0.01)
        pygame.mixer.unpause()

    for codeExec in scripts:
        exec(codeExec[2])
    zoomScreen = pygame.transform.scale(screen, (screenW+cameraZoom, screenH+cameraZoom))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screenW, screenH), 0)
    rotatedScreen=rotate_image(zoomScreen, cameraRotate)
    screen.blit(rotatedScreen[0],((rotatedScreen[1][0]+-cameraZoom/2)+cameraX,(rotatedScreen[1][1]+-cameraZoom/2)+cameraY))
    pygame.display.flip()
    if xCube<=0 or xCube+sizeCube>=screenW:
        moveDirection=-moveDirection
        velCube+=2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if event.key == pygame.K_SPACE and velCube==0:
                velCube=10
                yCube-=3
            elif event.key == pygame.K_SPACE and velCube!=0 and (moveDirection==1 or moveDirection==-1):
                moveDirection*=3

            if event.key == pygame.K_a and velCube==0:
                moveDirection=-1
            if event.key == pygame.K_d and velCube==0:
                moveDirection = 1
        if event.type == pygame.KEYUP:




            if event.key == pygame.K_a and velCube==0:
                moveDirection = 0
            if event.key == pygame.K_d and velCube==0:
                moveDirection = 0
def vcamera(inCam,outCam,inZoom=200,outZoom=200,zero=True):
    global cameraZoom
    if inCam!=0:
        for i in range(inZoom):
            cameraZoom+=1
            vsleep(inCam)
    else:
        cameraZoom += inZoom
    if outCam != 0:
        for i in range(outZoom):
            cameraZoom-=1
            vsleep(outCam)
    else:
        cameraZoom -= outZoom
    if zero==True:
        cameraZoom=0
def vprint(a,b="",c="",d="",e="",end="",sep="",_pos=[5684,-100]):
    global texts,screenW,screenH,code

    #time.sleep(0.1)
    if _pos[0]==5684:
        rand=randint(0,screenW)
        for line in range(len(a.split("\n"))):
            texts.append([rand,_pos[1]+20*line,a.split("\n")[line],0,0])
    else:
        for line in range(len(a.split("\n"))):
            texts.append([_pos[0], _pos[1]+20*line, a.split("\n")[line], 0, 0])


    render()


def vinput(text,_pos=[5684,screenH//2]):
    global texts,screenW,screenH,code
    pygame.mixer.pause()
    time.sleep(0.1)
    if _pos[0]==5684:
        texts.append([randint(0,screenW),_pos[1],f"{text}",0,0])
    else:
        texts.append([_pos[0], _pos[1], f"{text}", 0,0])
    render()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.unpause()
                    return texts[-1][2][len(text):]
                    #vprint("",_pos=_pos)


                elif event.key == pygame.K_BACKSPACE:
                    texts[-1][2] = texts[-1][2][:-1]
                    render()
                else:
                    texts[-1][2] += event.unicode
                    render()


lastTime=0
def vsleep(_timeSleep):
    count=0
    global lastTime
    lastTime=time.time()
    while True:

        count+=1
        render()

        if time.time() >= lastTime+_timeSleep:
            break
    #_pos = []

def end():
    count=0
    global screen,breakpointcountneed,breakpointcount,screenW,screenH,hp
    #breakpointcount=1000


    while texts!=[]:

        render()
        #if count%1000==0:vprint("END FILE!")
    time.sleep(0.01)
    pygame.mixer.pause()
    programmendY=-500
    goStepsCount=500
    for posyplus in range(goStepsCount):

        programmendY+=1 - posyplus/goStepsCount
        pygame.draw.circle(screen,(43, 105, 45),(screenW/2,programmendY),500)

        pygame.draw.circle(screen, (18, 46, 19), (screenW / 2, programmendY), 400)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        time.sleep(0.05)
    if breakpointcount<breakpointcountneed:
        hp = -1
        CharDie()
    for glithnum in range(1000):
        screen.blit(screen, (random.randint(-1,1), random.randint(-1,1)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    time.sleep(0.5)
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,0,screenW,screenH))
    pygame.display.flip()
    WriteInFakeConsole(["You infected this script! (WIN)", "", f"You breaks: {breakpointcount}", "", "Thank you for play!"])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
pygame.init()

pygame.display.set_caption('Visual')
screen = pygame.display.set_mode((screenW, screenH))

exitFromMenu = False

for codeExec in scripts:
    exec(codeExec[0])
if __name__ == '__main__':

    data = str(_get_request(standartDownloadUrl + "Info")).split("&*$")
    levelsList=data[1].split(",")
    selectLevel=0
    with open("icon.png", "wb") as fh:
        fh.write(base64.decodebytes(bytes(data[2], "utf-8")))
    time.sleep(1)
    Icon = pygame.image.load("icon.png")
    Icon = pygame.transform.scale(Icon, (200, 200))
    print(pygame.font.get_fonts())
    transition(True)
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screenW, screenH), 0)
    indextext = 0
    screen.blit(Icon, (0, 0))
    # for textcod in data[0].split("\n"):
    #     screen.blit(pygame.font.SysFont(None, 50).render(str(textcod), True, (255, 255, 255)),
    #                 (210, 10 + 40 * indextext))
    #     indextext += 1
    screen.blit(pygame.font.SysFont(fontTextInGame, 50).render(str("< " + levelsList[selectLevel] + " >"), True,
                                                               (255, 255, 255)),
                (210, 300))

    # screen.blit(pygame.font.SysFont(None, 50).render(str("Level: "+TextType), True, (255, 255, 255)), (0, screenH-50))
    pygame.display.flip()
    transition(False)
    while exitFromMenu==False:


            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screenW, screenH), 0)
            indextext = 0
            screen.blit(Icon, (0, 0))
            # for textcod in data[0].split("\n"):
            #     screen.blit(pygame.font.SysFont(None, 50).render(str(textcod), True, (255, 255, 255)),
            #                 (210, 10 + 40 * indextext))
            #     indextext += 1
            screen.blit(
                pygame.font.SysFont(fontTextInGame, 50).render(str("" + data[0] + ""),
                                                               True, (255, 255, 255)),
                (250, 0))
            screen.blit(pygame.font.SysFont(fontTextInGame, 50).render(str("Inject script:"+levelsList[selectLevel]+""), True, (255, 255, 255)),
                                         (0, 300))

            #screen.blit(pygame.font.SysFont(None, 50).render(str("Level: "+TextType), True, (255, 255, 255)), (0, screenH-50))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_d:
                        selectLevel+=1

                    if event.key == pygame.K_a:
                        selectLevel -= 1
                    if selectLevel>=len(levelsList):
                        selectLevel=len(levelsList)-1
                    if selectLevel<0:
                        selectLevel=0
                    if event.key == pygame.K_RETURN:
                        pygame.display.flip()
                        TextType=levelsList[selectLevel]
                        exitFromMenu = True
                    elif event.key == pygame.K_BACKSPACE:
                        TextType = TextType[:-1]
                    else:
                        TextType += event.unicode
    transition(True)
    DownloadLevel(TextType)

    #render()
    transition(False)
    #time.sleep(10)
    #WriteInFakeConsole(["Loaded main.py","Loaded sound.mp3","Loaded background.png","Loaded color.txt","All loaded"])
    # time.sleep(1)
    # PlaySound("sound.mp3")


    # render()
    #vsleep(10)

    try:


        shutil.copy2('main.py', 'replace.py')
        with open("replace.py", "r+", encoding='utf-8') as f:
            old = f.read()  # read everything in the file
            f.seek(0)  # rewind
            code = old

            f.write("import visual\n" +""
                                       "\n" + old.replace("print", "visual.vprint").replace("input",
                                                                                      "visual.vinput").replace(
                "time.sleep", "visual.vsleep") + "\nvisual.end()")  # write the new line before
        import replace

    except Exception as e:
        print(e)
        pygame.display.set_caption('File not found')

else:
    if ctypes.windll.user32.MessageBoxW(0, "Inject a code?", "Code inject", 4) == 7: exit()
    backGroundImage = pygame.transform.scale(pygame.image.load("BackGround.png"), (screenW, screenH))

    breakpointX = 1000
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screenW, screenH), 0)
    #render()
    transition(False)

    for zoom in range(50):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    cameraToPlayer = True
                    PlaySound("die.mp3")
        cameraZoom=-(500-zoom*10)
        cameraRotate=(500-zoom*10)/10
        try:
            render()
        except:
            print(cameraZoom)
    cameraZoom=0
    cameraRotate=0
    breakpointX=random.randint(0,screenW-30)
    PlaySound("sound.mp3")
