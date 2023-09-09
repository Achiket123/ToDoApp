from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty,NumericProperty
from kivy.animation import Animation
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.pickers import MDTimePicker
import pickle
import time


sm=ScreenManager(transition=WipeTransition())


dat=open('data/recs.dat','r+')



KV='''


<MD3Card>:
    md_bg_color:'#2fc0ff'
    size_hint: 1, None
    height:'50dp'
    MDGridLayout:
        rows:1
        MDCheckbox:
            
            on_active: app.on_checkbox_active(root)
            size_hint: '0.2sp', '1sp'
        MDLabel:      
             
            name:root.name
            id: task     
            text:root.text
            color:'black'
            bold:True
            font_size:'10sp'
        MDIconButton:
            icon:'pencil'
            on_press:app.edit_button(root)

    




MDScreenManager:
    id: screen_manager
    MDScreen:
        name:'main'
        id:screenA
        MDBoxLayout:
            spacing:'10sp'
            id:bx-1
            orientation: "vertical"
            md_bg_color: "#1E1E15"
        
            MDTopAppBar:
                title: "ToDoApp"
                padding:['1sp','1sp','20sp','20sp']
                size_hint:1,0.09
                anchor_title: "left"
                right_action_items: [["sword-cross",app.close_app]]
                
            MDScrollView:
                
                MDGridLayout:
                    padding:['10sp','0sp','10sp','0sp']
                    spacing:'10sp'
                    id:bx
                    size_hint: 1, None
                    cols:1
        
            MDGridLayout:
                cols:2
                size_hint: 1,0.1
                MDTextField:
                    id:txt_1
                    hint_text:'Enter Task'
                    hint_text_color_focus:'black'
                    text_color_focus:'black'
                    mode:'fill'
                    size_hint: 1,0.1
                MDRectangleFlatButton:
                    text:'Add Task'
                    size_hint: None,0.1
                    on_press:app.add_task()

        MDFloatingActionButton:
            id:plus
            icon:'plus'
            pos_hint: {"top": 0.19, "right": 0.99} 
                           
    MDScreen:
        md_bg_color: "#1E1E15"
        name:'info'
        MDBoxLayout:
            orientation: 'vertical'
            spacing: '30sp'
            MDTopAppBar:
                title: "ToDoApp"
                padding:['1sp','1sp','20sp','20sp']
                size_hint:1,0.09
                anchor_title: "left"
                left_action_items: [["./res/home.png",app.back]]
            MDBoxLayout:
                orientation: 'vertical'
                spacing:'30sp'
                
                MDBoxLayout:
                    
                    orientation: 'horizontal'
                    size_hint: 1, 0.15
                    pos_hint: {'center_x': 0.5,'center_y': 0.9}
                    padding:['10sp','0sp','10sp','0sp']
                    spacing:'10sp'
                    MDTextField:
                        
                        id:text
                        hint_text: "What Is To Be Done?"
                        mode: 'fill'
                        size_hint: 1, 1
                        text:''
                        font_size:'10sp'
                        hint_text_font_size:'10sp'
                    MDRectangleFlatIconButton:
                        icon:'floppy'
                        text:'SAVE'
                        size_hint:None,1
                        on_press:app.save(root)
                
                    
               
                MDBoxLayout:
                    
                    orientation: 'horizontal'
                    size_hint: 1, 0.15
                    pos_hint: {'center_x': 0.5,'center_y': 0.9}
                    padding:['10sp','0sp','10sp','0sp']
                    spacing:'10sp'
                    MDTextField:
                        
                        id:time
                        hint_text: "TIME"
                        mode: 'fill'
                        size_hint: 1, 1
                        
                        font_size:'10sp'
                        readonly:True
                        validater:'time'
                        time_format:'hh/mm/ss'
                    MDRectangleFlatIconButton:
                        icon:'clock'
                        text:'TIME'
                        size_hint:None,1
                        on_press:app.clock()
                        
                MDBoxLayout:
                    
                    orientation: 'horizontal'
                    size_hint: 1, 0.15
                    pos_hint: {'center_x': 0.5,'center_y': 0.9}
                    padding:['10sp','0sp','10sp','0sp']
                    spacing:'10sp'
                    MDTextField:
                        
                        id:date
                        hint_text: "DATE"
                        mode: 'fill'
                        size_hint: 1, 1
                        
                        font_size:'10sp'
                        readonly:True
                        validator: "date"
                        date_format: "yyyy/mm/dd"
                    MDRectangleFlatIconButton:
                        icon:'calendar'
                        text:'DATE'
                        size_hint:None,1
                        on_press:app.calender()
                        
                MDBoxLayout:        
                    
                
                
            
            
    
            
                    
                    
   
    


'''

   
class MD3Card(MDCard): 
          
    text=StringProperty()
    name=NumericProperty()
    
    
    
    
class mai(MDApp):
    title='TodoApp'
    icon='res/verified.png'
    def build(self):
        self.l=[]
        self.instance=None
        self.task=None
        self.time=None
        self.date=None
        self.ti=time.localtime()
        return Builder.load_string(KV)
    

    def add_task(self):
        new_task_text = self.root.ids.txt_1.text
        if new_task_text != '':
            no=len(self.l)
            card_screen = MD3Card(text=new_task_text,name=no)
            self.root.ids.bx.add_widget(card_screen)
            ob=[no+1,]
            ob.append(new_task_text)
            ob.append('{}:{}:{}'.format(self.ti.tm_hour,self.ti.tm_min,self.ti.tm_sec))
            ob.append('{}-{}-{}'.format(self.ti.tm_mday,self.ti.tm_mon,self.ti.tm_year))
            self.l.append(ob)
            
            
        

        
    def on_checkbox_active(self,instance,*args):
        self.root.ids.bx.remove_widget(instance)
        for i in self.l:
            if instance.name==i[0]:
                self.l.remove(i)
        
        
                
        
    def on_start(self):
        fin=open("./data/recs.dat",'rb+')
        try:
            while True:
                ob=pickle.load(fin)
                self.l.append(ob)
                
                
        except EOFError:
            fin.close()
        
        for i in self.l:
            if i[0]!='NAME':
                self.root.ids.bx.add_widget(MD3Card(text=i[1],name=i[0]))
            
    def save(self,instance):
        new_task=self.root.ids.text.text
        
        self.instance.ids.task.text=new_task
        
            
            
    def edit_button(self,instance):
        self.instance=instance
        self.root.current='info'
        self.txt=(str(instance.ids.task.text))
        self.root.ids.text.text=self.txt
        
        for i in self.l:
            
            if self.instance.name==i[0]:
                
                self.root.ids.time.text=i[2]
                self.root.ids.date.text=i[3]
        
        
        
        
        
    def calender(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        value=str(value)
        self.root.ids.date.text=value
        for i in self.l:
            if self.instance.name==i[0]:
                i[3]=str(value)
                
                
    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        pass
                
    def back(self,instance):
        self.root.current='main'
 
 
    def clock(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        '''
        The method returns the set time.

        :type instance: <kivymd.uix.picker.MDTimePicker object>
        :type time: <class 'datetime.time'>
        '''
        self.root.ids.time.text=str(time)
        for i in self.l:
            if self.instance.name==i[0]:
                i[2]=str(time)
        
    def close_app(self,instance):
        self.stop()
        
    def on_stop(self):
        
        fin=open("./data/recs.dat",'wb+')
        head=['NAME','TASK','TIME','DATE']
        pickle.dump(head,fin)
        for i in range(len(self.l)):
            if self.l[i][0]!='NAME':
                self.l[i][0]=i-1
                pickle.dump(self.l[i],fin)
                
            
        fin.close()
        
        
    
mai().run()