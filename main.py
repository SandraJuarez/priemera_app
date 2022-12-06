from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
# to change the kivy default settings we use this module config
from kivy.config import Config
import pandas as pd

Config.set('graphics', 'resizable', True)

texto="""
MDTextField:
    hint_text:"Ingresa cuánto gastaste"
    pos_hint:{'center_x': 0.5,
    'center_y': 0.5},size_hint_x=None, width=200)
    size_hint_x=None
    width:300
"""


class myLayout(GridLayout):
    def __init__(self,**kwargs):
        super(myLayout,self).__init__(**kwargs)
        #self.window = GridLayout()
        self.cols = 1

        ##################################################################
        #todo esto para añadir una imagen

        self.label=MDLabel(text="Control de Gastos", halign="center",
                        font_style="Subtitle2")
        self.add_widget(self.label)
        self.add_widget(Image(source="ivan.jpg"))
        # By default, the image is centered and fits
        # inside the widget bounding box.
        # If you don’t want that,
        # you can set allow_stretch to
        # True and keep_ratio to False.
        self.allow_stretch = True
        self.keep_ratio = False
        # Providing Size to the image
        # it varies from 0 to 1
        self.size_hint_x = 0.25
        self.size_hint_y = 0.25
        # Position set
        self.pos = (200, 100)
        ####################################################################

        self.gasto = MDTextField(hint_text='Ingresa cuanto gastaste',
                                pos_hint={'center_x': 0.5,
                                'center_y': 0.5},size_hint_x=None, width=200)
        #gasto = Builder.load_string(texto)
        self.add_widget(self.gasto)

        self.nombre=MDTextField(hint_text='Nombre del gasto',
                                pos_hint={'center_x': 0.5,
                                'center_y': 0.5},size_hint_x=None, width=200)
        self.add_widget(self.nombre)
        #self.gastoRequest = Label(text = "Ingresa cuánto gastaste")
        #self.add_widget(self.gastoRequest)
        #self.float = TextInput(multiline=False)
        #self.add_widget(self.float)

        #self.nombreRequest =Label(text="Ingresa el nombre del gasto")
        #self.add_widget(self.nombreRequest)
        #self.float =TextInput(multline=False)
        #self.add_widget(self.float)

        #######################################################################
        self.button = Button(text = "Calcula cuánto dinero te queda")
        self.button.bind(on_press = self.getQueda)
        self.add_widget(self.button)
        #return self.window


    def getQueda(self,event):
        df = pd.read_csv('totales.csv')
        total = df[['total']].values
        gasto2 = self.gasto.text
        total2 = total - float(gasto2)

        del df['total']
        df.insert(0,'total',total2)
        df.to_csv('totales.csv',index=False)
        total2=float(total2)
        #df=df[['total']].drop([0], axis=0, inplace=True)
        #df=df[df.total != 7]
        self.gasto.text = "Tienes " + str(total2) + " pesos"


class PresupuestoApp(MDApp):
    def build(self):
        ml=myLayout()
        return ml



if __name__ == "__main__":
    PresupuestoApp().run()
