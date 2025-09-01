from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.actionbar import ActionBar, ActionButton, ActionView, ActionPrevious
from kivy.core.window import Window
from kivy.graphics import Rectangle,Color,RoundedRectangle
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.animation import Animation
import json
from kivy.core.audio import SoundLoader
from kivy.metrics import sp

class CustomButton(Button):
    
    cor = ListProperty([0.1,0.5,0.7,1])
    cor2 = ListProperty([0.7,0.1,0.3,1])
    
    def on_press(self,*args):
        self.cor,self.cor2=self.cor2,self.cor
        
    def on_release(self,*args):
        self.cor,self.cor2=self.cor2,self.cor
    
    def on_cor(self,*args):
        self.atualizar()
    
    def __init__(self,**kwargs):
        super(CustomButton,self).__init__(**kwargs) 
        self.atualizar()
        
    def atualizar(self,*args):     
        self.background_color=(0,0,0,0)
        self.bind(pos=self.update_canvas,size=self.update_canvas)
        with self.canvas.before:
            Color(*self.cor)
            self.rect= RoundedRectangle(pos=self.pos,size=self.size,radius=[20])
            
    def update_canvas(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size
                        
                        
                        
class Tarefa(BoxLayout):
    def __init__(self,text=' ',parent_layout=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation='horizontal'
        self.size_hint_y=None
        self.height=90  
            
        self.label=Texto(text=text,size_hint_x=0.8)
        self.add_widget(self.label)    
         
        button=CustomButton(text='x',size_hint_x=0.2,width=50)   
        button.bind(on_release=self.rmv)
        self.add_widget(button)
        
        self.parent_layout=parent_layout
        
    def saveData(self,*args):
         with open('data.json','w') as data:
             json.dump(listtarefas,data)
        
    def rmv(self,instance):
        global poppapSound
        poppapSound.play()
        if self.parent_layout:
            texto=self.label.text
            self.parent_layout.remove_widget(self)
            listtarefas.remove(texto)
            self.saveData()

class Texto(Label):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.size_hint=(1,None)
        self.font_size=sp(17)
        
    def on_size(self,*args):
        self.text_size=(self.width - sp(10),None)
        
    def on_texture_size(self,*args):
        self.size=self.texture_size
        self.height+=sp(15)

            
        #tarefas
        
     
   
    
    
class Menu(Screen):
    
    def on_request_close(self,window,key,*args):
        if key == 27:
            self.confirmacao()
            return True
    
    def confirmacao(self,*args,**kwargs):
        global poppapSound
        poppapSound.play()
        
        box=BoxLayout(orientation='vertical',padding=1,spacing=1)
        butoes=BoxLayout(padding=1,spacing=2)
        pop=Popup(title='deseja mesmo sair?',content=box,size_hint_x=None,size_hint_y=None,size=(400,400))
        sim=CustomButton(text='sim')
        sim.bind(on_release=self.sair)
        nao=CustomButton(text='não')
        nao.bind(on_release=pop.dismiss)
        
        warning=Image(source='warning.png')
        
        butoes.add_widget(sim)
        butoes.add_widget(nao)
        box.add_widget(warning)
        box.add_widget(butoes)
        
        animText=Animation (color=(0,0,0,1)) + Animation(color=(1,1,1,1))
        animText.repeat=True
        animText.start(sim)
        
        anim=Animation (size=(450,300),duration =0.2,t='out_back')
        anim.start(pop)
        
        pop.open()
        
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.on_request_close)
        
       # with self.canvas:
   #         color=(1,0,0,1)
            #self.rect=Rectangle(size=(300,300),pos=(150,300))
        
        self.button=CustomButton(text='Ver tarefas',background_color=(1,1,1,1))
        self.button.bind(on_release=self.ir_para_tarefas)
        
        imj=Image(source='halfmoon.png')
        
        self.button3=CustomButton(text='Sair',height=100)
        self.button3.bind(on_release=self.confirmacao)
        
        self.button2=CustomButton(text='(em desenvolvimento)')
        
        self.layout_menu =BoxLayout(padding=[50,140,50,160],orientation='vertical',spacing=50)
        
        
        self.layout_menu.add_widget(imj)
        self.layout_menu.add_widget(self.button)
        self.layout_menu.add_widget(self.button2)
        self.layout_menu.add_widget(self.button3)
        self.add_widget(self.layout_menu)
        
    def ir_para_tarefas(self,*args):
            self.manager.current='tarefas'
    
    def sair(self,*args):
        App.get_running_app().stop()
        

listtarefas=[ ]

class Tarefas(Screen):
      
    def on_request_close(self,window,key,*args):
        if key == 27:
            self.confirmacao()
            return True
    
    def confirmacao(self,*args,**kwargs):  
        global poppapSound
        poppapSound.play()    
        box=BoxLayout(orientation='vertical',padding=1,spacing=1)
        butoes=BoxLayout(padding=1,spacing=2)
        pop=Popup(title='deseja mesmo sair?',content=box,size_hint_x=None,size_hint_y=None,size=(400,400))
        sim=CustomButton(text='sim')
        sim.bind(on_release=self.sair)
        nao=CustomButton(text='não')
        nao.bind(on_release=pop.dismiss)
        
        warning=Image(source='warning.png')
        
        butoes.add_widget(sim)
        butoes.add_widget(nao)
        box.add_widget(warning)
        box.add_widget(butoes)
        
        animText=Animation (color=(0,0,0,1)) + Animation(color=(1,1,1,1))
        animText.repeat=True
        animText.start(sim)
        
        anim=Animation (size=(450,300),duration =0.2,t='out_back')
        anim.start(pop)
        
        pop.open()
        
    def loadData(self,*args):
       global listtarefas
       try:
           with open('data.json','r') as data:
               
               listtarefas=json.load(data)
       except FileNotFoundError:
           pass
       
    def voltar_para_menu(self,*args):
        self.manager.current='menu'
        
    def sair(self,*args):
        App.get_running_app().stop()
        
    def on_pre_enter(self,*args):
        Window.bind(on_keyboard=self.voltar)
        
        self.loadData()
        
        name='tarefas'
        
        self.l=BoxLayout(orientation='vertical')
        
        action_bar=ActionBar(size_hint_y=None,height='48dp')
        action_view=ActionView()
        action_bar.add_widget(action_view)
        action_previous=ActionPrevious (title='Tarefas')
        action_previous.bind(on_release =self.voltar_para_menu)
        action_button= ActionButton(text='sair')
        
        #jdjdjdjdj
        action_button.bind(on_release=self.confirmacao)
        
        action_view.add_widget(action_previous)
        action_view.add_widget(action_button)
        
        self.l.add_widget(action_bar)
        
        
                
        self.layout= BoxLayout(orientation='horizontal',size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        
        self.layout2= BoxLayout(padding=[50,20,50,200],orientation='vertical',size_hint_y=None,spacing=15)
        self.layout2.bind(minimum_height=self.layout2.setter('height'))
        
        scroll_view =ScrollView(size_hint=(1,1))
        scroll_view.add_widget(self.layout2)
        
        cadd=Button(text='+',size_hint_y=None,height=75,size_hint_x=0.2,width=50)
        cadd.bind(on_release=self.add_tarefa)
        
        
        self.text_input= TextInput(size_hint_y=None,height=75,size_hint_x=0.8,width=200)
        
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(cadd)
       
           
        for tarefa in listtarefas:
            tarefa_widget=Tarefa(text=tarefa,parent_layout=self.layout2)
            self.layout2.add_widget(tarefa_widget)                                        
       
        self.l.add_widget(scroll_view)   
        self.l.add_widget(self.layout)
        self.add_widget(self.l)
        
    
    def voltar(self,window,key,*args):
        if key == 27:
            self.manager.current='menu'
            return True
    
    def on_pre_leave(self,*args):
        Window.unbind(on_keyboard=self.voltar)
        
    def saveData(self,*args):
         with open('data.json','w') as data:
             json.dump(listtarefas,data)
         
    def add_tarefa(self,instance):
         global popSound
         popSound.play()
         nova_tarefa_text=self.text_input.text
         if nova_tarefa_text:
             nova_tarefa= Tarefa(text=nova_tarefa_text,parent_layout =self.layout2)
             self.layout2.add_widget(nova_tarefa)
             self.text_input.text=' '
         listtarefas.append(nova_tarefa_text)
         self.saveData()
             
                           
class aplicativo(App):
    def build(self):
        Gerenciador=ScreenManager()
        tarefas_screen=Tarefas(name='tarefas')
        menu_screen=Menu(name='menu')
        Gerenciador.add_widget(menu_screen)
        Gerenciador.add_widget(tarefas_screen)
        Gerenciador.current='menu'
        return Gerenciador

popSound=SoundLoader.load('pop.mp3')
poppapSound=SoundLoader.load('poppap3.mp3')
aplicativo().run()
