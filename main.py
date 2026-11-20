# ============================================================
# CHESTER
# Juego de plataformas para Android con Kivy
#
# Python 3.8+
# Kivy 2.x
#
# Ejecutar:
#     python main.py
# ============================================================

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import (
    Color,
    Rectangle,
    Ellipse,
    Line,
    Triangle,
    RoundedRectangle
)
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp


# ============================================================
# CONFIGURACIÓN
# ============================================================

WORLD_WIDTH = 4200.0
WORLD_HEIGHT = 600.0

GRAVITY = 0.7
MOVE_SPEED = 5.0
JUMP_FORCE = -14.0

PLAYER_W = 42.0
PLAYER_H = 58.0

ENEMY_W = 40.0
ENEMY_H = 35.0


# ============================================================
# JUEGO
# ============================================================

class ChesterGame(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        self.state = "menu"

        self.lives = 3
        self.coins = 0

        self.player_x = 100.0
        self.player_y = 482.0

        self.vx = 0.0
        self.vy = 0.0

        self.on_ground = True

        self.camera_x = 0.0

        self.controls = {
            "left": False,
            "right": False
        }

        # ----------------------------------------------------
        # PLATAFORMAS
        # ----------------------------------------------------

        self.platforms = [
            # suelo
            (0, 540, 4200, 60),

            # plataformas
            (300, 450, 130, 25),
            (520, 390, 130, 25),
            (750, 330, 130, 25),

            (1050, 440, 150, 25),
            (1300, 370, 150, 25),
            (1550, 300, 150, 25),

            (1850, 440, 140, 25),
            (2100, 380, 140, 25),
            (2350, 320, 140, 25),

            (2650, 450, 180, 25),
            (2950, 390, 150, 25),
            (3200, 330, 150, 25),

            (3500, 450, 170, 25),
            (3800, 380, 150, 25),
            (4000, 300, 130, 25)
        ]

        # ----------------------------------------------------
        # BLOQUES
        # ----------------------------------------------------

        self.blocks = [
            (450, 500, 50, 40),
            (500, 500, 50, 40),

            (900, 500, 50, 40),
            (950, 500, 50, 40),

            (1200, 500, 50, 40),
            (1250, 500, 50, 40),

            (2000, 500, 50, 40),
            (2050, 500, 50, 40),

            (2850, 500, 50, 40),
            (2900, 500, 50, 40),

            (3350, 500, 50, 40),
            (3400, 500, 50, 40)
        ]

        # ----------------------------------------------------
        # CANVAS
        # ----------------------------------------------------

        self.game_canvas = Widget()
        self.add_widget(self.game_canvas)

        # ----------------------------------------------------
        # HUD
        # ----------------------------------------------------

        self.hud = Label(
            text="",
            size_hint=(None, None),
            size=(dp(330), dp(48)),
            pos_hint={
                "x": 0.025,
                "top": 0.97
            },
            color=(1, 1, 1, 1),
            bold=True,
            font_size="17sp"
        )

        self.add_widget(self.hud)

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        self.title = Label(
            text="CHESTER",
            font_size="42sp",
            bold=True,
            color=(0.20, 0.10, 0.30, 1),
            size_hint=(1, None),
            height=dp(65),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.66
            }
        )

        self.add_widget(self.title)

        self.subtitle = Label(
            text="Una aventura de tela",
            font_size="18sp",
            color=(0.25, 0.20, 0.30, 1),
            size_hint=(1, None),
            height=dp(40),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.58
            }
        )

        self.add_widget(self.subtitle)

        # ----------------------------------------------------
        # BOTÓN JUGAR
        # ----------------------------------------------------

        self.start_button = Button(
            text="JUGAR",
            size_hint=(None, None),
            size=(dp(190), dp(65)),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.40
            },
            font_size="20sp",
            bold=True,
            background_normal="",
            background_color=(0.18, 0.68, 0.34, 1)
        )

        self.start_button.bind(
            on_release=self.start_game
        )

        self.add_widget(self.start_button)

        # ----------------------------------------------------
        # BOTONES MÓVILES
        # ----------------------------------------------------

        self.left_button = Button(
            text="◀",
            font_size="31sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(78), dp(78)),
            pos_hint={
                "x": 0.035,
                "y": 0.035
            },
            background_normal="",
            background_color=(0.10, 0.14, 0.22, 0.90)
        )

        self.right_button = Button(
            text="▶",
            font_size="31sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(78), dp(78)),
            pos_hint={
                "x": 0.225,
                "y": 0.035
            },
            background_normal="",
            background_color=(0.10, 0.14, 0.22, 0.90)
        )

        self.jump_button = Button(
            text="SALTAR",
            font_size="15sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(105), dp(105)),
            pos_hint={
                "right": 0.965,
                "y": 0.03
            },
            background_normal="",
            background_color=(0.12, 0.67, 0.36, 0.95)
        )

        self.left_button.bind(
            on_press=lambda *_:
            self.move_pressed("left", True)
        )

        self.left_button.bind(
            on_release=lambda *_:
            self.move_pressed("left", False)
        )

        self.right_button.bind(
            on_press=lambda *_:
            self.move_pressed("right", True)
        )

        self.right_button.bind(
            on_release=lambda *_:
            self.move_pressed("right", False)
        )

        self.jump_button.bind(
            on_press=self.jump
        )

        self.add_widget(self.left_button)
        self.add_widget(self.right_button)
        self.add_widget(self.jump_button)

        # ----------------------------------------------------
        # INICIO
        # ----------------------------------------------------

        self.reset()
        self.set_controls(False)

        Clock.schedule_interval(
            self.update,
            1.0 / 60.0
        )

        self.bind(
            size=lambda *_: self.draw()
        )

    # ========================================================
    # CONTROLES
    # ========================================================

    def set_controls(self, visible):

        for button in (
            self.left_button,
            self.right_button,
            self.jump_button
        ):
            button.disabled = not visible
            button.opacity = 1 if visible else 0

    def move_pressed(self, direction, value):

        if direction in self.controls:
            self.controls[direction] = value

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.lives = 3
        self.coins = 0

        self.player_x = 100.0

        # El suelo está en 540.
        # Chester mide 58.
        self.player_y = 482.0

        self.vx = 0.0
        self.vy = 0.0

        self.on_ground = True

        self.camera_x = 0.0

        self.controls["left"] = False
        self.controls["right"] = False

        # ----------------------------------------------------
        # ENEMIGOS
        # ----------------------------------------------------

        self.enemies = [
            [600.0, 505.0, -1],
            [1120.0, 405.0, -1],
            [1900.0, 405.0, -1],
            [2700.0, 415.0, -1],
            [3550.0, 415.0, -1]
        ]

        # ----------------------------------------------------
        # MONEDAS
        # ----------------------------------------------------

        self.coin_list = [
            [350.0, 410.0],
            [570.0, 350.0],
            [800.0, 290.0],
            [1100.0, 400.0],
            [1350.0, 330.0],
            [1600.0, 260.0],
            [1900.0, 400.0],
            [2150.0, 340.0],
            [2400.0, 280.0],
            [2700.0, 410.0],
            [3000.0, 350.0],
            [3250.0, 290.0],
            [3550.0, 410.0],
            [3850.0, 340.0],
            [4040.0, 260.0]
        ]

    # ========================================================
    # COMENZAR
    # ========================================================

    def start_game(self, *_):

        self.reset()

        self.state = "playing"

        self.title.opacity = 0
        self.subtitle.opacity = 0

        self.start_button.opacity = 0
        self.start_button.disabled = True

        self.set_controls(True)

        self.draw()

    # ========================================================
    # SALTO
    # ========================================================

    def jump(self, *_):

        if self.state != "playing":
            return

        if self.on_ground:

            self.vy = JUMP_FORCE
            self.on_ground = False

    # ========================================================
    # COLISIÓN
    # ========================================================

    def collision(self, x, y, w, h, obj):

        ox, oy, ow, oh = obj

        return (
            x < ox + ow
            and
            x + w > ox
            and
            y < oy + oh
            and
            y + h > oy
        )

    # ========================================================
    # ACTUALIZACIÓN
    # ========================================================

    def update(self, dt):

        if dt > 0.1:
            dt = 0.1

        if self.state == "playing":

            # ------------------------------------------------
            # MOVIMIENTO
            # ------------------------------------------------

            self.vx = 0

            if self.controls["right"]:
                self.vx += MOVE_SPEED

            if self.controls["left"]:
                self.vx -= MOVE_SPEED

            new_x = self.player_x + self.vx

            new_x = max(
                0,
                min(
                    new_x,
                    WORLD_WIDTH - PLAYER_W
                )
            )

            # ------------------------------------------------
            # COLISIÓN HORIZONTAL
            # ------------------------------------------------

            for platform in self.platforms:

                if self.collision(
                    new_x,
                    self.player_y,
                    PLAYER_W,
                    PLAYER_H,
                    platform
                ):

                    if self.vx > 0:
                        new_x = platform[0] - PLAYER_W

                    elif self.vx < 0:
                        new_x = platform[0] + platform[2]

            self.player_x = new_x

            # ------------------------------------------------
            # GRAVEDAD
            # ------------------------------------------------

            self.vy += GRAVITY

            if self.vy > 15:
                self.vy = 15

            old_y = self.player_y
            new_y = self.player_y + self.vy

            self.on_ground = False

            # ------------------------------------------------
            # COLISIÓN VERTICAL
            # ------------------------------------------------

            for platform in self.platforms:

                if self.collision(
                    self.player_x,
                    new_y,
                    PLAYER_W,
                    PLAYER_H,
                    platform
                ):

                    # cayendo
                    if self.vy > 0:

                        if (
                            old_y + PLAYER_H
                            <= platform[1] + 15
                        ):

                            new_y = (
                                platform[1]
                                - PLAYER_H
                            )

                            self.vy = 0
                            self.on_ground = True

                    # subiendo
                    elif self.vy < 0:

                        if (
                            old_y
                            >= platform[1]
                            + platform[3]
                            - 10
                        ):

                            new_y = (
                                platform[1]
                                + platform[3]
                            )

                            self.vy = 0

            self.player_y = new_y

            # ------------------------------------------------
            # ENEMIGOS
            # ------------------------------------------------

            for enemy in self.enemies:

                enemy[0] += enemy[2] * 2

                if enemy[0] <= 0:

                    enemy[0] = 0
                    enemy[2] = 1

                elif enemy[0] >= WORLD_WIDTH - ENEMY_W:

                    enemy[0] = WORLD_WIDTH - ENEMY_W
                    enemy[2] = -1

            # ------------------------------------------------
            # MONEDAS
            # ------------------------------------------------

            for coin in self.coin_list[:]:

                if self.collision(
                    self.player_x,
                    self.player_y,
                    PLAYER_W,
                    PLAYER_H,
                    (
                        coin[0],
                        coin[1],
                        22,
                        30
                    )
                ):

                    self.coin_list.remove(coin)
                    self.coins += 1

            # ------------------------------------------------
            # ENEMIGOS
            # ------------------------------------------------

            defeated = None

            for enemy in self.enemies:

                if self.collision(
                    self.player_x,
                    self.player_y,
                    PLAYER_W,
                    PLAYER_H,
                    (
                        enemy[0],
                        enemy[1],
                        ENEMY_W,
                        ENEMY_H
                    )
                ):

                    # Saltar encima
                    if (
                        self.vy > 0
                        and
                        self.player_y + PLAYER_H
                        <= enemy[1] + 20
                    ):

                        defeated = enemy

                        self.vy = JUMP_FORCE * 0.7
                        self.on_ground = False

                    else:

                        self.lose_life()

                    break

            if defeated is not None:

                if defeated in self.enemies:
                    self.enemies.remove(defeated)

            # ------------------------------------------------
            # CAÍDA
            # ------------------------------------------------

            if self.player_y > 700:
                self.lose_life()

            # ------------------------------------------------
            # META
            # ------------------------------------------------

            if self.collision(
                self.player_x,
                self.player_y,
                PLAYER_W,
                PLAYER_H,
                (
                    4120,
                    210,
                    50,
                    120
                )
            ):

                self.finish("win")

            # ------------------------------------------------
            # CÁMARA
            # ------------------------------------------------

            self.update_camera()

        self.draw()

        return True

    # ========================================================
    # PERDER VIDA
    # ========================================================

    def lose_life(self):

        if self.state != "playing":
            return

        self.lives -= 1

        if self.lives <= 0:

            self.lives = 0

            self.finish("game_over")

            return

        self.player_x = 100
        self.player_y = 482

        self.vx = 0
        self.vy = 0

        self.on_ground = True

        self.camera_x = 0

        self.controls["left"] = False
        self.controls["right"] = False

    # ========================================================
    # CÁMARA
    # ========================================================

    def update_camera(self):

        if self.width <= 0:
            return

        # Aproximadamente 1000 unidades del mundo visibles.
        visible_width = 1000.0

        max_camera = max(
            0,
            WORLD_WIDTH - visible_width
        )

        target = self.player_x - 500

        self.camera_x = max(
            0,
            min(
                target,
                max_camera
            )
        )

    # ========================================================
    # FIN DEL JUEGO
    # ========================================================

    def finish(self, result):

        self.state = result

        self.controls["left"] = False
        self.controls["right"] = False

        self.set_controls(False)

        self.start_button.disabled = False
        self.start_button.opacity = 1
        self.start_button.text = "JUGAR OTRA VEZ"

        self.title.opacity = 1
        self.subtitle.opacity = 1

        if result == "win":

            self.title.text = "¡GANASTE!"

            self.subtitle.text = (
                "Monedas: %d\n\n"
                "¡Excelente trabajo!"
                % self.coins
            )

        else:

            self.title.text = "GAME OVER"

            self.subtitle.text = (
                "Se terminaron tus vidas.\n\n"
                "¡Intentá de nuevo!"
            )

        self.draw()

    # ========================================================
    # CONVERSIÓN DE COORDENADAS
    # ========================================================

    def sy(self, y, height):

        """
        Convierte las coordenadas del mundo,
        donde 0 está arriba, a las coordenadas
        de pantalla de Kivy, donde 0 está abajo.
        """

        return (
            WORLD_HEIGHT
            - y
            - height
        ) * (self.height / WORLD_HEIGHT)

    def sx(self, x):

        return (
            x - self.camera_x
        ) * (self.width / 1000.0)

    # ========================================================
    # DIBUJAR
    # ========================================================

    def draw(self):

        w = self.width
        h = self.height

        if w <= 0 or h <= 0:
            return

        canvas = self.game_canvas.canvas

        canvas.clear()

        with canvas:

            # =================================================
            # CIELO
            # =================================================

            Color(
                0.38,
                0.72,
                0.95,
                1
            )

            Rectangle(
                pos=(0, 0),
                size=(w, h)
            )

            # =================================================
            # NUBES
            # =================================================

            Color(
                1,
                1,
                1,
                0.70
            )

            Ellipse(
                pos=(w * 0.08, h * 0.77),
                size=(w * 0.13, h * 0.07)
            )

            Ellipse(
                pos=(w * 0.14, h * 0.79),
                size=(w * 0.10, h * 0.06)
            )

            Ellipse(
                pos=(w * 0.70, h * 0.68),
                size=(w * 0.15, h * 0.07)
            )

            Ellipse(
                pos=(w * 0.77, h * 0.70),
                size=(w * 0.11, h * 0.06)
            )

            # =================================================
            # SOL
            # =================================================

            Color(
                1,
                0.88,
                0.28,
                1
            )

            Ellipse(
                pos=(
                    w * 0.79,
                    h * 0.78
                ),
                size=(
                    w * 0.12,
                    h * 0.15
                )
            )

            # =================================================
            # MONTAÑAS LEJANAS
            # =================================================

            Color(
                0.38,
                0.63,
                0.73,
                1
            )

            Line(
                points=[
                    -100, h * 0.25,
                    w * 0.12, h * 0.52,
                    w * 0.28, h * 0.27,
                    w * 0.45, h * 0.50,
                    w * 0.62, h * 0.26,
                    w * 0.80, h * 0.49,
                    w * 1.05, h * 0.28
                ],
                width=3
            )

            # =================================================
            # SI ESTAMOS EN MENÚ
            # =================================================

            if self.state in (
                "menu",
                "game_over",
                "win"
            ):
                self.update_hud()
                return

            # =================================================
            # SUELO / PLATAFORMAS
            # =================================================

            for x, y, pw, ph in self.platforms:

                screen_x = self.sx(x)
                screen_y = self.sy(y, ph)

                # tierra
                Color(
                    0.42,
                    0.25,
                    0.14,
                    1
                )

                RoundedRectangle(
                    pos=(
                        screen_x,
                        screen_y
                    ),
                    size=(
                        pw * w / 1000.0,
                        ph * h / WORLD_HEIGHT
                    ),
                    radius=[dp(5)]
                )

                # césped
                Color(
                    0.20,
                    0.68,
                    0.30,
                    1
                )

                Rectangle(
                    pos=(
                        screen_x,
                        screen_y
                        + ph * h / WORLD_HEIGHT
                        - 10 * h / WORLD_HEIGHT
                    ),
                    size=(
                        pw * w / 1000.0,
                        10 * h / WORLD_HEIGHT
                    )
                )

                # brillo
                Color(
                    0.35,
                    0.82,
                    0.38,
                    1
                )

                Rectangle(
                    pos=(
                        screen_x,
                        screen_y
                        + ph * h / WORLD_HEIGHT
                        - 4 * h / WORLD_HEIGHT
                    ),
                    size=(
                        pw * w / 1000.0,
                        4 * h / WORLD_HEIGHT
                    )
                )

            # =================================================
            # BLOQUES
            # =================================================

            for x, y, bw, bh in self.blocks:

                screen_x = self.sx(x)
                screen_y = self.sy(y, bh)

                Color(
                    0.67,
                    0.39,
                    0.20,
                    1
                )

                Rectangle(
                    pos=(
                        screen_x,
                        screen_y
                    ),
                    size=(
                        bw * w / 1000.0,
                        bh * h / WORLD_HEIGHT
                    )
                )

                Color(
                    0.80,
                    0.53,
                    0.27,
                    1
                )

                Line(
                    rectangle=(
                        screen_x,
                        screen_y,
                        bw * w / 1000.0,
                        bh * h / WORLD_HEIGHT
                    ),
                    width=1.5
                )

            # =================================================
            # MONEDAS
            # =================================================

            for x, y in self.coin_list:

                cx = self.sx(x)
                cy = self.sy(y, 30)

                # sombra
                Color(
                    0.30,
                    0.22,
                    0.05,
                    0.25
                )

                Ellipse(
                    pos=(
                        cx + 3,
                        cy - 3
                    ),
                    size=(
                        22 * w / 1000.0,
                        30 * h / WORLD_HEIGHT
                    )
                )

                # moneda
                Color(
                    1.0,
                    0.78,
                    0.05,
                    1
                )

                Ellipse(
                    pos=(
                        cx,
                        cy
                    ),
                    size=(
                        22 * w / 1000.0,
                        30 * h / WORLD_HEIGHT
                    )
                )

                # centro
                Color(
                    1,
                    0.93,
                    0.32,
                    1
                )

                Ellipse(
                    pos=(
                        cx + 4,
                        cy + 3
                    ),
                    size=(
                        14 * w / 1000.0,
                        24 * h / WORLD_HEIGHT
                    )
                )

                # brillo
                Color(
                    1,
                    1,
                    0.82,
                    1
                )

                Ellipse(
                    pos=(
                        cx + 6,
                        cy + 17 * h / WORLD_HEIGHT
                    ),
                    size=(
                        4 * w / 1000.0,
                        7 * h / WORLD_HEIGHT
                    )
                )

            # =================================================
            # ENEMIGOS
            # =================================================

            for x, y, direction in self.enemies:

                ex = self.sx(x)
                ey = self.sy(y, ENEMY_H)

                # sombra
                Color(
                    0.10,
                    0.10,
                    0.15,
                    0.20
                )

                Ellipse(
                    pos=(
                        ex + 3,
                        ey - 3
                    ),
                    size=(
                        40 * w / 1000.0,
                        35 * h / WORLD_HEIGHT
                    )
                )

                # cuerpo
                Color(
                    0.85,
                    0.25,
                    0.20,
                    1
                )

                Ellipse(
                    pos=(
                        ex,
                        ey
                    ),
                    size=(
                        40 * w / 1000.0,
                        35 * h / WORLD_HEIGHT
                    )
                )

                # parte superior
                Color(
                    0.98,
                    0.38,
                    0.25,
                    1
                )

                Ellipse(
                    pos=(
                        ex + 5,
                        ey + 8
                    ),
                    size=(
                        30 * w / 1000.0,
                        23 * h / WORLD_HEIGHT
                    )
                )

                # ojos
                Color(
                    1,
                    1,
                    1,
                    1
                )

                Ellipse(
                    pos=(
                        ex + 7,
                        ey + 13
                    ),
                    size=(
                        10 * w / 1000.0,
                        11 * h / WORLD_HEIGHT
                    )
                )

                Ellipse(
                    pos=(
                        ex + 23,
                        ey + 13
                    ),
                    size=(
                        10 * w / 1000.0,
                        11 * h / WORLD_HEIGHT
                    )
                )

                # pupilas
                Color(
                    0.08,
                    0.08,
                    0.10,
                    1
                )

                Ellipse(
                    pos=(
                        ex + 10,
                        ey + 16
                    ),
                    size=(
                        5 * w / 1000.0,
                        6 * h / WORLD_HEIGHT
                    )
                )

                Ellipse(
                    pos=(
                        ex + 26,
                        ey + 16
                    ),
                    size=(
                        5 * w / 1000.0,
                        6 * h / WORLD_HEIGHT
                    )
                )

                # boca
                Line(
                    points=[
                        ex + 14,
                        ey + 8,
                        ex + 20,
                        ey + 5,
                        ex + 26,
                        ey + 8
                    ],
                    width=1.5
                )

            # =================================================
            # META
            # =================================================

            flag_x = self.sx(4140)

            flag_bottom = self.sy(
                330,
                120
            )

            Color(
                0.28,
                0.22,
                0.18,
                1
            )

            Rectangle(
                pos=(
                    flag_x,
                    flag_bottom
                ),
                size=(
                    7 * w / 1000.0,
                    120 * h / WORLD_HEIGHT
                )
            )

            Color(
                0.90,
                0.12,
                0.18,
                1
            )

            Triangle(
                points=[
                    flag_x + 7,
                    flag_bottom + 115 * h / WORLD_HEIGHT,

                    flag_x + 55 * w / 1000.0,
                    flag_bottom + 95 * h / WORLD_HEIGHT,

                    flag_x + 7,
                    flag_bottom + 75 * h / WORLD_HEIGHT
                ]
            )

            # =================================================
            # CHESTER
            # =================================================

            px = self.sx(self.player_x)

            # La posición player_y es el borde superior
            # lógico del personaje en nuestro sistema.
            py = self.sy(
                self.player_y,
                PLAYER_H
            )

            scale_x = w / 1000.0
            scale_y = h / WORLD_HEIGHT

            # ------------------------------------------------
            # SOMBRA
            # ------------------------------------------------

            Color(
                0.05,
                0.05,
                0.10,
                0.20
            )

            Ellipse(
                pos=(
                    px + 5,
                    py - 3
                ),
                size=(
                    34 * scale_x,
                    8 * scale_y
                )
            )

            # ------------------------------------------------
            # PIERNAS
            # ------------------------------------------------

            Color(
                0.55,
                0.30,
                0.70,
                1
            )

            Ellipse(
                pos=(
                    px + 4 * scale_x,
                    py + 2 * scale_y
                ),
                size=(
                    15 * scale_x,
                    25 * scale_y
                )
            )

            Ellipse(
                pos=(
                    px + 23 * scale_x,
                    py + 2 * scale_y
                ),
                size=(
                    15 * scale_x,
                    25 * scale_y
                )
            )

            # ------------------------------------------------
            # ZAPATOS
            # ------------------------------------------------

            Color(
                0.16,
                0.14,
                0.22,
                1
            )

            Ellipse(
                pos=(
                    px - 1 * scale_x,
                    py
                ),
                size=(
                    24 * scale_x,
                    12 * scale_y
                )
            )

            Ellipse(
                pos=(
                    px + 21 * scale_x,
                    py
                ),
                size=(
                    24 * scale_x,
                    12 * scale_y
                )
            )

            # ------------------------------------------------
            # CUERPO
            # ------------------------------------------------

            Color(
                0.53,
                0.30,
                0.70,
                1
            )

            Ellipse(
                pos=(
                    px + 5 * scale_x,
                    py + 20 * scale_y
                ),
                size=(
                    32 * scale_x,
                    34 * scale_y
                )
            )

            # ------------------------------------------------
            # PANZA
            # ------------------------------------------------

            Color(
                0.67,
                0.42,
                0.78,
                1
            )

            Ellipse(
                pos=(
                    px + 11 * scale_x,
                    py + 25 * scale_y
                ),
                size=(
                    20 * scale_x,
                    22 * scale_y
                )
            )

            # ------------------------------------------------
            # BRAZOS
            # ------------------------------------------------

            Color(
                0.94,
                0.52,
                0.60,
                1
            )

            Ellipse(
                pos=(
                    px - 8 * scale_x,
                    py + 22 * scale_y
                ),
                size=(
                    17 * scale_x,
                    29 * scale_y
                )
            )

            Ellipse(
                pos=(
                    px + 33 * scale_x,
                    py + 22 * scale_y
                ),
                size=(
                    17 * scale_x,
                    29 * scale_y
                )
            )

            # ------------------------------------------------
            # CABEZA
            # ------------------------------------------------

            Color(
                0.95,
                0.55,
                0.63,
                1
            )

            Ellipse(
                pos=(
                    px + 3 * scale_x,
                    py + 34 * scale_y
                ),
                size=(
                    36 * scale_x,
                    35 * scale_y
                )
            )

            # ------------------------------------------------
            # OREJAS
            # ------------------------------------------------

            Color(
                0.90,
                0.42,
                0.52,
                1
            )

            Ellipse(
                pos=(
                    px - 5 * scale_x,
                    py + 45 * scale_y
                ),
                size=(
                    17 * scale_x,
                    18 * scale_y
                )
            )

            Ellipse(
                pos=(
                    px + 30 * scale_x,
                    py + 45 * scale_y
                ),
                size=(
                    17 * scale_x,
                    18 * scale_y
                )
            )

            # ------------------------------------------------
            # OJOS
            # ------------------------------------------------

            Color(
                1,
                1,
                1,
                1
            )

            Ellipse(
                pos=(
                    px + 9 * scale_x,
                    py + 47 * scale_y
                ),
                size=(
                    11 * scale_x,
                    13 * scale_y
                )
            )

            Ellipse(
                pos=(
                    px + 23 * scale_x,
                    py + 47 * scale_y
                ),
                size=(
                    11 * scale_x,
                    13 * scale_y
                )
            )

            # pupilas
            Color(
                0.08,
                0.08,
                0.10,
                1
            )

            Ellipse(
                pos=(
                    px + 12 * scale_x,
                    py + 50 * scale_y
                ),
                size=(
                    5 * scale_x,
                    6 * scale_y
                )
            )

            Ellipse(
                pos=(
                    px + 26 * scale_x,
                    py + 50 * scale_y
                ),
                size=(
                    5 * scale_x,
                    6 * scale_y
                )
            )

            # ------------------------------------------------
            # NARIZ
            # ------------------------------------------------

            Color(
                0.70,
                0.22,
                0.36,
                1
            )

            Ellipse(
                pos=(
                    px + 18 * scale_x,
                    py + 41 * scale_y
                ),
                size=(
                    7 * scale_x,
                    6 * scale_y
                )
            )

            # ------------------------------------------------
            # SONRISA
            # ------------------------------------------------

            Color(
                0.35,
                0.10,
                0.18,
                1
            )

            Line(
                points=[
                    px + 16 * scale_x,
                    py + 39 * scale_y,

                    px + 21 * scale_x,
                    py + 37 * scale_y,

                    px + 27 * scale_x,
                    py + 39 * scale_y
                ],
                width=1.3
            )

        self.update_hud()

    # ========================================================
    # HUD
    # ========================================================

    def update_hud(self):

        self.hud.text = (
            "❤️ %d        🪙 %d"
            % (
                self.lives,
                self.coins
            )
        )


# ============================================================
# APP
# ============================================================

class ChesterApp(App):

    def build(self):

        Window.clearcolor = (
            0.38,
            0.72,
            0.95,
            1
        )

        return ChesterGame()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    ChesterApp().run()
