from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.collision import *
import random

janela = Window(1080, 720)
teclado = Window.get_keyboard()
fundo = GameImage("png/fundo_jogo_3.png")
janela.set_title("Vampiro Carioca")

player = Sprite("png/player.png")
player.set_position(460, 460)

def spawn_mob(listacoordenadas): #spawn de mobs aleatórios, com suas posições definidas pra fora do mapa
    listamob = [Sprite("png/zumbi.png"), Sprite("png/esqueleto.png"), Sprite("png/policial.png")]
    i = random.randint(0, 2)
    mob = listamob[i]
    coordenadas = random.choice(listacoordenadas)
    mob.set_position(coordenadas[0], coordenadas[1])
    return mob

def colision_tiro_mob(listamob, listatiro): #testa a colisão do tiro do player com os mobs
    if listamob != [] and listatiro != []:
        for m in listamob:
            for t in listatiro:
                if Collision.collided(m, t):
                    listamob.remove(m)
                    listatiro.remove(t)
                if t.x > janela.width:
                    listatiro.remove(t)

def mov_tiros(listatiros):
    if listatiros != []:
        for t in listatiros:
            t.draw()
    if listatiros != []:
        for t in listatiros:
            t.move_x(velTiro * janela.delta_time())

velplayer = 200
velmob = 50

matMob = []
timerMob = 0
timervelocidade = 0

matTiros = []
velTiro = 50
timerhit = 0

listacoordenadas = [[-25, -25], [-25, janela.height/2], [-25, janela.height + 25], [janela.width/2, janela.height + 25],  
                    [janela.width + 25, -25], [janela.width + 25, janela.height/2], [janela.width + 25, janela.height + 25], 
                    [janela.width/2, - 25]]

while True:

    #CONTADORES
    timervelocidade += janela.delta_time()
    timerMob += janela.delta_time()
    timerhit += janela.delta_time()

    #INCREMENTADOR DE VELOCIDADE
    if timervelocidade > 30:
        velmob = velmob + 20
        timervelocidade = 0

    #MOVIMENTAÇÃO E SPAWN DOS TIROS
    if teclado.key_pressed("w"):
        if player.y - 1 > 0: 
            player.move_y(janela.delta_time() * -velplayer)
    if teclado.key_pressed("s"):
        if player.y + 1 < janela.height - player.height: 
            player.move_y(janela.delta_time() * velplayer)
    if teclado.key_pressed("a"):
        if player.x - 1 > 0: 
            player.move_x(janela.delta_time() * -velplayer)
    if teclado.key_pressed("d"):
        if player.x + 1 < janela.width - player.width: 
            player.move_x(janela.delta_time() * velplayer)
    if teclado.key_pressed("space") and timerhit > 0.3:
            tiro = Sprite("png/moeda.png")
            tiro.set_position(player.x, player.y+player.height/2)
            matTiros.append(tiro)
            timerhit = 0

    #SPAWN E MOVIMENTAÇÃO MOBS
    if timerMob > 1:
        matMob.append(spawn_mob(listacoordenadas))
        timerMob = 0

    if matMob != []:
        for z in matMob:
            z.draw()

    if matMob != []:
        for z in matMob:
            if z.x > player.x:
                z.move_x(janela.delta_time() * -velmob)
            else:
                z.move_x(janela.delta_time() * velmob)
            if z.y > player.y:
                z.move_y(janela.delta_time() * -velmob)
            else:
                z.move_y(janela.delta_time() * velmob)

    #MOVIMENTAÇÃO E COLISÃO DOS TIROS DO PLAYER
    mov_tiros(matTiros)
    colision_tiro_mob(matMob, matTiros)

    #DESENHA INFORMAÇÕES AÍ
    janela.draw_text(str(timervelocidade) + " SEG",0,0,16,(255,255,255))
    janela.draw_text(str(velmob) + " PIXEL/SEG",0,20,16,(255,255,255))

    janela.update()
    fundo.draw()
    player.draw()