import numpy as np
import math
import pygame as pg


class PnmImage:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.storage = []

    def getNpArray(self) -> np.array:
        return np.array(self.storage)


def imageFromFile(path: str) -> PnmImage:
    with open(path, "rb") as file:
        file.readline()
        sizes = file.readline().split()
        image = PnmImage(int(sizes[0]), int(sizes[1]))
        file.readline()
        for i in range(image.y):
            line = file.readline().split()
            image.storage.append([])
            for j in range(image.x):
                image.storage[i].append(int(line[j]))
        return image


def imageFromBinaryFile(path: str) -> PnmImage:
    with open(path, "rb") as file:
        file.read(3)
        byte = file.read(1)
        x = 0
        while byte != b" ":
            x *= 10
            x += int(byte)
            byte = file.read(1)

        byte = file.read(1)
        y = 0
        while byte != b"\n":
            y *= 10
            y += int(byte)
            byte = file.read(1)

        file.read(4)  # 255\n
        image = PnmImage(x, y)
        for i in range(y):
            image.storage.append([])
            for j in range(x):
                r = file.read(1)
                image.storage[i].append(int.from_bytes(r, "little", signed=False))

        return image


def displayTogether(images: list[PnmImage]) -> None:
    PIXEL_SIZE = 1
    n = math.ceil(math.sqrt(len(images)))
    WIN_SIZE = [
        images[0].x * n * PIXEL_SIZE,
        PIXEL_SIZE * images[0].y * ((len(images) + n - 1) // n),
    ]
    pg.init()
    win = pg.display.set_mode(WIN_SIZE, pg.RESIZABLE)
    fake_win = win.copy()
    x = 0
    y = 0
    for image in images:
        for i in range(image.y):
            for j in range(image.x):
                pg.draw.rect(
                    fake_win,
                    (image.storage[i][j], image.storage[i][j], image.storage[i][j]),
                    (x + j * PIXEL_SIZE, y + i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                )

        win.blit(pg.transform.scale(fake_win, win.get_rect().size), (0, 0))
        pg.display.update()

        x += images[0].x * PIXEL_SIZE
        if x >= WIN_SIZE[0]:
            x = 0
            y += images[0].y * PIXEL_SIZE

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        win.blit(pg.transform.scale(fake_win, win.get_rect().size), (0, 0))
        pg.display.flip()
