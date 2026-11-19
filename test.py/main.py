import io

import pygame
import constantes
from personaje import Personaje
from textos import DamageText
from weapons import Weapons
from items import Item
import os

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, ((w * scale), h * scale))
    return nueva_imagen

def contar_elementos(directorio):
    return len(os.listdir(directorio))

def nombres_carpetas(directorio):
    return os.listdir(directorio)

pygame.init()
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

pygame.display.set_caption("Scooby doo pa pa y el bum bum bum bum")

font = pygame.font.Font("assets/fonts/m6x11.ttf", 25)

corazon_vacio = pygame.image.load("assets/images/characters/items/heart_empty.png")
corazon_vacio = escalar_img(corazon_vacio, constantes.SCALA_CORAZON)
corazon_mitad = pygame.image.load("assets/images/characters/items/heart_half.png")
corazon_mitad = escalar_img(corazon_mitad, constantes.SCALA_CORAZON)
corazon_lleno = pygame.image.load("assets/images/characters/items/heart_full.png")
corazon_lleno = escalar_img(corazon_lleno, constantes.SCALA_CORAZON)


animaciones = []
for i in range(1):
    imagen = pygame.image.load(f"assets//images//characters//player//player_{i}.png")
    imgen = escalar_img(imagen, constantes.SCALA_PERSONAJE * 0.5)
    animaciones.append(imgen)

directorio_enemigos = "assets/images/characters/enemies"
cantidad_enemigos = contar_elementos(directorio_enemigos)
animaciones_enemigos = []
lista_tipos_enemigos = nombres_carpetas(directorio_enemigos)

for eni in lista_tipos_enemigos:
    lista_temporal = []
    ruta_temp = f"assets/images/characters/enemies/{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        im_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i + 1}.png").convert_alpha()
        im_enemigo = escalar_img(im_enemigo, constantes.SCALA_ENEMIGOS)
        lista_temporal.append(im_enemigo)
    animaciones_enemigos.append(lista_temporal)

player_image = pygame.image.load("assets//images//characters//player//player_0.png")
player_image = escalar_img(player_image, constantes.SCALA_PERSONAJE)

imagen_pistola = pygame.image.load("assets/images/characters/weapons/gun.png")
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARMA)

imagen_balas = pygame.image.load("assets/images/characters/weapons/bullet.png")
imagen_balas = escalar_img(imagen_balas, constantes.SCALA_ARMA)

posion_roja = pygame.image.load("assets/images/characters/items/potion.png")
posion_roja = escalar_img(posion_roja, 0.3)

coin_images = []
ruta_img = "assets/images/characters/coins"
num_coin_images = contar_elementos(ruta_img)
for i in range(num_coin_images):
    img = pygame.image.load(f"assets/images/characters/coins/coin_{i + 1}.png")
    img = escalar_img(img, constantes.SCALA_MONEDA)
    coin_images.append(img)
    
def vida_jugador():
    c_mitad_dibujado = False
    for i in range(4):
        if jugador.energia >= ((i + 1) * 25):
            ventana.blit(corazon_lleno, (5+i*50, 5))
        elif jugador.energia % 25 > 0 and c_mitad_dibujado == False:
            ventana.blit(corazon_mitad, (5+i*50, 5))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio, (5+i*50, 5))

jugador = Personaje(50, 50, animaciones, 20)

hormiga = Personaje(400, 300, animaciones_enemigos[0], 100)
pato = Personaje(200, 200, animaciones_enemigos[1], 100)

lista_enemigos = []
lista_enemigos.append(hormiga)
lista_enemigos.append(pato)


pistola = Weapons(imagen_pistola, imagen_balas)

grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()

coin = Item(250, 25, 0, coin_images)
potion = Item(380, 55, 1, [posion_roja])

grupo_items.add(coin)
grupo_items.add(potion)

mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

reloj = pygame.time.Clock()

run = True
while run == True:

    reloj.tick(constantes.FPS)
    ventana.fill(constantes.COLOR_BG)

    delta_x = 0 
    delta_y = 0

    if mover_derecha == True:
        delta_x = constantes.VELOCIDAD
    if mover_izquierda == True:
        delta_x = -constantes.VELOCIDAD
    if mover_arriba == True:
        delta_y = -constantes.VELOCIDAD
    if mover_abajo == True:
        delta_y = constantes.VELOCIDAD

    jugador.movimiento(delta_x, delta_y)

    jugador.update()

    for ene in lista_enemigos:
        ene.update()

    bala = pistola.update(jugador)
    if bala:
        grupo_balas.add(bala)
    for bala in grupo_balas:
        damage, pos_damage = bala.update(lista_enemigos)
        if damage:
            damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constantes.ROJO)
            grupo_damage_text.add(damage_text)

    grupo_damage_text.update()

    grupo_items.update()


    jugador.dibujar(ventana)

    for ene in lista_enemigos:
        ene.dibujar(ventana)

    grupo_damage_text.draw(ventana)
    grupo_items.draw(ventana)

    pistola.dibujar(ventana)

    for bala in grupo_balas:
        bala.dibujar(ventana)

    vida_jugador()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    pygame.display.update()

pygame.quit()