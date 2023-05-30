import pygame as pg
import sys
def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_imgs = pg.transform.flip(pg.image.load("fig/pg_bg.jpg"),True,False)
    kk_img = pg.transform.flip(pg.image.load("fig/3.png"),True,False)
    kk_imgs = [kk_img,pg.transform.rotozoom(kk_img,2,1.0),pg.transform.rotozoom(kk_img,4,1.0),pg.transform.rotozoom(kk_img,6,1.0),pg.transform.rotozoom(kk_img,8,1.0),pg.transform.rotozoom(kk_img,10,1.0),pg.transform.rotozoom(kk_img,8,1.0),pg.transform.rotozoom(kk_img,6,1.0),pg.transform.rotozoom(kk_img,4,1.0),pg.transform.rotozoom(kk_img,2,1.0)]

    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        tmr += 1
        screen.blit(bg_img, [54-tmr, 0])
        screen.blit(bg_imgs,[1600-tmr,0])
        screen.blit(bg_img,[3200-tmr,0])
        screen.blit(kk_imgs[tmr%10],[300,200])

        pg.display.update()
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()