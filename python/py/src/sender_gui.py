import kivy
import os
import pandas as pd
import csv
from csv import DictReader
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_file('C:/project/whatsapp_message_sender/python/kv/kvfileforgui.kv')

class mainwindow(Screen):
    if os.path.isfile("C:/Program Files/WMS/sendmessagetopersonconfig.csv") and os.path.isfile("C:/Program Files/WMS/sendmessagetoallconfig.csv") == 1:
        os.remove("C:/Program Files/WMS/sendmessagetopersonconfig.csv")
        os.remove("C:/Program Files/WMS/sendmessagetoallconfig.csv")
    else:
        if os.path.isdir("C:/Program Files/WMS"):
            pass
        else:
            os.mkdir("C:/Program Files/WMS")   
    personmessagecsv = open("C:/Program Files/WMS/sendmessagetopersonconfig.csv","x") 
    alltomessagecsv = open("C:/Program Files/WMS/sendmessagetoallconfig.csv","x")

    def gomessagesendwindow(self):
        sm.current = "messagewindow"
    def gowholemessagesend(self):
        sm.current = "wholemessage" 
    def gosettingswindow(self):
        sm.current = "settingswindow"   

class messagesendwindow(Screen): 
    telno = ObjectProperty(None)
    message = ObjectProperty(None)
    def kaydetmebutonunabasti(self):
        #golang dosyaları patha eklenecek oto olarak .battan 
        if self.telno.text != "" and self.message.text != "" and self.telno.text.count("90") == 1 and len(self.telno.text) == 12:
            with open('C:/Program Files/WMS/sendmessagetopersonconfig.csv', 'w') as f:
                fieldnames = ['telno', 'message']
                writetocsv = csv.DictWriter(f, fieldnames=fieldnames)
                writetocsv.writeheader()
                writetocsv.writerow({'telno' : self.telno.text, 'message' : self.message.text})
            tirnakisareti = '"'      
            bosluk = " "
            with open('C:/Program Files/WMS/sendmessagetopersonconfig.csv', 'r') as reader:
                csv_dict_reader = DictReader(reader)
                for row in csv_dict_reader:
                    giristelno = row['telno']
                    girismessage = row['message']
            if os.system("messagesend.exe"+bosluk+giristelno+bosluk+tirnakisareti+bosluk+girismessage+bosluk+tirnakisareti) == 1:
                unknownerror()
            else:
                successmessage()

        else:
            invalidmessage()                 
    def returnmainwindow(self):
        sm.current = "main"

class wholemessagesend(Screen):
    telnos = ObjectProperty(None)
    ortakmesaj = ObjectProperty(None)
    def kaydetmebutonunabasti(self):
        if self.telnos.text != "" and self.ortakmesaj.text != "" and self.telnos.text.count("90") == 1:
            if self.telnos.text.count(",") == 1:              
                with open('C:/Program Files/WMS/sendmessagetoallconfig.csv', 'w') as f:
                    fieldnames = ['telnos', 'ortakmesaj']
                    writetocsv = csv.DictWriter(f, fieldnames=fieldnames)
                    writetocsv.writeheader()
                    writetocsv.writerow({'telnos': self.telnos.text, 'ortakmesaj': self.ortakmesaj.text})
    def returnmainwindow(self):
        sm.current = "main"
class settingsmainwindow(Screen):
    def returnmainwindow(self):
        sm.current = "main"
class WindowManager(ScreenManager):
    pass

def invalidmessage():
    pop = Popup(title='Mesaj gönderme sırasında hata',
                  content=Label(text='Telefon numarasını veya mesajı kurallara göre yazmamış olabilirsiniz! (press esc)'),
                  size_hint=(None, None), size=(600, 400))
    pop.open()
def successmessage():
    pop = Popup(title='Mesaj gönderildi',
                  content=Label(text='Mesaj başarıyla gönderildi! (press esc)'),
                  size_hint=(None, None), size=(600, 400))
    pop.open()    
def unknownerror():
    pop = Popup(title='Bilinmeyen hata',
                  content=Label(text='Bilinmeyen bir hata ile karşılaşıldı! (press esc)'),
                  size_hint=(None, None), size=(600, 400))
    pop.open()     

sm = WindowManager()

screens = [messagesendwindow(name="messagewindow"),mainwindow(name="main"),wholemessagesend(name="wholemessage"),settingsmainwindow(name="settingswindow")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"


class WMS(App):
    def build(self):
        return sm


if __name__ == "__main__":
    WMS().run()        