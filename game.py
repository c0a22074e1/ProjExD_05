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


class Difficulty_level:
    """
    ゲームの難易度に関するクラス
    """
    def __init__(self, level: str):
        """
        ゲームの難易度を設定・難易度を表示する
        引数：難易度の名前
        """
        self.level = level
        self.color = (0, 0, 0)
        self.font = pg.font.Font(None, 50)
        self.image = self.font.render(f"level: {self.level}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH-150, HEIGHT-50
        self.flag = 0
        self.str_flag = 0
        self.count = 700

    def change_level(self, change_level: str, count: int):
        """
        ゲームの難易度を変更する
        引数１：変更する難易度の名前
        引数２：敵機の出現する間隔
        """
        self.level = change_level
        self.str_flag = 1 #  難易度を一度変更すると再び変更できなくする
        self.count = count

    def update(self, screen: pg.Surface):
        """
        ゲーム難易度を表示する
        引数：画面Surfase
        """
        self.image = self.font.render(f"level: {self.level}", 0, self.color)
        screen.blit(self.image, self.rect)


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
        self.speed = 5

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                self.rect.move_ip(mv[0], +self.speed * mv[1])
        if check_bound(screen.get_rect(), self.rect) != (True, True):
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rect.move_ip(mv[0], -self.speed * mv[1])
        
        screen.blit(self.image, self.rect)

class Score:
    """
    コインの得た数をスコアとして表示する
    銀:10点
    金:20点
    """
    def __init__(self):
        self.font = pg.font.Font(None, 40)
        self.color = (255, 128, 0)
        self.score = 0
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH - 100, 30
        self.flag = 0

    def score_up(self, add):
        self.score += add

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)


class Coin(pg.sprite.Sprite):
    """
    コインに関するクラス
    """
    image = [1, 2, 2, 2]
    a = 0
    def __init__(self, score: Score):
        super().__init__()
        self.count = random.choice(__class__.image)
        if self.count == 1:
            self.image = pg.image.load("ex05/fig/coin.png")
            self.image = pg.transform.rotozoom(self.image,0,0.5)
            score.flag = 1
        else:
            self.image = pg.image.load("ex05/fig/coin_silver.png")
            self.image = pg.transform.rotozoom(self.image,0,0.1)
            score.flag = 2
            #print(self.image)
        self.image.set_colorkey((255, 255, 255))  # 白の背景を透過
        
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH-100,random.randint(0, HEIGHT)
        if __class__.a == 2:
            self.rect.center = WIDTH-200,random.randint(0, HEIGHT)
        #print(a, self.rect.center)
        self.vx, self.vy = -6, 0 
        
    def update(self):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下
        引数 screen：画面Surface
        """
        self.rect.centerx += self.vx




class Bonus(pg.sprite.Sprite):
    """
    ボーナスコインに関するクラス
    """
    img = pg.image.load("ex05/fig/coin_b.png")

    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づきボーナスコインSurfaceを生成する
        引数1 color：ボーナスコインの色タプル
        引数2 rad：ボーナスコインの半径
        """
        super().__init__()
        self.image = Bonus.img
        self.image.set_colorkey((255, 255, 255))  # 白の背景を透過
        self.image = pg.transform.rotozoom(self.image,0,2.0)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, 450)
        self.vx = +1

    def update(self):
        self.rect.move_ip(-1, 0) 


class Enemy1(pg.sprite.Sprite):
    """
    敵機に関するクラス
    """
    imgs = [pg.image.load(f"ex05/fig/alien{i}.png") for i in range(1, 4)]
    
    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH-50,random.randint(0, HEIGHT)
        self.vx = random.randint(1,5)

        
    def update(self, diff_level: Difficulty_level):
        if diff_level.flag == 2:
            self.vx = random.randint(6, 10)
        if diff_level.flag == 3:
            self.speed  = random.randint(11, 15)
        self.rect.centerx -= self.vx


class Life(pg.sprite.Sprite): #残機に関するクラス
    def __init__(self):

        self.life=2

        super().__init__()
        self.image = pg.image.load(f"ex05/fig/0.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH-40, (HEIGHT-50))


    def decrease_life(self):
        self.life-=1

class Enemy2(pg.sprite.Sprite):
    """
    変則型敵機に関するクラス
    """
    imgs = [pg.image.load(f"ex04/fig/alien{i}.png") for i in range(1, 4)]
    
    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.image = pg.transform.rotozoom(self.image,0,2.0)  #敵機のサイズ二倍

        self.rect = self.image.get_rect()
        self.rect.center = random.randint(1200, WIDTH), 100
        self.vy = +6
        self.vx = random.randint(2, 5)
        self.bound = random.randint(50, HEIGHT)  # 停止位置

    def update(self, diff_level: Difficulty_level):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下
        """
        tmr = 0
        
        if diff_level.flag == 2:
            self.vx = random.randint(6, 10)
        if diff_level.flag == 3:
            self.speed  = random.randint(9, 12)
        self.rect.centery += self.vy
        if self.rect.centery > self.bound:
            self.vy = 0
            while True:
                tmr += 1
                if tmr % 10000 == 0:
                    self.rect.centerx -= self.vx
                    tmr = 0
                    break


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    life_img=pg.image.load("ex05/fig/0.png")
    bg_imgs = pg.transform.flip(bg_img, True,False)
    score = Score()
    diff_level = Difficulty_level("normal")
    bird = Bird([100, 200])
    coins = pg.sprite.Group()
    bonusC = pg.sprite.Group()
    emys1 = pg.sprite.Group()  # 敵機のグループ
    emys2 = pg.sprite.Group()  # 変則型敵機
    game_life=Life()

    tmr = 0
    flag = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_2 and diff_level.str_flag == 0:
                diff_level.change_level("Hard", 650)
                diff_level.flag = 1 #  難易度に対応したフラグを立てる
            if event.type == pg.KEYDOWN and event.key == pg.K_3 and diff_level.str_flag == 0:
                diff_level.change_level("Lunatic", 600)
                diff_level.flag = 2

        # フラグに応じてコインの生成を制御
        if not flag and tmr % 300 == 0:
            coins.add(Coin(score))
        if not flag and tmr % 500 == 0:
            coins.add(Coin(score))

        # フラグに応じて敵機の生成を制御
        if not flag and tmr % diff_level.count == 0:
            emys1.add(Enemy1())
            emys1.add(Enemy1())
        if not flag and tmr % (diff_level.count/2) == 0:    
            emys2.add(Enemy2())
            emys2.add(Enemy2())

        if tmr % 3000 == 0:
            flag = False
        elif tmr % 7000 == 0:
            flag = True
            coins.empty()  # コインの削除
            emys1.empty()  # 敵機の削除
            emys2.empty()  # 変則型敵機の削除

        
        if flag and tmr % 7000 == 0:
            bonusC.add(Bonus((0, 255, 0), 200))
        
        tmr += 1
        x = tmr%3200
        screen.blit(bg_img,[-x, 0])
        screen.blit(bg_imgs, [1600-x, 0])
        screen.blit(bg_img, [3200-x, 0])

        if game_life.life==2: #ライフに応じて表示を変更
            screen.blit(life_img,[1440,750])
            screen.blit(life_img,[1480,750])
            screen.blit(life_img,[1520,750])
        if game_life.life==1:
            screen.blit(life_img,[1480,750])
            screen.blit(life_img,[1520,750])
        if game_life.life==0:
            screen.blit(life_img,[1520,750])

        if flag and len(pg.sprite.spritecollide(bird, bonusC, True)) != 0:
            flag = False

        # 工科丸とコインの衝突判定
        if len(pg.sprite.spritecollide(bird, coins, True)) != 0:
            diff_level.count -= 2
            if score.flag == 1:
                score.score_up(20) 
            else:
                score.score_up(10)
            #pg.display.update()

        # 工科丸とボーナスコインの衝突判定
        if len(pg.sprite.spritecollide(bird, bonusC, True)) != 0:
            diff_level.count -= 5
            score.score_up(100)
            #pg.display.update()

        # 工科丸と敵機の衝突判定
        if len(pg.sprite.spritecollide(bird, emys1, True)) != 0:
            if game_life.life>0:
                pg.display.update()
                game_life.decrease_life()
                pg.display.update()
                print(game_life.life)

            else:
                pg.display.update()
                return
        
        # 工科丸と変則型敵機の衝突判定
        if len(pg.sprite.spritecollide(bird, emys2, True)) != 0:
            if game_life.life>0:
                pg.display.update()
                game_life.decrease_life()
                pg.display.update()
                print(game_life.life)

            else:
                pg.display.update()
                return

        # コインが外に出たら削除
        for coin in coins:
            if False in check_bound(screen.get_rect(), coin.rect):
                coin.kill()
                #print(0)
        # 敵機が外に出たら削除
        for emy in emys1:
            if False in check_bound(screen.get_rect(), emy.rect):
                emy.kill()
        # 敵機が外に出たら削除
        for emy in emys2:
            if False in check_bound(screen.get_rect(), emy.rect):
                emy.kill()
        
        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)
        
        bonusC.update()
        bonusC.draw(screen)
        emys1.update(diff_level)
        emys1.draw(screen)
        emys2.update(diff_level)
        emys2.draw(screen)
        diff_level.update(screen)
        coins.update()
        coins.draw(screen)
        score.update(screen)
        pg.display.update()
        clock.tick(100)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()