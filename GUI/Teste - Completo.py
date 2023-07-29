from tkinter import *
from tkinter import font
import mysql.connector 
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')
import re


class Conexão_MySQL:
   def __init__(self) -> None:
      self.__host = 'localhost'
      self.__port = '3306'
      self.__user = 'root'
      self.__password = '---' # Não será colocado a senha
      self.__database = 'banco'
      self.conec = mysql.connector.connect(host=self.__host,port=self.__port,user=self.__user,
                           password=self.__password,database=self.__database)
      self.cursor = self.conec.cursor() 
      self.var = ''
   def execute_sql(self,sql):
         self.cursor.execute(sql)
         return self.conec.commit()
   
   def visualizar_dados(self,sql_):
       return pd.read_sql_query(sql=sql_,con=self.conec)
   
   def execute_e_armazene(self,sql_):
       cursor = self.conec.cursor() 
       cursor.execute(sql_)
       return cursor.fetchall()
   
   def mostrar_saldo(self,id_customer):
       saldo = '''SELECT VALOR FROM SALDO WHERE ID ="{}"'''.format(id_customer)
       cursor = self.conec.cursor()
       cursor.execute(saldo)
       return cursor.fetchall()
   
   class Saque:
       def __init__(self,id_cust) -> None:
          self.id = id_cust
          self.saldo = float(Conexão_MySQL().mostrar_saldo(id_customer = self.id)[0][0])
          self.root = Tk()
          self.root.title("Saque")
          self.root.geometry("200x120")
          self.root.configure(bg='black')
          self.font1 = font.Font(size = 20)
          ver = self.root.register(self.validar_numero)
          font1 = font.Font(size = 20)

          Label(self.root, text="Digite um valor para saque:",font=font1,fg='white',bg='black').grid(row=0,column=1)
          self.saque = Entry(self.root,validate='key',validatecommand=(ver, "%P"))
          self.saque.grid(row=1,column=1)
          Button(self.root, text='Confirmar', bg='blue',fg='white', width=15,command=self.get_saque).grid(row=2,column=1,padx=5,pady=10)
          Button(self.root, text='SACAR', bg='red',fg='white', width=10,command=self.sacar).grid(row=3,column=1)

       def validar_numero(self,entrada):
           if entrada == "":
                return True
           return re.match(r'^-?\d*\.?\d*$', entrada) is not None

       def get_saque(self):
           return self.saque.get()

       def sacar(self):
           saque = float(self.get_saque())
           saldo = Conexão_MySQL().mostrar_saldo(id_customer = self.id)[0][0]
           print(float(saldo),saque)
           if (saque > float(self.saldo)) or (saque == 0):
               return Janela_Aviso(msg='O valor inserido não está disponível em seu saldo',t1=280,t2=60)
           else:
                new_value = saldo - saque
                print(new_value)
                print(self.id)
                query ='''UPDATE SALDO SET VALOR ="{}" WHERE ID ="{}";'''.format(new_value,self.id)
                print(query)
                try:
                    print(Conexão_MySQL().execute_sql(sql=query))
                    print("Certo")
                    self.root.destroy()
                    return Janela_Aviso(msg='Valor sacado com sucesso!',t1=160,t2=60)
                    
                except: 
                    print("Erro")
                #return Janela_Aviso(msg='Valor sacado com sucesso!',t1=160,t2=60)

class Janela_LOG_CAD():
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Login/Cadastro")
        self.root.geometry("350x210")
        self.root.configure(bg='black')

        font1 = font.Font(size = 20)
        font2 = font.Font(size = 11)
    
        Label(self.root, text="Sistema Bancário",font=font1,fg='white',bg='black').grid(row=0,column=1)#,columnspan=4)

        Label(self.root, text="USER",font=font2,fg='white',bg='black').grid(row=3,column=0)
        self.login = Entry(self.root)
        
        self.login.grid(row = 3, column = 1,padx=5,pady=5)

        Label(self.root, text="PASSWORD",fg='white',font=font2,bg='black').grid(row=4,column=0)
        self.Password = Entry(self.root,show='*')
        self.Password.grid(row=4,column=1,padx=5,pady=5)

        # NOTE

        Button(self.root, text='Sign In', bg='blue',fg='white', width=10,command=self.close_jan2).grid(row=5,column=1)
        Button(self.root, text='Sign Up', bg = 'green',fg='white', width=10,command=self.close_jan1).grid(row=6,column=1)

        Label(self.root, text="",fg='white',font=font2,bg='black').grid(row=7,column=0)
        Label(self.root, text="Ver cadastros",fg='white',font=font2,bg='black').grid(row=8,column=0)

        Button(self.root, text='Registers',bg ='#8000FF',fg='white', width=10).grid(row=8,column=1)
        self.root.mainloop()

    def user__(self):
        user = str(self.login.get())
        return user
    
    def close_jan1(self):
        self.root.destroy()
        return Janela_CAD()
    
    def close_jan2(self):
        user = str(self.login.get())
        passw = str(self.Password.get())
        query = f'''SELECT NOME,SENHA,ID FROM usuário WHERE NOME = "{user}" and SENHA = "{passw}"'''
        try:
            results = Conexão_MySQL().execute_e_armazene(sql_=query)
            if (user == results[0][0]) and (passw == results[0][1]):
                id_mut = str(results[0][2])
                self.root.destroy()
                Janela_USER(user_= user,id_=id_mut)
        except IndexError:
            print("Erro!")

class Janela_USER():
    
    def __init__(self,user_,id_) -> None:
      self.id_ = id_
      self.user__ = user_
      self.root = Tk()
      self.root.title("Ambiente do Usuário")
      self.root.geometry("400x210")
      self.root.configure(bg='black')
      #self.root.after()
      

      font1 = font.Font(size = 20)
      font2 = font.Font(size = 11)
      Label(self.root, text="Interface do usuário",font=font1,fg='white',bg='black').grid(row=0,column=1)#,columnspan=4)
      Label(self.root, text="Saldo:",font=font2,fg='green',bg='black').grid(row=1,column=0)
      Label(self.root, text="R$ ",font=font1,fg='green',bg='black').grid(row=1,column=1)
      self.saldo_label = Label(self.root, text="",font=font1,fg='green',bg='black')
      self.saldo_label.grid(row=1,column=2)
      self.atualizar_dados()

      Button(self.root, text='SACAR', bg='red',fg='white', width=10,command = self.push_func).grid(row=2,column=1)

    
    def atualizar_dados(self):
        self.atualizar_saldo()
        # Defina o intervalo de tempo para atualização (5 segundos neste exemplo)
        intervalo = 500
        self.root.after(intervalo, self.atualizar_dados)

    def atualizar_saldo(self):
        novo_saldo = self.PUSH_SALDO()
        self.saldo_label.config(text="R$" + str(novo_saldo))

    def push_func(self):
        return Conexão_MySQL().Saque(id_cust=self.id_)
        
    def PUSH_SALDO(self) -> str:
 
        usuario = self.user__
        query = f'''SELECT ID FROM usuário WHERE NOME = "{usuario}"'''
        try:
            results = Conexão_MySQL().execute_e_armazene(sql_=query)
            id_cust = int(results[0][0])
            try:
                results2 = Conexão_MySQL().mostrar_saldo(id_customer=id_cust)[0][0]
                return results2
            except:
              return 'Erro'
        except:
            return "Erro"

class Janela_CAD():
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Cadastro")
        self.root.geometry("350x210")
        self.root.configure(bg='black')

class Janela_REG():
    pass

class Janela_Aviso():
    def __init__(self,msg,t1,t2) -> None:
        self.msg = msg
        self.root = Tk()
        self.root.title("WARNING")
        self.root.geometry("{}x{}".format(t1,t2))
        self.root.configure(bg='black')
        Label(self.root, text=msg,fg='YELLOW',bg='black').grid(row=0,column=1)
        Button(self.root, text='Ok', bg='red',fg='white', width=10,command=self.end_window).grid(row=1,column=1)
    def end_window(self):
        self.root.destroy()

Janela_LOG_CAD()
