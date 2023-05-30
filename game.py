import pygame as pg
import sys
import random

WIDTH = 1600
HEIGHT = 900


def check_bound(area: pg.Rect, obj: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj.left < area.left or area.right < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < area.top or area.bottom < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, +1),
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        self.image = pg.transform.flip(pg.image.load("ex05/fig/3.png"), True, False)

        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 10

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                self.rect.move_ip(mv)
        if check_bound(screen.get_rect(), self.rect) != (True, True):
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rect.move_ip(-mv[0], -mv[1])
        
        screen.blit(self.image, self.rect)


class Coin(pg.sprite.Sprite):
    """
    コインに関するクラス
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づきコインSurfaceを生成する
        引数1 color：コインの色タプル
        引数2 rad：コインの半径
        """
        super().__init__()
        self.image = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH-30, random.randint(0, HEIGHT))
        self.vx, self.vy = +1, +1

    def update(self):
        self.rect.move_ip(-1, 0)


class Bonus(pg.sprite.Sprite):
    """
    ボーナスコインに関するクラス
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づきボーナスコインSurfaceを生成する
        引数1 color：ボーナスコインの色タプル
        引数2 rad：ボーナスコインの半径
        """
        super().__init__()
        self.image = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, 450)
        self.vx = +1

    def update(self):
        self.rect.move_ip(-1, 0) 


class Enemy(pg.sprite.Sprite):
    """
    敵機に関するクラス
    """
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(f"ex05/fig/alien1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH-40, random.randint(0, HEIGHT))

    def update(self):
        self.rect.move_ip(-1, 0)


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    bg_imgs = pg.transform.flip(bg_img, True,False)

    bird = Bird([100, 200])
    coins = pg.sprite.Group()
    bonusC = pg.sprite.Group()
    emys = pg.sprite.Group()

    tmr = 0
    flag = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        # フラグに応じてコインの生成を制御
        if not flag and tmr % 700 == 0:
            for i in range(3):
                coins.add(Coin((255, 0, 0), 30))

        # フラグに応じて敵機の生成を制御
        if not flag and tmr % 700 == 0:
            emys.add(Enemy())

        if tmr % 3000 == 0:
            flag = False
        elif tmr % 7000 == 0:
            flag = True
            coins.empty()  # コインの削除
            emys.empty()  # 敵機の削除
        
        if flag and tmr % 7000 == 0:
            bonusC.add(Bonus((0, 255, 0), 200))
        
        tmr += 1
        x = tmr%3200
        screen.blit(bg_img,[-x, 0])
        screen.blit(bg_imgs, [1600-x, 0])
        screen.blit(bg_img, [3200-x, 0])

        if flag and len(pg.sprite.spritecollide(bird, bonusC, True)) != 0:
            flag = False

        # 工科丸とコインの衝突判定
        if len(pg.sprite.spritecollide(bird, coins, True)) != 0:
            pg.display.update()

        # 工科丸とボーナスコインの衝突判定
        if len(pg.sprite.spritecollide(bird, bonusC, True)) != 0:
            pg.display.update()

        # 工科丸と敵機の衝突判定
        if len(pg.sprite.spritecollide(bird, emys, True)) != 0:
            pg.display.update()
            return

        # コインが外に出たら削除
        for coin in coins:
            if False in check_bound(screen.get_rect(), coin.rect):
                coin.kill()
        # 敵機が外に出たら削除
        for emy in emys:
            if False in check_bound(screen.get_rect(), emy.rect):
                emy.kill()
        
        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)
        coins.update()
        coins.draw(screen)
        bonusC.update()
        bonusC.draw(screen)
        emys.update()
        emys.draw(screen)
        pg.display.update()
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()