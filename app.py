import MySQLdb
import time
import socket
import threading
import sys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty,ObjectProperty
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton

#################################################################
UserName = ""
UserPassword = ""
LabelText = " "

#################################################################
class DD_ProjectRoot(BoxLayout):
    def __init__ (self, **kwargs):
        super(DD_ProjectRoot, self).__init__(**kwargs)
        self.ids.kivy_screen_manager.current = "start_screen"
        
        
    def SetUserName(self, username):
        global UserName
        UserName = username
        
    def SetUserPassword(self, password):
        global UserPassword
        UserPassword = password               
        
    def Login(self):
        global LabelText
        try:
            db = MySQLdb.connect("localhost","root","zxc@123","dd_project" )
            cursor = db.cursor()
            sql = "SELECT * FROM users WHERE username ='%s'" % (UserName)
            # Execute the SQL command
            cursor.execute(sql)
            result = cursor.fetchone()
            if result[1] == UserName and result[2] == UserPassword:
                print("LoggedIn")
                self.ids.kivy_screen_manager.current = "to_do_list"
                ToDoList.on_start(self)
                
            else:
                LabelText = "* Incorrect Username or Password" 
                StartScreen.UpdateLabelText()              
            # Commit your changes in the database
            db.commit()
        except:
            LabelText = "* Incorrect Username or Password"
            StartScreen.UpdateLabelText() 
            # Rollback in case there is any error
            db.rollback()
            
        db.close()

    def SignUp(self):
        try:
            db = MySQLdb.connect("localhost","root","zxc@123","dd_project" )
            cursor = db.cursor()
            sql = "INSERT INTO users(username, password) VALUES ('%s', '%s')" %(UserName, UserPassword)
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        db.close()

        
        

#################################################################
class DD_ProjectApp(App):
    global LabelText
    def __init__ (self, **kwargs):
        super(DD_ProjectApp, self).__init__(**kwargs)
        
    def build(self):
        return DD_ProjectRoot()
        
    def on_stop(self):
        
        try:
            db = MySQLdb.connect("localhost","root","zxc@123","dd_project" )
            cursor = db.cursor()
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
            client = Client("192.168.0.100", 10050, result, "users")
            sql = "SELECT * FROM todo"
            cursor.execute(sql)
            result2 = cursor.fetchall()
            client2 = Client("192.168.0.100", 10050, result2, "todos")
            db.commit()
        except:
            db.rollback()
            
        db.close()
        print("stop")

    
#################################################################
class StartScreen(Screen):
    global LabelText
    mylabel = StringProperty(LabelText)
    
    def __init__ (self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

    def UpdateLabelText():
        mylabel = StringProperty(LabelText)

        
#################################################################
class ToDoListItemButton(ListItemButton):
    pass

#################################################################
class ToDoList(BoxLayout, Screen):
    global UserName 
    todoinput = ObjectProperty()
    listoftodo = ObjectProperty()
    
    def on_start(self):
        x = self.ids.to_do_list
        print(x.listoftodo)
        try:
            db = MySQLdb.connect("localhost","root","zxc@123","dd_project" )
            cursor = db.cursor()
            sql = "SELECT * FROM todo WHERE username = '%s'" %(UserName)
            # Execute the SQL command
            cursor.execute(sql)
            result = cursor.fetchall();
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        db.close()
        for z in result:
            x.listoftodo.adapter.data.extend([z[2]])
            x.listoftodo._trigger_reset_populate()
            
    
    def submit_to_do(self):
        todo = self.todoinput.text
        self.listoftodo.adapter.data.extend([todo])
        self.listoftodo._trigger_reset_populate()
        try:
            
            db = MySQLdb.connect("localhost","root","zxc@123","dd_project" )
            cursor = db.cursor()
            sql = "INSERT INTO todo(username, todos) VALUES ('%s', '%s')" %(UserName, todo)
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        db.close()
        
        
    def delete_to_do(self):
       if self.listoftodo.adapter.selection: 
            selection = self.listoftodo.adapter.selection[0].text
            self.listoftodo.adapter.data.remove(selection)
            self.listoftodo._trigger_reset_populate()
            try:
                db = MySQLdb.connect("localhost","root","zxc@123","dd_project" )
                cursor = db.cursor()
                sql = "DELETE FROM todo WHERE todos = '%s'" %(selection)
                # Execute the SQL command
                cursor.execute(sql)
                # Commit your changes in the database
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            db.close()
        
    def replace_to_do(self):
        if self.listoftodo.adapter.selection:
            selection = self.listoftodo.adapter.selection[0].text
            self.listoftodo.adapter.data.remove(selection)
            todo = self.todoinput.text
            self.listoftodo.adapter.data.extend([todo])
            self.listoftodo._trigger_reset_populate()
            try:
                db = MySQLdb.connect("localhost","root","zxc@123","dd_project" )
                cursor = db.cursor()
                sql = "SELECT * FROM todo WHERE todos = '%s' AND username = '%s'" %(selection, UserName)
                # Execute the SQL command
                cursor.execute(sql)
                result = cursor.fetchall();
                sql = "UPDATE todo SET todos = '%s' WHERE id = '%d'" %(todo, result[0][0])
                cursor.execute(sql)
                # Commit your changes in the database
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            db.close()
        
################################################################################################################################################################
################################################################################################################################################################

class Client: 
    def sendMsg(self, sock, data):
        x = "..1..::"
        for i in data:
            for z in i:
              x = x + ";" + str(z)  
            x = x + "::"
        sock.send(bytes(x, 'utf-8'))
        #sock.shutdown()
        #sock.close()
        return
    
    def sendMsg2(self, sock, data):
        x = "..2..::"
        for i in data:
            for z in i:
              x = x + ";" + str(z)  
            x = x + "::"
        sock.send(bytes(x, 'utf-8'))
        #sock.shutdown()
        #sock.close()
        
    def __init__(self, address, ServerPort, data, flag):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, ServerPort))
        if flag == "users":
            self.sendMsg(sock,data)
        if flag == "todos":
            self.sendMsg2(sock,data)
        


#################################################################   
if __name__ == '__main__':
    DD_ProjectApp().run()
    
    


