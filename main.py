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
from kivymd.app import App
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton,MDIconButton
# to change the kivy default settings we use this module config
from kivy.config import Config
import pandas as pd
from GoogleDrivePyDrive import *
from kivymd.uix.list import MDList,TwoLineListItem
import numpy as np
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen,ScreenManager

imagen="""
Image:
    source:"titulo.png"
    pos_hint:{"center_x":0.5,"center_y":0.8}
    size_hint:0.5,0.5
    width:200
"""

screen_helper="""
ScreenManager:
    PrincipalScreen:
    ListaScreen:
<PrincipalScreen>:
    name='principal'
    MDRenctangleFlatButton:
        text:'Desplegar Lista'
        pos_hint:{'center_x':0.5,'center_y':0.1}
        on_press:root.manager.current='list'
<ListaScreen>:
    name='lista'
    MDLabel:
        text:'Lista de productos'
"""

class PrincipalScreen(Screen):
    pass

class ListaScreen(Screen):
    pass

sm=ScreenManager()
sm.add_widget(PrincipalScreen(name='principal'))
sm.add_widget(ListaScreen(name='lista'))

class GastosApp(MDApp):

    def build(self):
        self.theme_cls.theme_style='Dark'
        screen=Screen()
        scroll=ScrollView()
        self.cols = 1
        adaptive_height= True
        ##################################################################
        images=Builder.load_string(imagen)
        screen.add_widget(images)
        ####################################################################
        self.nombre=MDTextField(hint_text='Nombre del gasto',
                                pos_hint={'x': 0.3,'y': 0.5},
                                size_hint_x=None,
                                 width=300)
        screen.add_widget(self.nombre)

        self.gasto = MDTextField(hint_text='Ingresa cuanto gastaste',
                                pos_hint={'x': 0.6,'y': 0.5},
                                size_hint_x=None,
                                width=200)
        screen.add_widget(self.gasto)

        #######################################################################
        button1=MDIconButton(icon='icono_add.PNG',
                            icon_size='40sp',
                           pos_hint={'x': 0.35,'y': 0.4})
        button1.bind(on_press=self.tolist)
        screen.add_widget(button1)

        button2 = MDIconButton(icon='calcula.png',
                                icon_size='40sp',
                               pos_hint={'x': 0.65,'y': 0.4})
        button2.bind(on_press = self.getQueda)
        screen.add_widget(button2)
        #return self.window

        buttonNew=MDIconButton(icon='plus.png',
                                    icon_size='40sp',
                                    pos_hint={'x':0.35,'y':0.3})
        buttonNew.bind(on_press=self.getNuevo)
        screen.add_widget(buttonNew)
        '''
        buttonVerLista=MDIconButton(icon='lista.png',
                                    icon_size='40sp',
                                    pos_hint={'x':0.65,'y':0.3})
        buttonVerLista.bind(on_press=self.verLista)
        screen.add_widget(buttonVerLista)
'''
        list_view=MDList()
        scroll.add_widget(list_view)
        #datos=bajar_archivo_por_id('1HgI8Sx0CSB1kFceVeaAZrRm09MsvDB3r1Nb0ws-CR2M','C:\\Users\52333\Documents\primera_app')
        df=pd.read_csv('gastos.csv')
        articulos=list(df['articulo'])
        costo=list(df['costo'])
        for i in range(len(articulos)):
            items=TwoLineListItem(text=articulos[i],secondary_text=str(costo[i]))
            list_view.add_widget(items)
        screen.add_widget(scroll)

        return screen

    def tolist(self,event):
        articulo=str(self.nombre.text)
        costo=str(self.gasto.text)
        df_list=pd.DataFrame([{'articulo':articulo,'costo':costo}],
                                columns=['articulo','costo'])
        df_list.to_csv('gastos.csv',index=False,mode='a',header=False)
        actualizar_archivo('gastos.csv','1HgI8Sx0CSB1kFceVeaAZrRm09MsvDB3r1Nb0ws-CR2M')
        self.nombre.text ="Se añadio el gasto a la lista"


    def getQueda(self,event):
        #ruta,id_folder
        df = pd.read_csv('totales.csv')
        total = df[['total']].values
        gasto2 = self.gasto.text
        total2 = total - float(gasto2)

        del df['total']
        df.insert(0,'total',total2)
        df.to_csv('totales.csv',index=False)
        actualizar_archivo('totales.csv','1HKfDprOjpJWTp4aRTuJ6ddlypc2Vg-5V')
        total2=float(total2)
        #df=df[['total']].drop([0], axis=0, inplace=True)
        #df=df[df.total != 7]
        self.gasto.text = "Tienes " + str(total2) + " pesos"

    def getNuevo(self,event):
        self.nombre.text= " "
        self.gasto.text=" "







'''
class PresupuestoApp(MDApp):
    def build(self):
        ml=GastosApp()
        return ml


'''
if __name__ == "__main__":
    GastosApp().run()
