# Interface para a plataforma de Planetas do Star Wars

#importacoes
import requests
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from urllib.parse import parse_qs

# cria janela da interface grafica
window = Tk() 
window.title("Os Planetas de Star Wars") 
window.geometry('400x200')

# cria abas para diferentes funcoes da api
tab_control = ttk.Notebook(window) 
tab_list = ttk.Frame(tab_control) 
tab_search = ttk.Frame(tab_control) 
tab_insert = ttk.Frame(tab_control) 
tab_delete = ttk.Frame(tab_control) 
tab_control.add(tab_list, text='Listar planetas') 
tab_control.add(tab_search, text='Procurar planeta')
tab_control.add(tab_insert, text='Inserir planeta')
tab_control.add(tab_delete, text='Deletar planeta')
tab_control.pack(expand=1, fill='both')

# texto para listar os planetas
lbl_list = Label(tab_list, text = "Para listar planetas: ") 
lbl_list.grid(column = 0, row = 1)

# metodo do botao e botao para listar os planetas
def list_planets():
    response1 = requests.get("http://127.0.0.1:5000/planets")
    text1 = response1.json()['result']
    messagebox.showinfo('Lista de planetas', json.dumps(text1, indent = 3))

btn_list = Button(tab_list, text = "clique aqui!", command = list_planets) 
btn_list.grid(column = 1, row = 1)

# texto para buscar e listar um so planeta
lbl_search = Label(tab_search, text = "Para buscar um planeta, selecione: ") 
lbl_search.grid(column = 0, row = 0)
lbl_search_fill = Label(tab_search, text = "Preencha o valor: ") 
lbl_search_fill.grid(column = 0, row = 2)

# escolha entre id e nome
selected = IntVar()
rad_id = Radiobutton(tab_search, text = 'Id', value = 1, variable = selected) 
rad_nome = Radiobutton(tab_search, text = 'Nome', value = 2, variable = selected)
rad_id.grid(column = 1, row = 0)
rad_nome.grid(column = 2, row = 0)

# campo para inserir o dado da busca (id ou nome)
txt_search = Entry(tab_search, width = 20) 
txt_search.grid(column = 1, row = 2)

# metodo do botao e botao para buscar um planeta
def search_planets():
    value = selected.get()
    if value == 1:
        if str.isdigit(txt_search.get()):
            response2 = requests.get("http://127.0.0.1:5000/planets?planetID=" + txt_search.get())
            text2 = response2.json()['result']
        else:
            text2 = "Id invalida, deve ser um numeral!"
    elif value == 2:
        response2 = requests.get("http://127.0.0.1:5000/planets?name=" + txt_search.get())
        text2 = response2.json()['result']
    messagebox.showinfo('Resultado da busca', json.dumps(text2, indent = 3))

btn_search = Button(tab_search, text = "e clique aqui!", command = search_planets) 
btn_search.grid(column = 1, row = 3)

# texto para inserir um novo planeta
lbl_insert = Label(tab_insert, text = "Para inserir um planeta, preencha: ") 
lbl_insert.grid(row = 1)
lbl_insert_name = Label(tab_insert, text = "Nome: ")
lbl_insert_name.grid(column = 0, row = 2)
lbl_insert_terrain = Label(tab_insert, text = "Terreno: ")
lbl_insert_terrain.grid(column = 0, row = 3)
lbl_insert_climate = Label(tab_insert, text = "Clima: ")
lbl_insert_climate.grid(column = 0, row = 4)

# campos para inserir os dados do planeta
txt_insert_name = Entry(tab_insert, width = 20) 
txt_insert_name.grid(column = 1, row = 2)
txt_insert_terrain = Entry(tab_insert, width = 20) 
txt_insert_terrain.grid(column = 1, row = 3)
txt_insert_climate = Entry(tab_insert, width = 20) 
txt_insert_climate.grid(column = 1, row = 4)

# metodo do botao e botao para inserir um planeta
def insert_planet():
    # configuracoes da conexao com a base de dados
    app = Flask(__name__)
    app.config['MONGO_DBNAME'] = 'starWars_planets_db'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/starWars_planets_db'

    mongo = PyMongo(app)
    planets = mongo.db.planetsTable

    # requisita um POST para cadastrar um novo planeta
    planetID = planets.count() + 1
    response3 = requests.post("http://127.0.0.1:5000/planets", 
                            json = {"planetID": planetID, 
                                    "name": txt_insert_name.get(), 
                                    "climate": txt_insert_climate.get(), 
                                    "terrain": txt_insert_terrain.get()})
    text3 = response3.json()['result']
    messagebox.showinfo('Resultado da insercao do planeta', json.dumps(text3, indent = 3))

btn_search = Button(tab_insert, text = "e clique aqui!", command = insert_planet) 
btn_search.grid(column = 1, row = 5)

# texto para buscar e deletar um planeta
lbl_delete = Label(tab_delete, text = "Selecione o planeta pelo nome: ") 
lbl_delete.grid(column = 0, row = 1)

# campo para inserir o nome do planeta
txt_delete = Entry(tab_delete, width = 20) 
txt_delete.grid(column = 1, row = 1)

# metodo do botao e botao para buscar um planeta
def delete_planet():
    response4 = requests.delete("http://127.0.0.1:5000/planets/" + txt_delete.get())
    text4 = response4.json()['result']
    messagebox.showinfo('Resultado da busca', json.dumps(text4, indent = 3))

btn_search = Button(tab_delete, text = "e clique aqui!", command = delete_planet) 
btn_search.grid(column = 2, row = 1)

window.mainloop()
