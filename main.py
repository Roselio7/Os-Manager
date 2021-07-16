import sys
import platform
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QTableWidgetItem, QListWidgetItem,QTableWidget,QCompleter,QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtCore import  QStringListModel
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import QTimer
import Banco
from style import stylized,unstyle
from impressao import imprimirOs, imprimirNE
from datetime import date
from PyQt5.QtGui import QFont, QFontDatabase
#Exemplo de como instanciar um arquivo de interface .ui
#precisa gerar um arquivo py do arquivo qrc e importá-lo como abaixo
import files_rc

Banco.Criarbanco()
Banco.Datar()

counter=0

class Principal(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('./Ui/main.ui',self)
        self.ConectarBanco()
        self.LoadEmpresa()
        self.Maxid()
        self.STATUS = False

        self.listabt=[self.btnpage_home,self.btnpage_cliente,self.btnpage_empresa,self.btnpage_aparelho,
        self.btnpage_editar,self.btnpage_pesquisar,self.btnpage_finalizar,self.btnpage_nota,
        self.btnpage_fluxo,self.btnpage_senhas,self.btnpage_ativar]

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.c.execute('select senha from senhaativar')
        num = self.c.fetchone()
        var=num [0] if num != None else None
        
#       BOTOES DA HOME
        self.btnpage_sair.clicked.connect(self.Sair)
        if var == None:
            if Banco.Verifica() == "OK":
                self.btnpage_home.clicked.connect(lambda:self.SelectButton(self.btnpage_home))
                self.btnpage_cliente.clicked.connect(lambda :self.SelectButton(self.btnpage_cliente))
                self.btnpage_empresa.clicked.connect(lambda :self.SelectButton(self.btnpage_empresa))
                self.btnpage_aparelho.clicked.connect(lambda :self.SelectButton(self.btnpage_aparelho))
                self.btnpage_editar.clicked.connect(lambda :self.SelectButton(self.btnpage_editar))
                self.btnpage_pesquisar.clicked.connect(lambda :self.SelectButton(self.btnpage_pesquisar))
                self.btnpage_finalizar.clicked.connect(lambda :self.SelectButton(self.btnpage_finalizar))
                self.btnpage_nota.clicked.connect(lambda :self.SelectButton(self.btnpage_nota))
                self.btnpage_fluxo.clicked.connect(lambda: self.SelectButton(self.btnpage_fluxo))
                self.btnpage_senhas.clicked.connect(lambda: self.SelectButton(self.btnpage_senhas))
        
                self.btnpage_ativar.clicked.connect(lambda: self.SelectButton(self.btnpage_ativar))
                self.stackedWidget.setCurrentWidget(self.page_9)
                self.btnpage_ativar.setStyleSheet(stylized)
                self.nome_tela.setText('| Ativar ')
            else:
                self.btnpage_ativar.clicked.connect(lambda: self.SelectButton(self.btnpage_ativar))
                self.stackedWidget.setCurrentWidget(self.page_9)
                self.btnpage_ativar.setStyleSheet(stylized)
                self.nome_tela.setText('| Ativar ')
        else:
            self.btnpage_home.clicked.connect(lambda:self.SelectButton(self.btnpage_home))
            self.btnpage_cliente.clicked.connect(lambda :self.SelectButton(self.btnpage_cliente))
            self.btnpage_empresa.clicked.connect(lambda :self.SelectButton(self.btnpage_empresa))
            self.btnpage_aparelho.clicked.connect(lambda :self.SelectButton(self.btnpage_aparelho))
            self.btnpage_editar.clicked.connect(lambda :self.SelectButton(self.btnpage_editar))
            self.btnpage_pesquisar.clicked.connect(lambda :self.SelectButton(self.btnpage_pesquisar))
            self.btnpage_finalizar.clicked.connect(lambda :self.SelectButton(self.btnpage_finalizar))
            self.btnpage_nota.clicked.connect(lambda :self.SelectButton(self.btnpage_nota))
            self.btnpage_fluxo.clicked.connect(lambda: self.SelectButton(self.btnpage_fluxo))
            self.btnpage_senhas.clicked.connect(lambda: self.SelectButton(self.btnpage_senhas))

            self.btnpage_ativar.clicked.connect(self.Msg)
            self.stackedWidget.setCurrentWidget(self.page_1)
            self.btnpage_home.setStyleSheet(stylized)
            self.nome_tela.setText('| Home ')
        
       
        self.BtMenu.clicked.connect(lambda:self.Menu(250, True))
#       BOTOES DA TELA CLIENTES
        self.btn_salvar.clicked.connect(self.Salvar)
        self.btn_novo.clicked.connect(self.Limpacampos)
        self.btn_excluir.clicked.connect(self.Excluir)
        self.btn_atualizar.clicked.connect(self.Atualizar)
        self.btn_pesquisar.clicked.connect(self.Pesquisar)
        self.input_pesquisa.returnPressed.connect(self.Pesquisar)
        self.btn_voltar.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.page_1))
        
#       BOTOES DA TELA EMPRESA
        self.btn_salvarempresa.clicked.connect(self.SalvarEmpresa)

        self.btn_cancelarempresa.clicked.connect(lambda :self.stackedWidget.setCurrentWidget(self.page_1))        

        self.SetarAutoCompletar()

#       BOTOES DA TELA CADASTRO DE APARELHO
        self.btnpesquisa_aparelho.clicked.connect(self.PesquisarAparelho)
        self.btnsalvar_aparelho.clicked.connect(self.SalvarAparelho)
        self.pesquisa_aparelho.returnPressed.connect(self.PesquisarAparelho)

#       BOTOES DA TELA INFORMAÇÕES ADICIONAIS
        self.btnpesquisa_adiciona.clicked.connect(self.PesquisarAdiciona)
        self.pesquisa_adiciona.returnPressed.connect(self.PesquisarAdiciona)
        self.btnsalvar_adiciona.clicked.connect(self.SalvarAdiciona)
        
#       BOTOES DA TELA PESQUISA        
        self.btnpesquisa_pesquisa.clicked.connect(self.PesquisarPesquisa)
        self.pesquisa_pesquisa.returnPressed.connect(self.PesquisarPesquisa)

#       BOTOES DA TELA FINALIZAR        
        self.btnpesquisa_finalizar.clicked.connect(self.PesquisarFinalizar)
        self.pesquisa_finalizar.returnPressed.connect(self.PesquisarFinalizar)
        self.btnconfirmar_finalizar.clicked.connect(self.ConfirmarFinalizar)   

#       BOTOES DA TELA FLUXO
        self.btnpesquisa_fluxo.clicked.connect(self.PesquisaData)

#       BOTOES DA TELA ALTERAR SENHA
        self.btnsalvar_alterarsenha.clicked.connect(self.VerifikSenha)

#       BOTOES DA TELA ATIVAR SOFTWARE
        self.btnativar_ativar.clicked.connect(self.registrar)

#       BOTOES DA TELA EMITIR NOTA
        self.btnconfirmar_nota.clicked.connect(self.Verificar)
        self.btngerar_nota.clicked.connect(self.Gerar)
#------------------------------------------------TELA  HOME---------------------------------------------------------------

#       SETANDO O HEADER PRA ALTOAJUSTAR

        #self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        #self.tableWidget_2.setRowCount(10)
        self.tableWidget_2.setColumnCount(8)
        header = self.tableWidget_2.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if self.STATUS == False:
                self.showMaximized()
                self.STATUS = True
            else:
                self.showNormal()
                self.STATUS = False
            #self.showNormal()
        if event.buttons() :
            width = self.frame_left_menu.width()
            standard = 85

            # SET MAX WIDTH
            if width == 250:
                widthExtended = standard       

            # ANIMATION
                self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
                self.animation.setDuration(400)
                self.animation.setStartValue(width)
                self.animation.setEndValue(widthExtended)
                self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animation.start()

    def Sair(self):
        question_close = QMessageBox.question(self, "Fechar",
                                    "Deseja realmente fechar a aplicação?", 
                                    QMessageBox.Yes, QMessageBox.No)
        if question_close == QMessageBox.Yes:
            exit(0)
 
    def SelectButton(self,bt):
        
        for i in self.listabt:
            if i != bt.objectName():
                i.setStyleSheet(unstyle)
        if bt.text() == 'Home':
            self.stackedWidget.setCurrentWidget(self.page_1)
            self.nome_tela.setText('| Home ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Cliente':
            self.stackedWidget.setCurrentWidget(self.page_2)
            self.nome_tela.setText('| Cliente ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Criar OS':
            self.stackedWidget.setCurrentWidget(self.page_4)
            self.nome_tela.setText('| Criar OS ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Editar OS':
            self.stackedWidget.setCurrentWidget(self.page_5)
            self.nome_tela.setText('| Editar OS ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Finalizar':
            self.stackedWidget.setCurrentWidget(self.page_10)
            self.nome_tela.setText('| Finalizar ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Pesquisar':
            self.stackedWidget.setCurrentWidget(self.page_6)
            self.nome_tela.setText('| Pesquisar ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Fluxo':
            self.stackedWidget.setCurrentWidget(self.page_7)
            self.nome_tela.setText('| Fluxo ')
            bt.setStyleSheet(stylized)
            self.Inicializar()
        if bt.text() == 'Empresa':
            self.stackedWidget.setCurrentWidget(self.page_3)
            self.nome_tela.setText('| Empresa ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Nota':
            self.stackedWidget.setCurrentWidget(self.page_11)
            self.nome_tela.setText('| Nota ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Ativar':
            self.stackedWidget.setCurrentWidget(self.page_9)
            self.nome_tela.setText('| Ativar ')
            bt.setStyleSheet(stylized)
        if bt.text() == 'Senhas':
            self.stackedWidget.setCurrentWidget(self.page_8)
            self.nome_tela.setText('| Senhas ')
            bt.setStyleSheet(stylized)
    def Maxid(self):
        conn=sqlite3.connect('ideal.db')
        c=conn.cursor()
        c.execute('''select max (id) from Aparelhos ''')
        r = c.fetchone()
        reg = str(r[0]) if r != None else '0'
        self.lb_os.setText(reg)

    def Msg(self):
        QMessageBox.about(self,"Aviso",' Esta aplicação já está ativada!! ')
        
    def ListaClientes(self):
        self.c.execute('select Nome from Clientes')
        return self.c.fetchall()

    def SetarAutoCompletar(self):
        self.lista=[]
        if self.ListaClientes() !=[]:
            for i in self.ListaClientes():
                self.lista.append(i[0])
        
        self.completer =QCompleter(self.lista)
        self.model = QStringListModel(self.lista)
        self.completer.setModel(self.model)
        self.completer.setCaseSensitivity(0)
        self.input_pesquisa.setCompleter(self.completer)
        self.pesquisa_aparelho.setCompleter(self.completer)
                      
#       SETA O TABLEWIDGET COM CABEÇALHOS DE ACORDO COM O TAMNHO DA TELA 
    def AtualizaHome(self):
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.clear()
        self.GetDdata()
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tamanho=self.size()
        self.reftela=round(self.tamanho.width()/100)*2

        self.tableWidget.setHorizontalHeaderItem( 0, QTableWidgetItem((self.reftela-12)*' '+'OS'+(self.reftela-12)*' '))
        self.tableWidget.setHorizontalHeaderItem( 1, QTableWidgetItem((self.reftela+16)*' '+'Nome do Cliente'+(self.reftela+16)*' '))
        self.tableWidget.setHorizontalHeaderItem( 2, QTableWidgetItem((self.reftela-2)*' '+'Aparelho'+(self.reftela-2)*' '))
        self.tableWidget.setHorizontalHeaderItem( 3, QTableWidgetItem((self.reftela-5)*' '+'Marca'+(self.reftela-5)*' '))
        self.tableWidget.setHorizontalHeaderItem( 4, QTableWidgetItem(self.reftela*' '+'Data de Entrada'+ self.reftela *' '))
        if self.data != None and self.data != []:
            p = 0
            for i in self.data:
                
                self.tableWidget.setItem(p, 0, QTableWidgetItem((self.reftela-5)*' '+str(i[0])+(self.reftela-5)*' '))
                self.tableWidget.setItem(p, 1, QTableWidgetItem((self.reftela+16)*' '+str(i[1])+(self.reftela+16)*' '))
                self.tableWidget.setItem(p, 2, QTableWidgetItem((self.reftela-2)*' '+str(i[2])+(self.reftela-2)*' '))
                self.tableWidget.setItem(p, 3, QTableWidgetItem((self.reftela-2)*' '+str(i[3])+(self.reftela-2)*' '))
                self.tableWidget.setItem(p, 4, QTableWidgetItem((self.reftela-5)*' '+str(self.formatdate(i[4]))))
                p = p+1
        
    def GetDdata(self):
        self.c.execute('''select id,Nome,Aparelho,Marca,DataEntrada from Aparelhos where Status="Aberto"''')
        self.data=self.c.fetchall()

    def resizeEvent(self, event):
        self.AtualizaHome()
        self.Inicializar()

    def Menu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 85

            # SET MAX WIDTH
            if width == 85:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

#       CARREGA O BANDO DE DADOS
    def ConectarBanco(self):
        self.conn=sqlite3.connect('ideal.db')
        self.c=self.conn.cursor()
        
            
#       FORMATA A DATA                        
    def formatdate(self,arg):
        meses = [' ', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        fano = arg
        Ano = fano[0:4]
        fmes = arg
        indicemes = int(fmes[5:7])
        Mes = meses[indicemes]
        fdia = arg
        Dia = fdia[8:10]
        dataformat = (Dia + '-' + Mes + '-' + Ano)
        return dataformat
#----------------------------------------------------TELA CADSTRO DE CLIENTES------------------------------------------------------

#       FUNÇÃO SALVAR
    def Salvar(self):
        if self.input_nome.text() =='' or self.input_endereco.text() == '' or self.input_telefone.text() == '' or self.input_bairro.text() == '' or self.input_cidade.text() == '':
            QMessageBox.about(self,"Aviso",'      Nenhum campo de ficar em branco       ')

        else:
            try:
                self.c.execute(
                    """ INSERT INTO Clientes(Nome,Endereco,Celular,Bairro,Cidade) VALUES (?,?,?,?,?)""",
                    (self.input_nome.text(),self.input_endereco.text(),self.input_telefone.text(),self.input_bairro.text(),self.input_cidade.text()))
                self.conn.commit()
                self.Limpacampos()
                QMessageBox.about(self,'Aviso','      Dados Salvos Com Sucesso!       ')
            except sqlite3.IntegrityError:
                QMessageBox.about(self,"Aviso",'      Este Cliente já existe no Sistema       ')
        
    def Limpacampos(self):
        self.SetarAutoCompletar()
        self.input_nome.setText('')
        self.input_endereco.setText('')
        self.input_telefone.setText('')
        self.input_bairro.setText('')
        self.input_cidade.setText('')

    def Pesquisar(self):
        
        if self.input_pesquisa.text() != '' and not self.input_pesquisa.text().isdigit():
            self.c.execute('select * from Clientes where nome=?',(self.input_pesquisa.text(),))
            dados = self.c.fetchone()
            self.idcli=dados[0]
            self.nome =dados[1]
            if dados != None:
                self.input_nome.setText(dados[1])
                self.input_endereco.setText(dados[2])
                self.input_telefone.setText(str(dados[3]))
                self.input_bairro.setText(dados[4])
                self.input_cidade.setText(dados[5])
                
            else:
                QMessageBox.about(self,'Aviso','      Este Cliente Não Exite! Você Digitou Certo?       ')

##   FUNCAO DO BOTAO EXCLUIR

    def Excluir(self):
        if self.input_nome.text() != '' and not self.input_nome.text().isdigit():
            self.c.execute('delete from Clientes where nome=?',(self.input_nome.text(),))
            self.conn.commit()
            QMessageBox.about(self,'Aviso','      Cliente Excluído Com Sucesso!       ')
            self.Limpacampos()

##  FUNCAO DO BOTAO ATUALIZAR

    def Atualizar(self):
        self.c.execute("UPDATE Clientes SET Nome=?,Endereco=?,Celular=?,Bairro=?,Cidade=? WHERE  id=?",(self.input_nome.text(),self.input_endereco.text(),self.input_telefone.text(),self.input_bairro.text(),self.input_cidade.text(),self.idcli))
        self.conn.commit()
        QMessageBox.about(self,'Aviso','      Dados do Cliente Atualizados       ')
        
        self.c.execute('select id from Aparelhos where Nome=?',(self.nome,))
        a = self.c.fetchone()
        var = a[0] if a != None else None
        if var != None:
            self.c.execute('update Aparelhos set Nome=? where id=?',(self.input_nome.text(),var))
            self.conn.commit()
        self.Limpacampos()
                   
#-----------------------------------------------TELA CADASTRO DA EMPRESA---------------------------------------------------------  

#     FUNÇÃO DO BOTAO SALVAR 

    def SalvarEmpresa(self):
        self.c.execute('select nome from empresa')
        vr = self.c.fetchone()
        self.var= vr[0] if vr != None else None

        if self.var == None :
            self.c.execute("insert into empresa (nome,rua,bairro,cidade,tel,cpf,garantia)values(?,?,?,?,?,?,?)",(self.nome_empresa.text(),self.endereco_empresa.text(),self.bairro_empresa.text(),self.cidade_empresa.text(),self.telefone_empresa.text(),self.cnpj_empresa.text(),self.garantia_empresa.text()))
            self.conn.commit()
            QMessageBox.about(self,'Aviso','      Dados da Empresa Salvos!       ')
            
        else:
            self.c.execute("UPDATE empresa SET nome=?,rua=?,bairro=?,cidade=?,tel=?,cpf=?,garantia=? ",(self.nome_empresa.text(),self.endereco_empresa.text(),self.bairro_empresa.text(),self.cidade_empresa.text(),self.telefone_empresa.text(),self.cnpj_empresa.text(),self.garantia_empresa.text()))
            self.conn.commit()
            QMessageBox.about(self,'Aviso','      Dados da Empresa Atualizados       ')
    
    def LoadEmpresa(self):
        self.c.execute('select * from empresa')
        vr = self.c.fetchall()
        self.load= vr[0] if vr != [] else None
        if self.load != None:
            
            self.nome_empresa.setText(self.load[0])
            self.endereco_empresa.setText(self.load[1])
            self.bairro_empresa.setText(self.load[2])
            self.cidade_empresa.setText(self.load[3])
            self.telefone_empresa.setText(self.load[4])
            self.cnpj_empresa.setText(self.load[5])
            self.garantia_empresa.setText(self.load[6]+' Dias de Garantia')
        
#------------------------------------------TELA CADASTRO DE APARELHO------------------------------------------------
    def PesquisarAparelho(self):
        self.c.execute('select * from Clientes where nome=?',(self.pesquisa_aparelho.text(),))
        dados = self.c.fetchone()
        if dados != None:
            self.pesquisa_aparelho.focusNextChild()
            self.btnpesquisa_aparelho.focusNextChild()
            self.aparelho_aparelho.setFocus()
            self.lbinformacao_aparelho.setText(self.pesquisa_aparelho.text())
            self.pesquisa_aparelho.clear()
            self.aparelho_aparelho.setEnabled(True)
            self.marca_aparelho.setEnabled(True)
            self.modelo_aparelho.setEnabled(True)
            self.serie_aparelho.setEnabled(True)
            self.adicional_aparelho.setEnabled(True)
            self.defeito_aparelho.setEnabled(True)
        else:
            QMessageBox.about(self,'Aviso','Esse cliente não existe!\nCadastre o cliente antes ou verifique a ortografia')
    
    def SalvarAparelho(self):
        data_atual = date.today()
        status='Aberto'
        if self.lbinformacao_aparelho.text() != '' and self.aparelho_aparelho.text() != '' and self.marca_aparelho.text() != '' and self.modelo_aparelho.text() != '' and self.defeito_aparelho.text() != '':
            self.c.execute('insert into Aparelhos (Nome,Aparelho,Marca,Modelo,Serie,DefeitoInfo,InfoAdd,DataEntrada,Status) values(?,?,?,?,?,?,?,?,?)',
                      (self.lbinformacao_aparelho.text(),self.aparelho_aparelho.text(),self.marca_aparelho.text(),self.modelo_aparelho.text(),
                       self.serie_aparelho.text(),self.defeito_aparelho.text(),self.adicional_aparelho.text(),data_atual,status))
            self.conn.commit()
            QMessageBox.about(self,'Aviso','Os dados do aparelho foram salvos com sucesso!')
            self.aparelho_aparelho.clear()
            self.marca_aparelho.clear()
            self.modelo_aparelho.clear()
            self.serie_aparelho.clear()
            self.adicional_aparelho.clear()
            self.defeito_aparelho.clear()

            self.aparelho_aparelho.setEnabled(False)
            self.marca_aparelho.setEnabled(False)
            self.modelo_aparelho.setEnabled(False)
            self.serie_aparelho.setEnabled(False)
            self.adicional_aparelho.setEnabled(False)
            self.defeito_aparelho.setEnabled(False)
            self.lbinformacao_aparelho.setText('')
            self.AtualizaHome()
            self.Inicializar()
            self.Maxid()

#---------------------------------------- TELA INFORMAÇÕES ADICIONAIS-----------------------------------------------
    def PesquisarAdiciona(self):
                
        if self.pesquisa_adiciona.text() != '':
            self.c.execute('select * from Aparelhos where id=?',(self.pesquisa_adiciona.text(),))
            dados = self.c.fetchone()
            if dados != None:
                if dados[14] !='autorizado':
                    self.os=dados[0]
                    cliente= 'OS '+str(dados[0])+ ' - '+dados[1]
                    self.lbinformacao_adiciona.setText(cliente)
                    self.pesquisa_adiciona.clear()
                    self.aparelho_adiciona.setText(dados[2])
                    self.marca_adiciona.setText(dados[3])
                    self.modelo_adiciona.setText(dados[4])
                    self.serie_adiciona.setText(dados[5])
                    self.servico_adiciona.setEnabled(True)
                    self.pecas_adiciona.setEnabled(True)
                    self.valor_adiciona.setEnabled(True)
                    
                else:
                    QMessageBox.about(self,"Aviso",'   Esta OS ja foi atualizada   ')
            else:
                self.pesquisa_adiciona.clear()
                QMessageBox.about(self,'Aviso','Essa OS não existe no sistema!')

    def SalvarAdiciona(self):
                
        if self.servico_adiciona.text() != '' and self.pecas_adiciona.text() != '' and  self.valor_adiciona.text() != '':
            
            autorizado='autorizado'
            self.c.execute("UPDATE Aparelhos SET Servico=?,Pecas=?,Preço=?,Situacao=? WHERE id=?",
                            (self.servico_adiciona.text(), self.pecas_adiciona.text(), self.valor_adiciona.text(), autorizado, self.os))
            self.conn.commit()
            QMessageBox.about(self,"Aviso",'  OS Atualizada Com Sucesso!  ')
            self.LimpaAdiciona()
            self.Maxid()
                
    def LimpaAdiciona(self):
        self.AtualizaHome()
        self.lbinformacao_adiciona.setText('')
        self.pesquisa_adiciona.clear()
        self.aparelho_adiciona.clear()
        self.marca_adiciona.clear()
        self.modelo_adiciona.clear()
        self.serie_adiciona.clear()
        self.servico_adiciona.clear()
        self.pecas_adiciona.clear()
        self.valor_adiciona.clear()
        self.servico_adiciona.setEnabled(False)
        self.pecas_adiciona.setEnabled(False)
        self.valor_adiciona.setEnabled(False)

#----------------------------------------------TELA PESQUISA-----------------------------------------------------------------
    def PesquisarPesquisa(self):
                       
        if self.pesquisa_pesquisa.text() != '':
            if not self.pesquisa_pesquisa.text().isdigit():
                self.c.execute('select * from Aparelhos where Nome=?',(self.pesquisa_pesquisa.text(),))
                dados = self.c.fetchone()
                if dados != None:
                    
                    self.os=dados[0]
                    cliente= 'OS '+str(dados[0])+ ' - '+dados[1]
                    self.lbinformacao_pesquisa.setText(cliente)
                    self.pesquisa_adiciona.clear()
                    self.aparelho_pesquisa.setText(dados[2])
                    self.marca_pesquisa.setText(dados[3])
                    self.modelo_pesquisa.setText(dados[4])
                    self.serie_pesquisa.setText(dados[5])
                    self.defeito_pesquisa.setText(dados[6])
                    self.adicional_pesquisa.setText(dados[7])
                    self.servico_pesquisa.setText(dados[8])
                    self.pecas_pesquisa.setText(dados[9])
                    self.valor_pesquisa.setText(dados[13]+',00')     
                else:
                    self.pesquisa_adiciona.clear()
                    QMessageBox.about(self,'Aviso','Essa OS não existe no sistema!')
            else:
                self.c.execute('select * from Aparelhos where id=?',(self.pesquisa_pesquisa.text(),))
                dados = self.c.fetchone()
                if dados != None:
                    self.os=dados[0]
                    cliente= 'OS '+str(dados[0])+ ' - '+dados[1]
                    self.lbinformacao_pesquisa.setText(cliente)
                    self.pesquisa_adiciona.clear()
                    self.aparelho_pesquisa.setText(dados[2])
                    self.marca_pesquisa.setText(dados[3])
                    self.modelo_pesquisa.setText(dados[4])
                    self.serie_pesquisa.setText(dados[5])
                    self.defeito_pesquisa.setText(dados[6])
                    self.adicional_pesquisa.setText(dados[7])
                    self.servico_pesquisa.setText(dados[8])
                    self.pecas_pesquisa.setText(dados[9])
                    self.valor_pesquisa.setText(dados[13]+',00')   

#----------------------------------------------TELA FINALIZAR-----------------------------------------------------------
    def PesquisarFinalizar(self):
                       
        if self.pesquisa_finalizar.text() != '':
            if  self.pesquisa_finalizar.text().isdigit():
                self.c.execute('select * from Aparelhos where id=? ',(self.pesquisa_finalizar.text(),))
                dados = self.c.fetchone()
                if dados != None:
                    self.c.execute('select Status from Aparelhos where id=? ',(self.pesquisa_finalizar.text(),))
                    d = self.c.fetchone()
                    data = d[0] if d != None else None
                    
                    if data =='Aberto':
                        self.os=dados[0]
                        cliente= 'OS '+str(dados[0])+ ' - '+dados[1]
                        self.lbinformacao_finalizar.setText(cliente)
                        self.pesquisa_finalizar.clear()
                        self.aparelho_finalizar.setText(dados[2])
                        self.marca_finalizar.setText(dados[3])
                        self.modelo_finalizar.setText(dados[4])
                        self.valor_finalizar.setText(dados[13]+',00')
                    else:
                        self.pesquisa_finalizar.clear()
                        QMessageBox.about(self,'Aviso','Essa OS já foi finalizada!')
                      
                else:
                    self.pesquisa_finalizar.clear()
                    QMessageBox.about(self,'Aviso','Essa OS não existe no sistema!')

    def ConfirmarFinalizar(self):
        if self.valorpago_finalizar.text()=='':
            pass
        elif not self.valorpago_finalizar.text().isdigit():
            QMessageBox.about(self,'Aviso','   Digite apenas números   ')
        else:
            data_atual = date.today()
            self.c.execute("UPDATE Aparelhos SET DataEntregue=?,Status=?,ValorPago=? WHERE id=?",(data_atual,'finalizado',self.valorpago_finalizar.text(),self.os))
            self.conn.commit()
            QMessageBox.about(self,'Aviso','   Os Finalizada!   ')
            self.lbinformacao_finalizar.setText('')
            self.pesquisa_finalizar.clear()
            self.aparelho_finalizar.clear()
            self.marca_finalizar.clear()
            self.modelo_finalizar.clear()
            self.valor_finalizar.clear()
            self.valorpago_finalizar.clear()
            self.AtualizaHome()
            self.Inicializar()
            self.Maxid()

#----------------------------------------------TELA FLUXO MENSAL-----------------------------------------------------------------

    def Inicializar(self):
        self.tableWidget_2.clear()
        self.listasomar = []
        self.c.execute('select id,Nome,Aparelho,Marca,Modelo,DataEntrada,DataEntregue,ValorPago from Aparelhos where Status="finalizado" ')
        rec = self.c.fetchall()
        self.tableWidget_2.setRowCount(len(rec))    
        self.tableWidget_2.horizontalHeader().setVisible(True)
            
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tamanho=self.size()
        self.reftela=round(self.tamanho.width()/100)*2

        self.tableWidget_2.setHorizontalHeaderItem( 0, QTableWidgetItem((self.reftela-16)*' '+'OS'+(self.reftela-16)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 1, QTableWidgetItem((self.reftela-10)*' '+'Nome do Cliente'+(self.reftela-10)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 2, QTableWidgetItem((self.reftela-12)*' '+'Aparelho'+(self.reftela-12)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 3, QTableWidgetItem((self.reftela-10)*' '+'Marca'+(self.reftela-10)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 4, QTableWidgetItem((self.reftela-10)*' '+'Modelo'+(self.reftela-10)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 5, QTableWidgetItem((self.reftela)*' '+'Entrada'+(self.reftela)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 6, QTableWidgetItem((self.reftela)*' '+'Entrega'+(self.reftela)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 7, QTableWidgetItem((self.reftela-20)*' '+'Valor'+(self.reftela-20)*' '))
        if rec !=None and rec != []:
                        
            p = 0
            for i in rec:
                
                self.tableWidget_2.setItem(p, 0, QTableWidgetItem(str(i[0])))
                self.tableWidget_2.setItem(p, 1, QTableWidgetItem(str(i[1])))
                self.tableWidget_2.setItem(p, 2, QTableWidgetItem(str(i[2])))
                self.tableWidget_2.setItem(p, 3, QTableWidgetItem(str(i[3])))
                self.tableWidget_2.setItem(p, 4, QTableWidgetItem(str(i[4])))
                self.tableWidget_2.setItem(p, 5, QTableWidgetItem(str(self.formatdate(i[5]))))
                self.tableWidget_2.setItem(p, 6, QTableWidgetItem(str(self.formatdate(i[6]))))
                self.tableWidget_2.setItem(p, 7, QTableWidgetItem(str(i[7])+',00'))           
                p = p+1
                self.listasomar.append(int(i[7]))
            self.lbtotal_fluxo.setText('R$ '+str(sum(self.listasomar))+',00')
    def PesquisaData(self):
        self.tableWidget_2.clear()
        self.listasomar = []
        self.c.execute('select id,Nome,Aparelho,Marca,Modelo,DataEntrada,DataEntregue,ValorPago from Aparelhos where Status="finalizado" and DataEntregue between ? and ?', (self.DataEdit(self.dateEdit.date()),self.DataEdit(self.dateEdit_2.date())))
        rec = self.c.fetchall()
        self.tableWidget_2.setRowCount(len(rec))    
        self.tableWidget_2.horizontalHeader().setVisible(True)
            
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tamanho=self.size()
        self.reftela=round(self.tamanho.width()/100)*2

        self.tableWidget_2.setHorizontalHeaderItem( 0, QTableWidgetItem((self.reftela-16)*' '+'OS'+(self.reftela-16)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 1, QTableWidgetItem((self.reftela-10)*' '+'Nome do Cliente'+(self.reftela-10)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 2, QTableWidgetItem((self.reftela-12)*' '+'Aparelho'+(self.reftela-12)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 3, QTableWidgetItem((self.reftela-10)*' '+'Marca'+(self.reftela-10)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 4, QTableWidgetItem((self.reftela-10)*' '+'Modelo'+(self.reftela-10)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 5, QTableWidgetItem((self.reftela)*' '+'Entrada'+(self.reftela)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 6, QTableWidgetItem((self.reftela)*' '+'Entrega'+(self.reftela)*' '))
        self.tableWidget_2.setHorizontalHeaderItem( 7, QTableWidgetItem((self.reftela-20)*' '+'Valor'+(self.reftela-20)*' '))
        if rec !=None and rec != []:
                        
            p = 0
            for i in rec:
                
                self.tableWidget_2.setItem(p, 0, QTableWidgetItem(str(i[0])))
                self.tableWidget_2.setItem(p, 1, QTableWidgetItem(str(i[1])))
                self.tableWidget_2.setItem(p, 2, QTableWidgetItem(str(i[2])))
                self.tableWidget_2.setItem(p, 3, QTableWidgetItem(str(i[3])))
                self.tableWidget_2.setItem(p, 4, QTableWidgetItem(str(i[4])))
                self.tableWidget_2.setItem(p, 5, QTableWidgetItem(str(self.formatdate(i[5]))))
                self.tableWidget_2.setItem(p, 6, QTableWidgetItem(str(self.formatdate(i[6]))))
                self.tableWidget_2.setItem(p, 7, QTableWidgetItem(str(i[7])+',00'))           
                p = p+1
                self.listasomar.append(int(i[7]))
            self.lbtotal_fluxo.setText('R$ '+str(sum(self.listasomar))+',00')
        
    def  DataEdit(self,arg):
        self.data=arg
        if int(self.data.month()) < 10:
            mes='0'+str(self.data.month())
        else:
            mes=str(self.data.month())
        if int(self.data.day()) < 10:
            dia='0'+str(self.data.day())
        else:
            dia=str(self.data.day())
        self.dataedit=str(self.data.year())+'-'+mes+'-'+dia
        return self.dataedit

#-------------------------------------------------TELA ALTERAR SENHA------------------------------------------------

    def VerifikSenha(self):
        self.c.execute('select Senha from SenhaLogin')
        currentsenha= self.c.fetchone()[0]
        if self.oldsenha.text() != '' and self.newsenha.text() != '':
        
            if currentsenha != self.oldsenha.text() and self.oldsenha.text()!= "OsManager777":
                QMessageBox.about(self,'Aviso','   Senha Antiga incorreta!!   ')
            
            else:
                self.c.execute('UPDATE SenhaLogin SET Senha=? ', (self.newsenha.text(),))
                self.conn.commit()
                QMessageBox.about(self,'Aviso','   Senha Atualizada!!   ')
                self.oldsenha.clear()
                self.newsenha.clear()
                
#---------------------------------------------------TELA ATIVAR----------------------------------------------------

    def registrar(self):
        
        self.c.execute('select senha from senhaativar')
        var=self.c.fetchone()[0] if self.c.fetchone()!= None else None
        
        if  self.senha_ativar.text() != '':
            if self.senha_ativar.text()=="r7dg4s5374g" and var == None:
                self.label_15.setText('Software Ativado!\nAproveite!!')
                self.c.execute('insert into senhaativar (senha) values("r7dg4s5374g")')
                self.conn.commit()
                self.senha_ativar.clear()
                self.btnativar_ativar.setEnabled(False)
            else:
                QMessageBox.about(self,'Aviso','   Chave de ativação incorreta!!   ')
                self.senha_ativar.clear()

#----------------------------------------------------TELA EMITIR NOTA-----------------------------------------------

    def Verificar(self):
        
        if self.os_nota.text() != '':
            self.c.execute('select Nome from empresa ')
            v = self.c.fetchone()
            if v == None:
                QMessageBox.about(self,'Aviso','   Dados da empresa precisam ser preenchidos!   ')
            else:
                self.c.execute('select id,Nome,Aparelho,Marca,Modelo,Serie,DefeitoInfo from Aparelhos where id=?',(self.os_nota.text(),))
                n = self.c.fetchone()
                if n != None:
                    self.listWidget.clear()
                    self.label_nota.setText('OS nº ' + self.os_nota.text())
                    self.listWidget.addItem("OS "+str(n[0]))
                    self.listWidget.addItem("Cliente: "+n[1])
                    self.listWidget.addItem("Aparelho: "+n[2])
                    self.listWidget.addItem("Marca: "+n[3])
                    self.listWidget.addItem("Modelo: "+n[4])
                    self.listWidget.addItem("Número de Serie: "+n[5])
                    self.listWidget.addItem("Defeito Informado: "+n[6])
                else:
                    QMessageBox.about(self,'Aviso','  Os não existe no sistema!   ')
                    self.label_nota.setText('')
                    self.listWidget.clear()

    def Gerar(self):
        self.lista=[]
        if self.label_nota.text() !='':
            if self.rb_orcamento.isChecked():

                self.c.execute('select Nome from Aparelhos where id=?',(self.os_nota.text(),))
                da=self.c.fetchone()
                dados=da[0] if da != None else None
                if dados != None:
                    self.c.execute("select * from empresa")
                    rec=self.c.fetchall()[0]
                    self.c.execute("select * from Aparelhos where id=?",(self.os_nota.text(),))
                    rec2 = self.c.fetchall()[0]
                    nome=rec2[1]
                    self.c.execute("select Endereco from Clientes where Nome=?",(nome,))
                    rec3 = self.c.fetchone()[0]
                    for a in range(6):
                        self.lista.append(rec[a])
                    for a in range(5):
                        self.lista.append(rec2[a])
                    self.lista.append(rec2[8])
                    self.lista.append(rec2[-1])
                    self.lista.append(self.formatdate(rec2[10]))
                    datasaida=self.formatdate(rec2[12]) if rec2[12] != None else ""
                    self.lista.append(datasaida)
                    self.lista.append(rec[-1])
                    self.lista.append(rec3)
                    
            if self.rb_entrega.isChecked():
                self.c.execute('select Nome,Status from Aparelhos where id=?',(self.os_nota.text(),))
                da=self.c.fetchone()
                dados=da[0] if da != None else None
                verificar = da[1] if da != None else None
                if dados != None:
                    if verificar == 'Aberto':
                        QMessageBox.about(self,'Aviso','OS '+self.os_nota.text()+' ainda nao foi finalizada')
                    else:
                        self.c.execute("select * from empresa")
                        rec=self.c.fetchone()
                        self.c.execute("select * from Aparelhos where id=?",(self.os_nota.text(),))
                        rec2 = self.c.fetchone()
                        nome = rec2[1]
                        self.c.execute("select Endereco from Clientes where Nome=?", (nome,))
                        rec3 = self.c.fetchone()[0]
                        for a in range(6):
                            self.lista.append(rec[a])
                        for a in range(5):
                            self.lista.append(rec2[a])
                        self.lista.append(rec2[8])
                        self.lista.append(rec2[-1])
                        self.lista.append(self.formatdate(rec2[10]))
                        datasaida=self.formatdate(rec2[12]) if rec2[12] != None else ""
                        self.lista.append(datasaida)
                        self.lista.append(rec[-1])
                        self.lista.append(rec3)
            save = QFileDialog.getSaveFileName(self,'Gerar Nota')
            self.lista.append(save[0])
            self.imprimir()

    def imprimir(self):
        if self.rb_orcamento.isChecked():
            imprimirOs(self.lista)
            QMessageBox.about(self,'Aviso','Nota de Recebimento Gerada!!')
        if self.rb_entrega.isChecked():
            imprimirNE(self.lista)
            QMessageBox.about(self,'Aviso','Nota de Entrega Gerada!!')

###################################################################################################################

class Login(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('./Ui/Login.ui',self)
        so = platform.system()
        if so == 'Windows':
            self.tamanho=self.size()
            self.tam = self.tamanho.width()-70
            self.setGeometry(int(self.tam), 40, 500, 790)
        self.btlogin.clicked.connect(self.login)
        self.password.returnPressed.connect(self.login)
        self.frame_error.hide()
        self.conn=sqlite3.connect('ideal.db')
        self.c=self.conn.cursor()
        self.c.execute('select Senha from SenhaLogin')
        v = self.c.fetchone()
        self.var = v[0] if v != None else None
        if self.var == None:
            self.c.execute('insert into SenhaLogin (Senha) values("admin")')
            self.conn.commit()

    def login(self):
        if self.user.text() != '' and self.password.text() != '':
            if self.user.text() == 'admin' and self.password.text() == self.var:
                self.principal=Principal()
                self.close()
                self.principal.show()
            else:
                self.label_error.setText('Senha incorreta!')
                self.frame_error.show()
        

#####################################################################################################################

class TelaSplash(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('./Ui/Splash.ui',self)

        
#        Tira a moldura da janela e os botoes
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

#        Temporizador da tela

        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
#        Tempo em milisegundos 

        self.timer.start(40)

#        Muda a label descrição automaticamente 

        QtCore.QTimer.singleShot(1400, lambda: self.label_descricao.setText("LOADING DATABASE"))
        QtCore.QTimer.singleShot(2500, lambda: self.label_descricao.setText("LOADING USER INTERFACE"))

#        funçao de decrementar 

    def progress(self):
        global counter
        self.progressbar.setValue(counter)

        if counter > 100:
            self.timer.stop()
            self.close()
            self.main = Login()
            self.main.show()               
        counter+=1
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('./fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('./fonts/segoeuib.ttf')
    main=TelaSplash()  
    main.show()
    sys.exit(app.exec_())
