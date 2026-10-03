# Chester - version Android con Kivy
# Requiere Kivy 2.0.0 y Python 3.8
# Ejecutar: python main.py

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, Line, Triangle
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty
from kivy.metrics import dp


ANCHO_MUNDO = 4200
ALTO_MUNDO = 600
GRAVEDAD = 0.7
VELOCIDAD = 5
FUERZA_SALTO = -14


class ChesterGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teclas = {"izq": False, "der": False}
        self.estado = "menu"
        self.vidas = 3
        self.monedas = 0
        self.camara_x = 0
        self.px, self.py = 100.0, 300.0
        self.vx = self.vy = 0.0
        self.en_suelo = False
        self.enemigos = []
        self.monedas_lista = []
        self.plataformas = [
            (0, 540, 4200, 60),
            (300,450,130,25),(520,390,130,25),(750,330,130,25),
            (1050,440,150,25),(1300,370,150,25),(1550,300,150,25),
            (1850,440,140,25),(2100,380,140,25),(2350,320,140,25),
            (2650,450,180,25),(2950,390,150,25),(3200,330,150,25),
            (3500,450,170,25),(3800,380,150,25),(4000,300,130,25)
        ]
        self.bloques = [
            (450,500,50,40),(500,500,50,40),(900,500,50,40),
            (950,500,50,40),(1200,500,50,40),(1250,500,50,40),
            (2000,500,50,40),(2050,500,50,40),(2850,500,50,40),
            (2900,500,50,40),(3350,500,50,40),(3400,500,50,40)
        ]
        self.reset()
        self.canvas_widget = Widget()
        self.add_widget(self.canvas_widget)
        self.hud = Label(text="", size_hint=(None,None), size=(dp(260),dp(38)),
                         pos_hint={"x":0.02,"top":0.99}, color=(1,1,1,1),
                         bold=True, font_size="16sp")
        self.add_widget(self.hud)
        self.menu_label = Label(text="CHESTER\\nUna aventura de tela\\n\\nTocá JUGAR",
                                halign="center", valign="middle",
                                font_size="28sp", color=(0.1,0.1,0.2,1))
        self.add_widget(self.menu_label)
        self.start_button = Button(text="JUGAR", size_hint=(None,None),
                                   size=(dp(150),dp(55)), pos_hint={"center_x":.5,"center_y":.38})
        self.start_button.bind(on_release=self.start)
        self.add_widget(self.start_button)
        self.left_button = Button(text="◀", font_size="30sp", size_hint=(None,None),
                                  size=(dp(70),dp(70)), pos_hint={"x":.03,"y":.03},
                                  background_color=(.15,.2,.3,.9))
        self.right_button = Button(text="▶", font_size="30sp", size_hint=(None,None),
                                   size=(dp(70),dp(70)), pos_hint={"x":.23,"y":.03},
                                   background_color=(.15,.2,.3,.9))
        self.jump_button = Button(text="SALTAR", font_size="16sp", size_hint=(None,None),
                                  size=(dp(90),dp(90)), pos_hint={"right":.97,"y":.03},
                                  background_color=(.1,.65,.3,.95))
        self.left_button.bind(on_press=lambda *_: self.set_move("izq",True),
                              on_release=lambda *_: self.set_move("izq",False))
        self.right_button.bind(on_press=lambda *_: self.set_move("der",True),
                               on_release=lambda *_: self.set_move("der",False))
        self.jump_button.bind(on_press=self.jump)
        self.add_widget(self.left_button)
        self.add_widget(self.right_button)
        self.add_widget(self.jump_button)
        self.set_controls(False)
        Clock.schedule_interval(self.update, 1/60)

    def set_controls(self, visible):
        for w in (self.left_button,self.right_button,self.jump_button):
            w.disabled = not visible
            w.opacity = 1 if visible else 0

    def set_move(self, direction, value):
        self.teclas[direction] = value

    def reset(self):
        self.vidas, self.monedas = 3, 0
        self.camara_x = 0
        self.px, self.py = 100.0, 300.0
        self.vx = self.vy = 0.0
        self.en_suelo = False
        self.enemigos = [[600.,505.,-1],[1120.,405.,-1],[1900.,405.,-1],
                         [2700.,415.,-1],[3550.,415.,-1]]
        self.monedas_lista = [[350,410],[570,350],[800,290],[1100,400],
                              [1350,330],[1600,260],[1900,400],[2150,340],
                              [2400,280],[2700,410],[3000,350],[3250,290],
                              [3550,410],[3850,340],[4040,260]]

    def start(self, *_):
        self.reset()
        self.estado = "jugando"
        self.menu_label.opacity = 0
        self.start_button.opacity = 0
        self.set_controls(True)

    def jump(self, *_):
        if self.estado == "jugando" and self.en_suelo:
            self.vy = FUERZA_SALTO
            self.en_suelo = False

    def collide(self, x, y, w, h, p):
        return x < p[0]+p[2] and x+w > p[0] and y < p[1]+p[3] and y+h > p[1]

    def update(self, dt):
        if self.estado == "jugando":
            self.vx = (VELOCIDAD if self.teclas["der"] else 0) - (VELOCIDAD if self.teclas["izq"] else 0)
            self.px = max(0, self.px + self.vx)
            # Colisiones horizontales
            for p in self.plataformas:
                if self.collide(self.px,self.py,42,58,p):
                    if self.vx > 0: self.px = p[0]-42
                    elif self.vx < 0: self.px = p[0]+p[2]
            self.vy = min(15, self.vy + GRAVEDAD)
            old_y = self.py
            self.py += self.vy
            self.en_suelo = False
            for p in self.plataformas:
                if self.collide(self.px,self.py,42,58,p):
                    if self.vy > 0 and old_y+58 <= p[1]+15:
                        self.py = p[1]-58
                        self.vy = 0
                        self.en_suelo = True
                    elif self.vy < 0:
                        self.py = p[1]+p[3]
                        self.vy = 0
            for e in self.enemigos:
                e[0] += e[2]*2
                if e[0] < 0 or e[0] > ANCHO_MUNDO-40: e[2] *= -1
            for coin in self.monedas_lista[:]:
                if self.collide(self.px,self.py,42,58,(coin[0],coin[1],22,30)):
                    self.monedas_lista.remove(coin)
                    self.monedas += 1
            for e in self.enemigos[:]:
                if self.collide(self.px,self.py,42,58,(e[0],e[1],40,35)):
                    if self.vy > 0 and self.py+58 <= e[1]+20:
                        self.enemigos.remove(e)
                        self.vy = FUERZA_SALTO*.7
                    else:
                        self.vidas -= 1
                        self.px,self.py = 100.,300.
                        self.vx=self.vy=0
                        if self.vidas <= 0: self.end("game_over")
                    break
            if self.py > 700:
                self.vidas -= 1
                self.px,self.py=100.,300.
                self.vx=self.vy=0
                if self.vidas <= 0: self.end("game_over")
            if self.collide(self.px,self.py,42,58,(4120,210,50,90)):
                self.end("victoria")
            self.camara_x = max(0,min(ANCHO_MUNDO-self.width*600/max(1,self.height),
                                     self.px-self.width*500/max(1,self.height)))
        self.draw()
        return True

    def end(self, state):
        self.estado = state
        self.set_controls(False)
        self.menu_label.text = "¡GANASTE!\\nMonedas: %d\\n\\nTocá JUGAR para volver a jugar" % self.monedas if state=="victoria" else "GAME OVER\\n\\nTocá JUGAR para intentar otra vez"
        self.menu_label.opacity = 1
        self.start_button.text = "JUGAR OTRA VEZ"
        self.start_button.opacity = 1

    def draw(self):
        w,h=self.width,self.height
        if w<=0 or h<=0: return
        sx=w/1000.0; sy=h/600.0
        c=self.canvas_widget.canvas
        c.clear()
        with c:
            Color(0.47,0.78,1,1); Rectangle(pos=self.pos,size=self.size)
            # Sol y montañas
            Color(1,.92,.43,1); Ellipse(pos=(w*.80,h*.79),size=(w*.11,h*.18))
            Color(.39,.70,.82,1)
            Line(points=[(-100*sx,100*sy),(0,300*sy),(250*sx,100*sy),(500*sx,320*sy),(800*sx,100*sy),(1100*sx,300*sy),(1400*sx,100*sy)],width=2)
            if self.estado in ("menu","game_over","victoria"):
                return
            def rect_world(x,y,ww,hh,color):
                Color(*color)
                Rectangle(pos=((x-self.camara_x)*sx,y*sy),size=(ww*sx,hh*sy))
            for x,y,ww,hh in self.plataformas:
                rect_world(x,y,ww,hh,(.47,.29,.18,1))
                rect_world(x,y,ww,12,(.27,.72,.34,1))
            for x,y,ww,hh in self.bloques:
                rect_world(x,y,ww,hh,(.65,.39,.22,1))
            for x,y in self.monedas_lista:
                Color(1,.86,.18,1); Ellipse(pos=((x-self.camara_x)*sx,y*sy),size=(22*sx,30*sy))
                Color(1,.97,.5,1); Ellipse(pos=((x+5-self.camara_x)*sx,(y+5)*sy),size=(8*sx,20*sy))
            for x,y,d in self.enemigos:
                Color(.95,.42,.12,1); Ellipse(pos=((x-self.camara_x)*sx,y*sy),size=(40*sx,35*sy))
                Color(1,1,1,1)
                Ellipse(pos=((x+7-self.camara_x)*sx,(y+12)*sy),size=(10*sx,11*sy))
                Ellipse(pos=((x+23-self.camara_x)*sx,(y+12)*sy),size=(10*sx,11*sy))
                Color(.1,.1,.1,1)
                Ellipse(pos=((x+11-self.camara_x)*sx,(y+16)*sy),size=(4*sx,4*sy))
                Ellipse(pos=((x+27-self.camara_x)*sx,(y+16)*sy),size=(4*sx,4*sy))
            # Meta
            rect_world(4140,210,7,120,(.35,.3,.25,1))
            Color(.86,.15,.18,1)
            Triangle(points=[(4147*sx-self.camara_x*sx,330*sy),(4195*sx-self.camara_x*sx,310*sy),(4147*sx-self.camara_x*sx,290*sy)])
            # Chester: cuerpo, cabeza, brazos, piernas, zapatos y cara
            x=(self.px-self.camara_x)*sx; y=self.py*sy
            Color(.49,.29,.63,1); Ellipse(pos=(x+4*sx,y+42*sy),size=(16*sx,25*sy)); Ellipse(pos=(x+22*sx,y+42*sy),size=(16*sx,25*sy))
            Color(.25,.22,.31,1); Ellipse(pos=(x,y+56*sy),size=(23*sx,11*sy)); Ellipse(pos=(x+22*sx,y+56*sy),size=(23*sx,11*sy))
            Color( .94,.51,.59,1); Ellipse(pos=(x+5*sx,y+20*sy),size=(32*sx,32*sy)); Ellipse(pos=(x-8*sx,y+22*sy),size=(18*sx,30*sy)); Ellipse(pos=(x+32*sx,y+22*sy),size=(18*sx,30*sy))
            Ellipse(pos=(x+3*sx,y-12*sy),size=(36*sx,38*sy)); Ellipse(pos=(x-4*sx,y+0*sy),size=(16*sx,16*sy)); Ellipse(pos=(x+31*sx,y+0*sy),size=(16*sx,16*sy))
            Color(1,1,1,1); Ellipse(pos=(x+8*sx,y+0*sy),size=(12*sx,13*sy)); Ellipse(pos=(x+23*sx,y+0*sy),size=(12*sx,13*sy))
            Color(.1,.1,.1,1); Ellipse(pos=(x+13*sx,y+4*sy),size=(5*sx,6*sy)); Ellipse(pos=(x+26*sx,y+4*sy),size=(5*sx,6*sy))
            Color(.75,.25,.4,1); Ellipse(pos=(x+19*sx,y+8*sy),size=(6*sx,5*sy))
        self.hud.text = "VIDAS: %d     MONEDAS: %d" % (self.vidas,self.monedas)


class ChesterApp(App):
    def build(self):
        Window.clearcolor=(.47,.78,1,1)
        return ChesterGame()


if __name__ == "__main__":
    ChesterApp().run()
