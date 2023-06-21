import pygame
import colores
import random
import os

#directorios
#directorio carpeta principal
carpeta_juego = os.path.dirname(__file__)

#directorio de imagenes
#directorio de imagenes principal
carpeta_imagenes = os.path.join(carpeta_juego,"imagenes")
#subdirectorio de imagenes
carpeta_imagenes_enemigos = os.path.join(carpeta_imagenes,"enemigos")
carpeta_imagenes_fondos = os.path.join(carpeta_imagenes,"fondos")
carpeta_imagenes_jugador = os.path.join(carpeta_imagenes,"jugador")
carpeta_imagenes_explosiones = os.path.join(carpeta_imagenes,"explosiones")
#directorios de sonido
#directorio de sonido principal
carpeta_sonidos = os.path.join(carpeta_juego,"sonidos")
#subdirectorios de sonido
carpeta_sonidos_ambiente = os.path.join(carpeta_sonidos,"ambiente")
carpeta_sonidos_armas = os.path.join(carpeta_sonidos,"armas")
carpeta_sonidos_explosiones = os.path.join(carpeta_sonidos,"explosiones")


#Tamaño de pantalla
ANCHO = 800
ALTO = 600

#FPS
FPS = 30

#fuentes
consolas = pygame.font.match_font('consolas')
times = pygame.font.match_font('times')
arial = pygame.font.match_font('arial')
courier = pygame.font.match_font('courier')
#sonidos
pygame.mixer.init()
pygame.mixer.Sound("sonidos/armas/laserShoot.wav")
laser = pygame.mixer.Sound(os.path.join(carpeta_sonidos_armas,"laserShoot.wav"))
explosion1 = pygame.mixer.Sound(os.path.join(carpeta_sonidos_explosiones,"explosion1.wav"))
explosion2 = pygame.mixer.Sound(os.path.join(carpeta_sonidos_explosiones,"explosion1.wav"))
ambiente = pygame.mixer.Sound(os.path.join(carpeta_sonidos_ambiente,"Quake2.ogg"))
tecla = pygame.mixer.Sound(os.path.join(carpeta_sonidos_ambiente,"tecla.wav"))

ambiente.play()

import pygame
import sys

def obtener_nombre_jugador():
    pygame.init()

    # Configuración de la ventana
    ventana = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Ingresar Nombre")

    # variable para almacenar el nombre ingresado
    nombre = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                tecla.play()
                if event.key == pygame.K_RETURN:
                    # si el jugador presiona enter, finaliza la entrada del nombre
                    return nombre
                elif event.key == pygame.K_BACKSPACE:
                    # si el jugador presiona la tecla de retroceso, elimina un caracter del nombre
                    nombre = nombre[:-1]
                else:
                    # Agrega el caracter ingresado al nombre
                    nombre += event.unicode

        # Limpiar la pantalla
        ventana.fill(colores.BLACK)

        # Dibujar el campo de texto
        fuente = pygame.font.Font(courier, 32)
        texto = fuente.render(nombre, True, colores.WHITE)
        ventana.blit(texto, (100,50))

        texto_adicional = "Luego de su nombre, intro para continuar..."
        fuente_adicional = pygame.font.Font(None, 24)
        texto_renderizado = fuente_adicional.render(texto_adicional, True, colores.WHITE)
        ventana.blit(texto_renderizado, (30, 20))

        # Actualizar la ventana
        pygame.display.flip()
# Obtener el nombre del jugador antes de iniciar el juego
nombre_jugador = obtener_nombre_jugador()



class Jugador(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (jugador)
        self.image = pygame.image.load(os.path.join(carpeta_imagenes_jugador,"nave.png")).convert()
        self.image.set_colorkey(colores.WHITE)
        self.image = pygame.transform.scale(self.image,(50,60))
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        #circulo de pruebas
        self.radius = 20
        #pygame.draw.circle(self.image,colores.GREEN,self.rect.center,self.radius)
        # Centra el rectángulo (sprite)
        self.rect.center = (400,520)
        #velocidad inicial del PJ
        self.velocidad_x = 0
        #disparos
        self.cadencia = 150
        self.ultimo_disparo = pygame.time.get_ticks()
        self.hp = 100

    def update(self):
        #velocidad predeterminada en cada vuelta del bucle si no pulsas nada
        self.velocidad_x = 0
        #teclas pulsadas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -15
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = 15
        
        if teclas[pygame.K_SPACE]:
            ahora = pygame.time.get_ticks()
            #tiempo actual menos tiempo del ultimo disparo
            if ahora - self.ultimo_disparo > self.cadencia:
                #llamo al metodo disparo
                self.disparo()
                self.ultimo_disparo = ahora

        #actualiza la velocidad del personaje
        self.rect.x += self.velocidad_x 
        #limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0
        #limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

    def disparo(self):
        bala = Disparos(self.rect.centerx, self.rect.top)
        balas.add(bala)
        laser.play()

class EnemigoFacil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(carpeta_imagenes_enemigos, "enemigo.png")).convert()
        self.image.set_colorkey(colores.BLACK)
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(100 - self.rect.height)
        self.velocidad_x = random.randrange(1, 5)
        self.velocidad_y = random.randrange(1, 5)
        self.hp = 20
        self.cadencia = 1000
        self.ultimo_disparo = pygame.time.get_ticks()

    def disparo(self):
        bala_enemiga = DisparosEnemigos(self.rect.centerx, self.rect.bottom)
        balas_enemigas.add(bala_enemiga)

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        #limita el margen izquierdo
        if self.rect.left < 0:
            self.velocidad_x += 1
        #limita el margen derecho
        if self.rect.right > ANCHO:
            self.velocidad_x -= 1
        #limita el margen arriba
        if self.rect.top < 0:
            self.velocidad_y += 1
        #limita el margen abajo
        if self.rect.bottom > ALTO:
            self.velocidad_y -= 1

        # Verificar si es momento de disparar
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia:
            self.disparo()
            self.ultimo_disparo = ahora

    


class EnemigoMedio(pygame.sprite.Sprite):
    # Sprite del enemigo
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (enemigo)
        self.image = pygame.image.load(os.path.join(carpeta_imagenes_enemigos,"enemigo22.png")).convert()
        self.image.set_colorkey(colores.WHITE)
        self.image = pygame.transform.scale(self.image,(50,60))
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(colores.WHITE)
        #circulo de pruebas
        self.radius = 40
        #pygame.draw.circle(self.image,colores.RED1,self.rect.center,self.radius)
        
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(100 - self.rect.height)
        self.velocidad_x = random.randrange(4,12)
        self.velocidad_y = random.randrange(4,12)
        self.hp = 30 
        self.cadencia = 600
        self.ultimo_disparo = pygame.time.get_ticks()

    def disparo(self):
        bala_enemiga = DisparosEnemigos(self.rect.centerx, self.rect.bottom)
        balas_enemigas.add(bala_enemiga)

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        #limita el margen izquierdo
        if self.rect.left < 0:
            self.velocidad_x += 1
        #limita el margen derecho
        if self.rect.right > ANCHO:
            self.velocidad_x -= 1
        #limita el margen arriba
        if self.rect.top < 0:
            self.velocidad_y += 1
        #limita el margen abajo
        if self.rect.bottom > ALTO:
            self.velocidad_y -= 1

        # Verificar si es momento de disparar
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia:
            self.disparo()
            self.ultimo_disparo = ahora

    

class EnemigoDificil(pygame.sprite.Sprite):
    # Sprite del enemigo
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (enemigo)
        self.image = pygame.image.load(os.path.join(carpeta_imagenes_enemigos,"enemigo33.png")).convert()
        self.image.set_colorkey(colores.WHITE)
        self.image = pygame.transform.scale(self.image,(50,60))
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(colores.WHITE)
        #circulo de pruebas
        self.radius = 15
        
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(100 - self.rect.height)
        self.velocidad_x = random.randrange(6,15)
        self.velocidad_y = random.randrange(6,15)
        self.hp = 60
        self.cadencia = 400
        self.ultimo_disparo = pygame.time.get_ticks()

    def disparo(self):
        bala_enemiga = DisparosEnemigos(self.rect.centerx, self.rect.bottom)
        balas_enemigas.add(bala_enemiga)

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        #limita el margen izquierdo
        if self.rect.left < 0:
            self.velocidad_x += 1
        #limita el margen derecho
        if self.rect.right > ANCHO:
            self.velocidad_x -= 1
        #limita el margen arriba
        if self.rect.top < 0:
            self.velocidad_y += 1
        #limita el margen abajo
        if self.rect.bottom > ALTO:
            self.velocidad_y -= 1

        # Verificar si es momento de disparar
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia:
            self.disparo()
            self.ultimo_disparo = ahora

class Disparos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(carpeta_imagenes_jugador,"laser.png")).convert(),(5,10))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
    def update(self):
        self.rect.y -= 50
        if self.rect.bottom < 0:
            self.kill()

class DisparosEnemigos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(carpeta_imagenes_jugador,"laser.png")).convert(),(5,10))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
    def update(self):
        self.rect.y += 10
        if self.rect.bottom < 0:
            self.kill()

class Explosiones(pygame.sprite.Sprite):
    def __init__(self,centro,dimensiones):
        pygame.sprite.Sprite.__init__(self)
        self.dimensiones = dimensiones
        self.image = animacion_explosion[self.dimensiones][0]
        self.rect = self.image.get_rect()
        self.rect.center = centro
        self.fotograma = 1
        self.frecuencia_fotograma = 80
        self.actualizacion = pygame.time.get_ticks()

    def update(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.actualizacion > self.frecuencia_fotograma:
            self.actualizacion = ahora
            self.fotograma += 1
            if self.fotograma == len(animacion_explosion[self.dimensiones]):
                self.kill()
            else:
                centro = self.rect.center
                self.image = animacion_explosion[self.dimensiones][self.fotograma]
                self.rect = self.image.get_rect()
                self.rect.center = centro

# Inicialización de Pygame, creación de la ventana, título y control de reloj.
#pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))

#puntuaciones
puntuacion = 0

#explosiones
animacion_explosion = {'size1':[],'size2':[]}
for i in range(7):
    archivo_explosiones = f"{i+1}.png"
    imagenes = pygame.image.load(os.path.join(carpeta_imagenes_explosiones,archivo_explosiones)).convert()
    imagenes.set_colorkey(colores.WHITE)
    
    imagenes_size1 = pygame.transform.scale(imagenes,(40,40))
    animacion_explosion["size1"].append(imagenes_size1)
    imagenes_size2 = pygame.transform.scale(imagenes,(80,80))
    animacion_explosion["size2"].append(imagenes_size2)

def barra_hp(pantalla,x,y,hp):
    largo = 200
    ancho = 25
    calculo_barra = int((jugador.hp / 100) * largo)
    borde = pygame.Rect(x,y,largo,ancho)
    rectangulo = pygame.Rect(x,y,calculo_barra,ancho)
    pygame.draw.rect(pantalla,colores.GREEN1 ,borde,3)
    pygame.draw.rect(pantalla,colores.GREENYELLOW,rectangulo)
    pantalla.blit(pygame.transform.scale(jugador.image,(30,30)),(545,15))
    warning = pygame.image.load(os.path.join(carpeta_imagenes_jugador, "warning.png")).convert()
    warning.set_colorkey(colores.BLACK)

    if jugador.hp < 0:
        jugador.hp = 0
    if jugador.hp < 30:
        pantalla.blit(pygame.transform.scale(warning,(30,30)),(545,15)) 
        

def muestra_texto(pantalla, fuente, texto, color, dimensiones, x, y, texto2):
    tipo_letra = pygame.font.Font(fuente, dimensiones)
    superficie_texto = tipo_letra.render(texto, True, color)
    rectangulo_texto = superficie_texto.get_rect()
    rectangulo_texto.center = (x, y)
    pantalla.blit(superficie_texto, rectangulo_texto)

    superficie_texto2 = tipo_letra.render(texto2, True, color)
    rectangulo_texto2 = superficie_texto2.get_rect()
    rectangulo_texto2.right = rectangulo_texto.left - 30
    rectangulo_texto2.centery = rectangulo_texto.centery
    pantalla.blit(superficie_texto2, rectangulo_texto2)


def guardar_puntajes(puntajes, nombre_jugador):
    with open("puntajes.txt", "a") as archivo:
        archivo.write(f"Jugador: {nombre_jugador}, Puntaje: {puntajes}\n")

def muestra_score():
    with open("puntajes.txt", "r") as archivo:
        contenido = archivo.read()
    print(contenido)

fondo = pygame.transform.scale(pygame.image.load(os.path.join(carpeta_imagenes_fondos,"fondo.jpg")).convert(),(1000,1000))
pygame.display.set_caption("Jueguito")
clock = pygame.time.Clock()

#Grupo de sprites, instanciación del objeto jugador.
sprites = pygame.sprite.Group()
enemigos_facil = pygame.sprite.Group()
enemigos_medio = pygame.sprite.Group()
enemigos_dificil = pygame.sprite.Group()
balas = pygame.sprite.Group()
balas_enemigas = pygame.sprite.Group()
explosiones = pygame.sprite.Group()

#instanciacion del personaje
jugador = Jugador()
sprites.add(jugador)


# Bucle de juego
ejecutando = True
while ejecutando:
    # Es lo que especifica la velocidad del bucle de juego
    clock.tick(FPS)
    # Eventos
    for event in pygame.event.get():
        # Se cierra y termina el bucle
        if event.type == pygame.QUIT:
            ejecutando = False

    # Actualización de sprites
    sprites.update()
    enemigos_facil.update()
    enemigos_medio.update()
    enemigos_dificil.update()
    balas.update()
    balas_enemigas.update()
    explosiones.update()

    colision_dispares_facil_jugador = pygame.sprite.spritecollide(jugador,balas_enemigas,True,pygame.sprite.collide_circle)
    if colision_dispares_facil_jugador:
        jugador.hp -= 20
        explosion1.play()

    colision_dispares_medio_jugador = pygame.sprite.spritecollide(jugador,balas_enemigas,True,pygame.sprite.collide_circle)
    if colision_dispares_medio_jugador:
        jugador.hp -= 30
        explosion1.play()

    colision_dispares_dificil_jugador = pygame.sprite.spritecollide(jugador,balas_enemigas,True,pygame.sprite.collide_circle)
    if colision_dispares_dificil_jugador:
        jugador.hp -= 50
        explosion1.play()

    colision_disparos_facil = pygame.sprite.groupcollide(enemigos_facil, balas, False, True, pygame.sprite.collide_circle)
    if colision_disparos_facil:
        for enemigo in colision_disparos_facil:
            puntuacion += 10
            explosion1.play()
            explosion = Explosiones(enemigo.rect.center, 'size1')
            explosiones.add(explosion)
            enemigo.hp -= 10
            if enemigo.hp <= 0:
                enemigo.kill()

    colision_disparos_medio = pygame.sprite.groupcollide(enemigos_medio, balas, False, True, pygame.sprite.collide_circle)
    if colision_disparos_medio:
        for enemigo in colision_disparos_medio:
            puntuacion += 50
            explosion1.play()
            explosion = Explosiones(enemigo.rect.center, 'size1')
            explosiones.add(explosion)
            enemigo.hp -= 10
            if enemigo.hp <= 0:
                enemigo.kill()

    colision_disparos_dificil = pygame.sprite.groupcollide(enemigos_dificil, balas, False, True, pygame.sprite.collide_circle)
    if colision_disparos_dificil:
        for enemigo in colision_disparos_dificil:
            puntuacion += 100
            explosion2.play()
            explosion = Explosiones(enemigo.rect.center, 'size2')
            explosiones.add(explosion)
            enemigo.hp -= 10
            if enemigo.hp <= 0:
                enemigo.kill()

    colision_nave_facil = pygame.sprite.spritecollide(jugador,enemigos_facil,True,pygame.sprite.collide_circle)
    if colision_nave_facil:
        explosion1.play()
        explosion = Explosiones(enemigo1.rect.center,'size1')
        explosiones.add(explosion)
        jugador.hp -= 20
        puntuacion -= 100
        if puntuacion < 0:
            puntuacion = 0

    colision_nave_medio = pygame.sprite.spritecollide(jugador,enemigos_medio,True,pygame.sprite.collide_circle)
    if colision_nave_medio:
        explosion1.play()
        explosion = Explosiones(enemigo2.rect.center,'size1')
        explosiones.add(explosion)
        jugador.hp -= 30
        puntuacion -= 75
        if puntuacion < 0:
            puntuacion = 0

    colision_nave_dificil = pygame.sprite.spritecollide(jugador,enemigos_dificil,True,pygame.sprite.collide_circle)
    if colision_nave_dificil:
        explosion2.play()
        explosion = Explosiones(enemigo3.rect.center,'size2')
        explosiones.add(explosion)
        jugador.hp -= 50
        puntuacion -= 25
        if puntuacion < 0:
            puntuacion = 0
    
    if jugador.hp <= 0:
        ejecutando = False

    if not enemigos_facil and not enemigos_medio and not enemigos_dificil:
        
        for i in range(3):
            enemigo1 = EnemigoFacil()        
            enemigos_facil.add(enemigo1)

        for i in range(2):
            enemigo2 = EnemigoMedio()
            enemigos_medio.add(enemigo2)

        enemigo3 = EnemigoDificil()
        enemigos_dificil.add(enemigo3)

    # Fondo de pantalla, dibujo de sprites y formas geométricas.   
    pantalla.blit(fondo,(0,0)) 
    sprites.draw(pantalla)
    enemigos_facil.draw(pantalla)
    enemigos_medio.draw(pantalla)
    enemigos_dificil.draw(pantalla)
    balas.draw(pantalla)
    balas_enemigas.draw(pantalla)
    explosiones.draw(pantalla)

    #dibuja textos en la pantalla
    #def muestra_texto(pantalla, fuente, texto, color, dimensiones, x, y, texto2):
    muestra_texto(pantalla,consolas,str(puntuacion).zfill(7), colores.BLACK, 40, 680, 60,nombre_jugador)
    barra_hp(pantalla,580,15,jugador.hp)
    
    pygame.display.flip()
guardar_puntajes(puntuacion,nombre_jugador)


muestra_score()
pygame.quit()
