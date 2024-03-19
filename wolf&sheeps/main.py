import pygame
import sys
import random

class Vlk(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/wolf.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rychlost = 5
        self.body = 0

    def pohyb(self, smer_x, smer_y):
        nova_x = self.rect.x + smer_x * self.rychlost
        nova_y = self.rect.y + smer_y * self.rychlost

        if 0 <= nova_x <= sirka - self.rect.width and 0 <= nova_y <= vyska - self.rect.height:
            self.rect.x = nova_x
            self.rect.y = nova_y

class Ovce(pygame.sprite.Sprite):
    def __init__(self, vlk_skupina):
        super().__init__()
        self.image = pygame.image.load("img/sheep.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.vlk_skupina = vlk_skupina
        self.rychlost = random.uniform(1.0, 3.0)
        self.smer_x = random.choice([-1, 1])
        self.smer_y = random.choice([-1, 1])
        self.reset()

    def pohyb(self):
        self.rect.x += self.smer_x * self.rychlost
        self.rect.y += self.smer_y * self.rychlost

        if self.rect.left < 0 or self.rect.right > sirka:
            self.smer_x = -self.smer_x
        if self.rect.top < 0 or self.rect.bottom > vyska:
            self.smer_y = -self.smer_y

    def reset(self):
        while True:
            self.rect.x = random.randint(30, sirka - 30 - self.rect.width)
            self.rect.y = random.randint(30, vyska - 30 - self.rect.height)

            if pygame.sprite.spritecollideany(self, self.vlk_skupina, pygame.sprite.collide_rect):
                continue 
            else:
                break 

class Vcela(pygame.sprite.Sprite):
    def __init__(self, vlk_skupina):
        super().__init__()
        self.image = pygame.image.load("img/bee.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.vlk_skupina = vlk_skupina
        self.rychlost = random.uniform(4.0, 10.0)
        self.smer_x = random.choice([-1, 1])
        self.smer_y = random.choice([-1, 1])
        self.reset()

    def pohyb(self):
        self.rect.x += self.smer_x * self.rychlost
        self.rect.y += self.smer_y * self.rychlost

        if self.rect.left < 0 or self.rect.right > sirka:
            self.smer_x = -self.smer_x
        if self.rect.top < 0 or self.rect.bottom > vyska:
            self.smer_y = -self.smer_y

    def reset(self):
        self.rect.center = (sirka // 2, vyska // 2)

class Hra:
    def __init__(self):
        self.vlk_skupina = pygame.sprite.Group()
        self.ovce_skupina = pygame.sprite.Group()
        self.vcely_skupina = pygame.sprite.Group()
        self.vlk = Vlk()
        self.vlk_skupina.add(self.vlk)
        self.generuj_ovci()
        self.generuj_vcelu()

    def generuj_ovci(self):
        ovce = Ovce(self.vlk_skupina)
        self.ovce_skupina.add(ovce)

    def generuj_vcelu(self):
        vcela = Vcela(self.vlk_skupina)
        self.vcely_skupina.add(vcela)

    def spust(self):
        hodiny = pygame.time.Clock()
        skore = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            smer_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            smer_y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

            self.vlk.pohyb(smer_x, smer_y)

            for ovce in self.ovce_skupina:
                ovce.pohyb()

            for vcela in self.vcely_skupina:
                vcela.pohyb()

                if pygame.sprite.collide_rect(self.vlk, vcela):
                    self.konec_hry(skore)

            chycene_ovce = pygame.sprite.spritecollide(self.vlk, self.ovce_skupina, True)
            skore += len(chycene_ovce) * 10  

            if chycene_ovce:
                self.generuj_ovci()

            okno.fill((255, 255, 255))
            self.vlk_skupina.draw(okno)
            self.ovce_skupina.draw(okno)
            self.vcely_skupina.draw(okno)

            # Skóre
            font = pygame.font.Font(None, 36)
            text = font.render(f"Skóre: {skore}", True, (0, 0, 0))
            okno.blit(text, (10, 10))

            pygame.display.update()

            hodiny.tick(60)

    def konec_hry(self, skore):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.spust()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            okno.fill((255, 255, 255))
            font = pygame.font.Font(None, 72)
            text = font.render("Konec hry", True, (255, 0, 0))
            okno.blit(text, (sirka // 2 - text.get_width() // 2, vyska // 2 - text.get_height() // 2))

            font = pygame.font.Font(None, 36)
            text = font.render(f"Skóre: {skore}", True, (0, 0, 0))
            okno.blit(text, (sirka // 2 - text.get_width() // 2, vyska // 2 + 50))

            font = pygame.font.Font(None, 24)
            text = font.render("Stiskněte R pro restart, nebo Q pro ukončení", True, (0, 0, 0))
            okno.blit(text, (sirka // 2 - text.get_width() // 2, vyska // 2 + 100))

            pygame.display.update()


pygame.init()


sirka, vyska = 800, 600
okno = pygame.display.set_mode((sirka, vyska))
pygame.display.set_caption('Vlk, slepice a včela')

hra = Hra()
hra.spust()

pygame.quit()
sys.exit()
