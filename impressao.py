import time
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import date
import os
arquivo =''
Data=str(date.today())
def formatdate(arg):
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
listaex=['empresa','rua','bairro','cidade','tel','cpf','Os','cliente','aparelho','marca','modelo','servico','valor','dataentrada','datasaida','60','endereco','path']
def imprimirNE(args):
        global arquivo
        path=args[17]
        enderecocli=args[16]
        garantia=args[15]
        cliente=args[7]
        aparelho=args[8]
        marca=args[9]
        modelo=args[10]
        servico=args[11]
        valor=args[12]+",00"
        dataentrada=args[13]
        datasaida=args[14]
        rua = args[1]
        bairro= args[2]
        tel= args[4]
        cidade=args[3]
        endereco=rua+' - '+bairro
        lugar= cidade+' - '+'tel: '+tel
        Os=args[6]
        cpf= args[5]
        CPF="Cpf/Cnpj: "+cpf
        Empresa = args[0]
        aster='_'
        doc = SimpleDocTemplate(path+".pdf",pagesize=A4)
        arquivo=path+".pdf"
        Story=[]

        styles=getSampleStyleSheet()

        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

        ptext = '<font size=15>%s</font>' % aster*52
        Story.append(Paragraph(ptext, styles["Center"]))
      

        Story.append(Spacer(1, 5))
        ptext = '<font size=32>%s</font>' % Empresa
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1, 30))
        
        # Create return address
        ptext = '<font size=11 fontname="Helvetica-Oblique">%s</font>' % endereco
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1,2))

        ptext = '<font size=11 fontname="Helvetica-Oblique">%s</font>' % lugar
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1,2))

        ptext = '<font size=11 fontname="Helvetica-Oblique">%s</font>' % CPF
        Story.append(Paragraph(ptext, styles["Center"]))

        ptext = '<font size=15>%s</font>' % aster*52
        Story.append(Paragraph(ptext, styles["Center"]))
        #Corpo do documento
        Story.append(Spacer(1, 20))
        ptext = '<font size=18 fontname="Helvetica-Bold">Nota de Entrega</font>'
        Story.append(Paragraph(ptext, styles["Center"]))
        
        Story.append(Spacer(1, 32))
        
        ptext = '<font size=12 fontname="Helvetica">Número da OS : %s</font>' %Os
        Story.append(Paragraph(ptext, styles["Right"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=12>Nome do Cliente : %s</font>' %cliente
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=12>Endereço : %s</font>' %enderecocli
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=12>Aparelho: %s</font>' %aparelho
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=12>Marca: %s</font>' %marca
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=12>Modelo: %s</font>' %modelo
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=12>Serviço Feito: %s</font>' %servico
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 17))

        ptext = '<font size=12>Valor: %s</font>' %valor
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=12>Entrada do Aparelho: %s</font>' %dataentrada
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=12>Saída do Aparelho: %s</font>' %datasaida
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 7))

        ptext = '<font size=15>%s</font>' % aster*52
        Story.append(Paragraph(ptext, styles["Center"]))

        Story.append(Spacer(1, 18))
        ptext = '<font size=13 fontname="Helvetica-Bold">Termos da Garantia</font>' 
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1, 18))

        ptext = '<font size=11 fontname="Helvetica-Oblique">1. Qualquer serviço de ordem técnica, não autorizado pela %s implicará na perda da garantia.</font>'%Empresa
        Story.append(Paragraph(ptext, styles["Normal"]))


        ptext = '<font size=11 fontname="Helvetica-Oblique">2. Garantia de %s dias, a partir da data de entrega do aparelho</font>' %garantia
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 7))

        ptext = '<font size=15>%s</font>' % aster*52
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1, 40))


        ptext = '<font size=13 fontname="Helvetica">Emitido em:  %s</font>' %formatdate(Data)
        Story.append(Paragraph(ptext, styles["Right"]))
        doc.build(Story)

def imprimirOs(args):
        global arquivo
        path=args[17]
        enderecocli=args[16]
        garantia=args[15]
        cliente=args[7]
        aparelho=args[8]
        marca=args[9]
        modelo=args[10]
        servico=args[11]
        valor=args[12]
        dataentrada=args[13]
        datasaida=args[14]
        rua = args[1]
        bairro= args[2]
        tel= args[4]
        cidade=args[3]
        endereco=rua+' - '+bairro
        lugar= cidade+' - '+'tel: '+tel
        Os=args[6]
        cpf= args[5]
        CPF="Cpf/Cnpj: "+cpf
        Empresa = args[0]
        aster='_'
        doc = SimpleDocTemplate(path+".pdf",pagesize=A4)
        arquivo=path+".pdf"
        Story=[]

        styles=getSampleStyleSheet()

        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

        ptext = '<font size=15>%s</font>' % aster*52
        Story.append(Paragraph(ptext, styles["Center"]))
      

        Story.append(Spacer(1, 5))
        ptext = '<font size=35>%s</font>' % Empresa
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1, 30))
        
        # Create return address
        ptext = '<font size=11 fontname="Helvetica-Oblique">%s</font>' % endereco
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1,2))

        ptext = '<font size=11 fontname="Helvetica-Oblique">%s</font>' % lugar
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1,2))

        ptext = '<font size=11 fontname="Helvetica-Oblique">%s</font>' % CPF
        Story.append(Paragraph(ptext, styles["Center"]))

        ptext = '<font size=15>%s</font>' % aster*52
        Story.append(Paragraph(ptext, styles["Center"]))
        #Corpo do documento
        Story.append(Spacer(1, 20))
        ptext = '<font size=18 fontname="Helvetica-Bold">Orçamento</font>'
        Story.append(Paragraph(ptext, styles["Center"]))
        
        Story.append(Spacer(1, 40))
        
        ptext = '<font size=15 fontname="Helvetica">Número da OS : %s</font>' %Os
        Story.append(Paragraph(ptext, styles["Right"]))
        Story.append(Spacer(1, 30))

        ptext = '<font size=13>Nome do Cliente : %s</font>' %cliente
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 25))

        ptext = '<font size=13>Endereço : %s</font>' %enderecocli
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 25))

        ptext = '<font size=13>Aparelho: %s</font>' %aparelho
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 25))

        ptext = '<font size=13>Marca: %s</font>' %marca
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 25))

        ptext = '<font size=13>Modelo: %s</font>' %modelo
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 25))

        ptext = '<font size=13>Entrada do Aparelho: %s</font>' %dataentrada
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 30))

        ptext = '<font size=15>%s</font>' % aster*52
        Story.append(Paragraph(ptext, styles["Center"]))

        Story.append(Spacer(1, 25))
        ptext = '<font size=13 fontname="Helvetica-Bold">Termos Legais</font>' 
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1, 20))

        ptext = '<font size=11 fontname="Helvetica-Oblique">1 . Aparelhos que nao forem retirados em até 90 Dias, Receberão reajustes de preços </font>'
        Story.append(Paragraph(ptext, styles["Normal"]))


        ptext = '<font size=11 fontname="Helvetica-Oblique">2 . Aparelhos que nao forem retirados em até 180 Dias, serão vendidos pra cobrir despezas</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 8))

        ptext = '<font size=15>%s</font>' % aster*52
        Story.append(Paragraph(ptext, styles["Center"]))
        Story.append(Spacer(1, 70))


        ptext = '<font size=13 fontname="Helvetica">Emitido em:  %s</font>' %formatdate(Data)
        Story.append(Paragraph(ptext, styles["Right"]))
        doc.build(Story)
        



