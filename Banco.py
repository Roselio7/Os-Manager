import sqlite3
from datetime import date
from datetime import timedelta

DATAINI=""
def Criarbanco():
    conn = sqlite3.connect('ideal.db')
    c = conn.cursor()
    c.execute(""" 
                   CREATE TABLE IF NOT EXISTS Clientes (
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         Nome TEXT UNIQUE,
                         Endereco TEXT, 
                         Celular TEXT,
                         Bairro TEXT,
                         Cidade TEXT)""")
    conn.commit()
    c.execute(""" 
                   CREATE TABLE IF NOT EXISTS empresa (
                         nome TEXT,
                         rua TEXT, 
                         bairro TEXT,
                         cidade TEXT,
                         tel TEXT,
                         cpf TEXT,
                         garantia TEXT)""")
    conn.commit()
    c.execute(""" 
                   CREATE TABLE IF NOT EXISTS validade ( 
                         data TEXT )""")
    conn.commit()
    c.execute(""" 
                   CREATE TABLE IF NOT EXISTS senhaativar ( 
                         senha TEXT )""")
    conn.commit()
    c.execute("""CREATE TABLE IF NOT EXISTS SenhaLogin (Senha TEXT)""")
    conn.commit()
    
    
    
    ######################## Outra tabela ################
    c.execute(""" CREATE TABLE IF NOT EXISTS Aparelhos (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 Nome TEXT,
                                 Aparelho TEXT, 
                                 Marca TEXT,
                                 Modelo TEXT, 
                                 Serie TEXT,
                                 DefeitoInfo TEXT,
                                 InfoAdd TEXT,
                                 Servico TEXT,
				                 Pecas TEXT,
                                 DataEntrada TEXT,
                                 DataConsertado TEXT,
                                 DataEntregue TEXT,
                                 Preço TEXT,
                                 Situacao TEXT,
                                 Status TEXT,
                                 ValorPago)""")

    conn.commit()
    conn.close()

def Datar():
    global DATAINI
    conn = sqlite3.connect('ideal.db')
    c = conn.cursor()
    c.execute('select data from validade')
    dado=c.fetchone()
    var=dado[0] if dado != None else None
    DATAINI=var if var != None else str(date.today())
    if var == None:
        hje = date.today()
        c.execute('insert into validade (data) values (?)', (hje,))
        conn.commit()

def DataAtual():
    return date.today()

def Verifica():
    global DATAINI
    ano = int(DATAINI[0:4:1])
    mes = int(DATAINI[5:7:1])
    dia = int(DATAINI[8:10:1])
   
    vencimento = date(ano, mes, dia) + timedelta(days=15)
    if date.today() <= vencimento:
        return "OK"
    if date.today() > vencimento:
        return "Vencido"
    
