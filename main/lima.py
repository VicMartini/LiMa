#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import *
from qrtools import QR
from qrcode import *
from datetime import *
from PyQt4.uic import *
import codecs
import time 
import sys
import os
import re

reload(sys)
sys.setdefaultencoding("utf-8")
utf8=codecs.getencoder('UTF8')
status = 0
decoded = ""
archlibros = './data/libros.ini'
archgeneros = './data/generos.txt'
opciones = ["titulo","autor","genero","estado","nprestamos","clftotal","cflnula","prestamoid"]
titulo = ""
genero = ""
autor = ""
txt = ""
generostr = ["genero"] 
generos = []
datos = []
completerList = []
configs = []
archconfigs = 'conf.ini'
archtransacciones ='./data/transacciones.ini'
validacion = False
editando = False
opmetodos = ['QR' , 'Texto']
parser = RawConfigParser()
parser.read(archconfigs)
metodo = int(parser.get('metodo','busqueda'))

class Form1(QtGui.QWidget):
    def __init__(self, parent=None, *args ):

        QtGui.QWidget.__init__(self,parent, *args)
        locale = unicode(QtCore.QLocale.system().name())
        self.ui=loadUi("./GUI/limaui.ui",self)
        self.setWindowTitle("Open LiMa - Home")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        centrar(self)
        self.close()
        global status ,modulo0, modulo1 , modulo2 ,modulo3,modulo4,modulo5,modulo6,modulo7, web 
        modulo0 = self
        modulo1 = Form2()
        modulo2 = Form3()
        modulo3 = Form4()
        modulo4 = Form5()
        modulo5 = CambiarPassword()
        modulo6 = Form6()
        modulo7 = Form7()
        if validacion:
            self.show()
        self.options_btn.setIcon(QtGui.QIcon("./images/optionsico.png"))
        self.setWindowIcon(QtGui.QIcon('./images/limaico.png'))
        for y in range(len(generos)):

            modulo2.genero_cb.addItem(generos[y])


    def infolibro(self):
        
        global status, editando
        editando = False
        centrar(modulo1)
        ajustart(modulo1)
        modulo3.atrasados()
        if metodo == 0:
            
            while status == 0:
            
                decodificar()
            
                if status == 0:
            
                    errordecodificar()

            if status == 1: 

                self.info()
        
        elif metodo == 1:
            
            modulo3.show()

        status = 0

    def info(self):
        global estado
        modulo4.lvcolor() 
        modulo1.web2.hide()
        modulo1.web.show()
        parserread()
        modulo1.his = False
        if float(total) != 0:
            calificacion = str('{: .2f}'.format(float(total)/(int(nprestamos)-int(cflnula))))+"/5.00" 
            if (estado == 'Prestado') or (estado == 'Atrasado'):
                calificacion = str('{: .2f}'.format(float(total)/(int(nprestamos)-(1+int(cflnula)))))+"/5.00" 
        else:
            calificacion = 'No disponible'

        self.stylesheet = 'body,td,tr { color: '+modulo4.ltrcolor+'; font-family: Ubuntu;font-size:85%;background-color: '+modulo4.fndcolor+'} table , th , td ,tr \
                { border: 1px #dedede; padding: 10px;background-color: '+modulo4.tblcolor+';color: '+modulo4.ltrcolort+';border-radius: 17px;} table {border-collapse: collapse;width: 100%;}</style>'
        informacion = '<head><style type="text/css">'+self.stylesheet+'</style></head><h5>Informacion sobre :</h5><h3>'+titulo+'</h3><body><table border="1" >'\
        +"<tr><td>Autor </td><td>"+autor+"</td></tr><tr>"+"<td>Genero  </td><td>"+genero+\
        "</td></tr><tr><td>Estado </td><td>"+estado+"</td></tr><tr><td>Calificacion media </td><td>"+calificacion+"</td></tr><td>Veces prestado </td><td>"+nprestamos+"</td></tr>"
        modulo1.web.setHtml(informacion+'</body>')
        if (estado == 'Prestado') or (estado == 'Atrasado'):
            modulo1.web.setHtml(informacion+"<tr><td>Usuario actual </td><td>"+nombre+"</td></tr>"\
            +"<tr><td>Fecha de prestamo </td><td>"+fechaprestamo+"</td></tr><tr><td>Fecha de entrega maxima </td><td>"+fechaentrega+"</td></tr>")
        modulo1.show()    
    
    def nuevolibro(self):
        global editando
        editando = False
        ajustart(modulo2)  
        centrar(modulo2)  
        modulo2.estado_cb.hide()
        modulo2.estadolabel.hide()       
        modulo2.show()
        readgeneros()
        modulo2.genero_cb.setCurrentIndex(0)
        modulo2.imprimir_bt.hide()

    def prestamo(self):
        
        global status
        while status == 0:
            
            decodificar()
            
            if status == 0:
            
                errordecodificar()

        if status == 1: 

            parserread()
            if estado != ('Prestado' or 'En reparacion' or 'Perdido' or 'Atrasado' ):          
                modulo6.show()
                modulo6.titulolabel.setText('Prestando : '+titulo)
                modulo6.limpiar()
            else:
                QtGui.QMessageBox.critical(self, 'Error',
                "Libro no disponible", QtGui.QMessageBox.Ok)
        status = 0

    def quitarlibro(self):  #Editar Información
        

        global status, editando 
        modulo3.atrasados()
        centrar(modulo2)
        ajustart(modulo2)
        editando = True
        modulo2.estado_cb.show()
        modulo2.estadolabel.show()        
        if metodo == 0:
            
            while status == 0:
            
                decodificar()
            
                if status == 0:
            
                    errordecodificar()

            if status == 1: 

                self.editar()
        
        elif metodo == 1:
            
            modulo3.show()

        status = 0

    def editar(self):

        centrar(modulo2)
        ajustart(modulo2)
        parserread()
        modulo2.imprimir_bt.show()
        modulo2.previsualizar_btn.hide()
        modulo2.titulo_txt.setText(titulo)
        modulo2.autor_txt.setText(autor)
        a = modulo2.genero_cb.findText(genero)
        b = modulo2.estado_cb.findText(estado)
        modulo2.setWindowTitle("Open LiMa - Editar")
        if a == -1:
            modulo2.genero_cb.addItem(genero)
            a = modulo2.genero_cb.findText(genero)
        if b == -1:
            modulo2.estado_cb.clear()
            modulo2.estado_cb.addItem(estado)
            b = modulo2.estado_cb.findText(estado)
        modulo2.genero_cb.setCurrentIndex(a)
        modulo2.estado_cb.setCurrentIndex(b)
        codificar(decoded,modulo2)    
        modulo2.show()
    
    def recibir(self):
        
        global status
        modulo7._1.setChecked(True)
        while status == 0:
            
            decodificar()
            
            if status == 0:
            
                errordecodificar()

        if status == 1: 

            parserread()
            if (estado == 'Prestado') or (estado == 'Atrasado') :            
                modulo7.titulolabel.setText('Devolviendo : '+titulo)
                modulo7.show()
            else:
                QtGui.QMessageBox.critical(self, 'Error',
                "Libro no prestado", QtGui.QMessageBox.Ok)
        status = 0

    
    def opciones(self):
       
        modulo4.show()
 
class Form2(QtGui.QDialog):
    
    def __init__(self, parent=None):
    
        QtGui.QDialog.__init__(self, parent)
        self.ui=loadUi("./GUI/limaui_m1.ui",self)
        self.setWindowTitle("Open LiMa - Informacion")
        self.web2 = QWebView(self)
        self.web2.setObjectName("web2")
        self.horizontall3.addWidget(self.web2)
        self.web = QWebView(self)
        self.web.setObjectName("web")
        self.horizontall3.addWidget(self.web)

    def historial(self):
        if int(nprestamos) != 0:
            global status
            self.his = True
            parser = RawConfigParser()
            parser.read(archtransacciones)
            parserread()
            sections = parser.sections()
            info_o = '<style type="text/css">'+modulo0.stylesheet+'</style></head><h2>Lista de prestamos: </h2>'
            count = 0
            for x in range(len(sections)):
                titulodb = parser.get(str(x),'titulo')
                if titulo == titulodb:
                    count += 1
                    fechaprestamo =  parser.get(str(x),'fechaprestamo')
                    fechaentrega =  parser.get(str(x),'fechaentrega')
                    vfechadeentrega = parser.get(str(x),'vfechadeentrega')
                    usuario = parser.get(str(x),'nombre')
                    info_n = "<h5>Prestamo "+str(count)+":</h5><br><table border><tr><td>Usuario </td><td>"+usuario+\
                    "</td></tr><tr><td>Fecha de prestamo </td><td>"+fechaprestamo+"</td></tr><tr><td>Fecha de entrega maxima \
                    </td><td>"+fechaentrega+"</td></tr><tr><td>Fecha de entrega </td><td>"+vfechadeentrega+"</td></tr></table><br>"
                    info_o = info_o+info_n
                self.web.hide()
                self.web2.show()
                self.web2.setHtml(info_o)
        else:
            QtGui.QMessageBox.critical(self, 'Error',
            "No hubo prestamos", QtGui.QMessageBox.Ok)


    def _close(self):
        
        if self.his:
            self.web2.hide()
            self.web.show()
            self.his = False
        else:  
            pass
            self.close()


class Form3(QtGui.QDialog):
    
    def __init__(self, parent=None):
   
        QtGui.QDialog.__init__(self, parent)
        self.ui=loadUi("./GUI/limaui_m2.ui",self)
        self.setWindowTitle("Open LiMa - Nuevo Libro")
        self.limpiar()        
        global imprimir, error
        imprimir = False
        error = False
        self.count = 0
        readgeneros()

    def nuevogenero(self):

        global generos
        text,ok  = QtGui.QInputDialog.getText(self, '', 
        'Nuevo genero :')
        if (text != ""):
            modulo2.genero_cb.addItem(text)
            generos.append(str(text))

        elif ok:

            QtGui.QMessageBox.question(self, 'Error',
            "Genero Invalido", QtGui.QMessageBox.Ok)


    def quitargenero(self):

        global generos ,editando
        text = modulo2.genero_cb.currentText()
        generos.remove(str(text))
        index = modulo2.genero_cb.currentIndex()
        if index != 0:
            modulo2.genero_cb.removeItem(index)

    def limpiar(self):

        myPixmap = QtGui.QPixmap("./images/perview.png")
        self.qr_perview.setPixmap(QtGui.QPixmap(myPixmap))
        self.titulo_txt.setText("")
        self.autor_txt.setText("")
        self.genero_cb.setCurrentIndex(0)

    def previsualizar(self):
        
        global titulo,autor,genero
        error ,generado = False , False
        titulo = modulo2.titulo_txt.text()
        autor = modulo2.autor_txt.text()
        genero = modulo2.genero_cb.currentText()
        datos = [str(titulo), str(autor),str(genero)]
        for x in range(len(opciones)-5):
            if (datos[x] == "") or (genero == 'Seleccionar'):

                error = True

        if error != True:
        
            generarid(archlibros)
            codificar(countstr,modulo2)
            generado = True
            self.imprimir_bt.show()

        else:
            
            QtGui.QMessageBox.critical(self, 'Error',
            "Antes debe ingresar todos los datos.", QtGui.QMessageBox.Ok)
        return generado
            

    def imprimir(self):

        printerobject = QtGui.QPrinter(0)
        printdialog = QtGui.QPrintDialog(printerobject)
        if printdialog.exec_() == QtGui.QDialog.Accepted:
            pixmapImage = QtGui.QPixmap.grabWidget(self.qr_perview)
            painter = QtGui.QPainter(printerobject)
            painter.drawPixmap(0, 0, pixmapImage)
            del painter

    def qrcambiado(self):

        if editando:
            self.count += 1
            myPixmap = QtGui.QPixmap("./images/perview.png")
            self.qr_perview.setPixmap(QtGui.QPixmap(myPixmap))
            self.previsualizar_btn.hide()
            self.imprimir_bt.show()
            if self.count > 3: 
                self.imprimir_bt.hide()
                self.previsualizar_btn.show()
        else:
            myPixmap = QtGui.QPixmap("./images/perview.png")
            self.qr_perview.setPixmap(QtGui.QPixmap(myPixmap))
            self.imprimir_bt.hide()


    def aceptar(self):
        
        global datos
        global error
        if not generarid(archlibros):            
            titulo = modulo2.titulo_txt.text()
            autor = modulo2.autor_txt.text()
            genero = modulo2.genero_cb.currentText()
            estado = modulo2.estado_cb.currentText()
            if editando != True:

                datos = [str(titulo),str(autor),str(genero),'En biblioteca',0,0,0]
                self.count = 0
            
            else:

                datos = [str(titulo),str(autor),str(genero),str(estado),nprestamos,total,cflnula]

            writegeneros()
            generarid(archlibros)
            if editando != True:
                
                parserwrite(countstr)    
            
            else:

                parserwrite(str(decoded))

            if error != True:
                      
                self.limpiar()
                self.count = 0
                self.hide()

        else:

            QtGui.QMessageBox.question(self, 'Error',
            "Debe llenar todos los campos", QtGui.QMessageBox.Ok)
            error = False
        
    def close(self):
       
        self.hide()
        self.limpiar()
        self.count = 0

class Form4(QtGui.QDialog):
    
    def __init__(self, parent=None):
    
        QtGui.QDialog.__init__(self, parent)
        self.ui=loadUi("./GUI/limaui_m3.ui",self)
        self.setWindowTitle("Open LiMa - Buscar")
        centrar(self)
        global opcion , index , txt
        complete = QtGui.QCompleter()
        parser.read(archlibros)
        sections = parser.sections()
        txt = self.search_txt.text()
        opcion = 'titulo'
        index = 0
        self.list2.hide()
        for x in range(len(opciones)-4):

            self.filtro_cb.addItem(opciones[x])


    def filtro(self):

        global opcion
        self.index  = self.filtro_cb.currentIndex() 
        opcion = str(opciones[self.index]) 
        self.search_txt.clear()

    def atrasados(self):

        hoy = datetime.strptime(str(date.today()),'%Y-%m-%d')
        parser = RawConfigParser()
        parser.read(archtransacciones)
        sections = parser.sections()
        for x in range(len(sections)):
            fechaentrega  = datetime.strptime(str(parser.get(str(x),'fechaentrega')),'%A %d de %B del %Y')
            diasdeatraso , libroid = (fechaentrega - hoy).days , parser.get(str(x),'idlibro')
            if diasdeatraso < 0:
                parser = RawConfigParser()
                parser.read(archlibros)
                parser.set(libroid,'estado','Atrasado')
                with open(archlibros , 'wb') as libros:
                    parser.write(libros)


    def buscar(self):
       
        global ids ,decoded   
        parser = RawConfigParser()   
        parser.read(archlibros)
        sections = parser.sections()
        txt = self.search_txt.text()
        self.list.clear()
        self.list2.hide()
        count = 0     
        ids = {}

        for x in range(len(sections)):
    
            nm = parser.get(sections[x],str(opcion))
            match = re.search(str(txt),nm,re.I)
            if (match != None) and (txt != "") and (txt != " "):
                repetido = False
                for y in range(count):
                    
                    item = self.list.item(y).text()                                         
                    if (nm == item) and (self.index != 0):

                        repetido = True
                    
                if repetido != True:     
                    
                    ids.update({str(nm):x})
                    decoded = str(x)
                    self.list.addItem(nm)
                    self.list.setSortingEnabled(True)
                    count += 1

    def mas(self):

        global ids ,decoded
        parser = RawConfigParser()
        if self.index != 0:
            ids = {}
            self.list2.clear()
            parser = RawConfigParser()        
            parser.read(archlibros)
            sections = parser.sections()
            txt = self.list.currentItem().text()
            self.list2.show()
            repetido = False
            for x in range(len(sections)):

                nm = parser.get(sections[x],str(opcion))
                nam = parser.get(sections[x],'titulo')
                match = re.search(str(txt),nm,re.I)
                if (match != None) and (txt != "") and (txt != " "):
                
                    ids.update({str(nam):x})
                    decoded = str(x)
                    self.list2.addItem(str(nam))
                    self.list.setSortingEnabled(True)

    def seleccionar(self):

        global decoded ,status , editando
        if self.index == 0:
            a = self.list.currentItem().text()
        else:
            a = self.list2.currentItem().text() 
        decoded = ids[str(a)]
        self.search_txt.clear()
        parserread()
        if editando  == False:

            modulo0.info()
        
        else:

            modulo0.editar()

        self.hide()

   
    def close(self):
        
        modulo3.search_txt.clear()
        modulo3.hide()

class Form5(QtGui.QDialog):
    
    def __init__(self, parent=None):
    
        QtGui.QDialog.__init__(self, parent)
        self.ui=loadUi("./GUI/limaui_m4.ui",self)
        centrar(self)
        self.setWindowTitle("Open LiMa - Opciones")
        self.metodo_btn.setText(opmetodos[int(metodo)])
        parser = RawConfigParser()
        parser.read(archconfigs)
        self.lvcolor()
        self.fondocolor.setStyleSheet("QWidget { background-color: %s }"
            % self.fndcolor)
        self.tablacolor.setStyleSheet("QWidget { background-color: %s }"
            % self.tblcolor)
        self.letracolor.setStyleSheet("QWidget { background-color: %s }"
            % self.ltrcolor)
        self.letracolort.setStyleSheet("QWidget { background-color: %s }"
            % self.ltrcolort)


    def metodo(self):
        
        global metodo   
        parser = RawConfigParser()
        parser.read(archconfigs)
        if metodo == 0:
       
            metodo = 1
            parser.set('metodo','busqueda',metodo)
            self.metodo_btn.setText(opmetodos[int(metodo)])

        elif metodo == 1:

            metodo = 0
            parser.set('metodo','busqueda',metodo)
            self.metodo_btn.setText(opmetodos[int(metodo)])
      
        with open('conf.ini', 'wb') as configs:
        
            parser.write(configs)
            configs.close()



    def pickcolor(self):
        parser = RawConfigParser()
        parser.read(archconfigs)
        col = QtGui.QColorDialog.getColor()
        sender = self.sender()
        self.senderobject = sender.objectName()
        self.c = self.findChild(QtGui.QPushButton, self.senderobject)
        if col.isValid():
            self.c.setStyleSheet("QWidget { background-color: %s }"
                % col.name())

            parser.set('colores',str(self.senderobject),col.name())
            with open('conf.ini', 'wb') as configs:
        
                parser.write(configs)
                configs.close()
    def lvcolor(self):

        parser = RawConfigParser()
        parser.read(archconfigs)
        self.fndcolor = parser.get('colores','fondocolor')
        self.tblcolor = parser.get('colores','tablacolor')
        self.ltrcolor = parser.get('colores','letracolor')
        self.ltrcolort = parser.get('colores','letracolort')

    def guardar(self):

        self.hide()

class Form6(QtGui.QDialog):

    def __init__(self, parent=None):
    
        QtGui.QDialog.__init__(self, parent)
        self.ui=loadUi("./GUI/limaui_m6.ui",self)
        locale = unicode(QtCore.QLocale.system().name())
        self.setWindowTitle("Open LiMa - Prestando")
        self.nombre_txt.setText("")


    def fechas(self):
                  
        dias = self.dias_spin.value()
        self.hoy = date.today()
        entrega=self.hoy+timedelta(days=dias)
        self.fechaentrega = entrega.strftime('%A %d de %B del %Y')
        self.fechas_label.setText('Fecha de entrega: '+self.fechaentrega)
        if (entrega.strftime('%a') == 'dom') or (entrega.strftime('%a') == 'sáb'):

            QtGui.QMessageBox.critical(self, 'Error',
            "Fecha de entrega invalida", QtGui.QMessageBox.Ok)

    
    def prestar(self):
        parserread()
        if self.nombre_txt.text != "":
            parser = RawConfigParser()
            nombre = self.nombre_txt.text()
            parser.read(archtransacciones)
            generarid(archtransacciones)
            parser.add_section(countstr)
            fechaprestamo = self.hoy.strftime('%A %d de %B del %Y')
            parser.set(countstr,'idlibro',decoded)
            parser.set(countstr,'titulo',titulo)
            parser.set(countstr,'fechaprestamo',fechaprestamo)
            parser.set(countstr,'fechaentrega',self.fechaentrega)
            parser.set(countstr,'vfechadeentrega','No disponible')
            parser.set(countstr,'nombre',nombre)

            with open(archtransacciones, 'wb') as transacciones:
                parser.write(transacciones)
            parser = RawConfigParser()
            parser.read(archlibros)
            try:
                nprestamos = parser.get(decoded,'nprestamos')
                nprestamos = int(nprestamos)+1
                parser.set(decoded,'nprestamos',str(nprestamos))
            except:
                nprestamos = 1
                parser.set(decoded,'nprestamos',nprestamos)
            parser.set(decoded,'estado','Prestado')
            parser.set(decoded,'prestamoid',countstr)
            with open(archlibros, 'wb') as libros:
                parser.write(libros)
            self.close()
        else:
            QtGui.QMessageBox.critical(self, 'Error',
            "Ingrese el nombre del alumno", QtGui.QMessageBox.Ok)
    def cerrar(self):
        self.close()   

    def limpiar(self):
        self.nombre_txt.setText('')
        self.dias_spin.setValue(7)       

class Form7(QtGui.QDialog):
    
    def __init__(self, parent=None):
    
        QtGui.QDialog.__init__(self, parent)
        self.ui=loadUi("./GUI/limaui_m7.ui",self)
        self.setWindowTitle("Open LiMa - Devolviendo Libro")

    def numero(self):  
        global  total
        sender = self.sender()
        sender = str(sender.objectName())
        strnum  = sender.split('_')
        num_a = int(strnum[1])
        parser = RawConfigParser()
        parser.read(archlibros)
        try:    
            num_b = float(parser.get(decoded,'clftotal'))
        except:
            num_b = 0
        self.total = num_a + num_b

    def devolver(self):
        
        parser = RawConfigParser()
        parser.read(archlibros)
        parserread()
        self.hoy = date.today()
        fechaentrega = self.hoy.strftime('%A %d de %B del %Y')
        prestamoid = parser.get(decoded,'prestamoid')
        if self.cflnula_chk.isChecked() == False:
            parser.set(str(decoded),'estado','En biblioteca')
            parser.set(decoded,'clftotal',self.total)
        else:
            parser.set(str(decoded),'estado','En biblioteca')
            cflnulas = int(cflnula) + 1
            parser.set(decoded,'cflnula',cflnulas)
        with open(archlibros, 'wb') as libros:
            parser.write(libros)
        parser = RawConfigParser()
        parser.read(archtransacciones)
        parser.set(prestamoid,'vfechadeentrega',fechaentrega)
        with open(archtransacciones, 'wb') as transacciones:
            parser.write(transacciones)
        self.close()
class Login(QtGui.QDialog):
    
    def __init__(self, parent=None):
    
        QtGui.QDialog.__init__(self, parent)
        self.ui=loadUi("./GUI/login.ui",self)
        self.setWindowTitle("Open LiMa - Login")
        self.setWindowIcon(QtGui.QIcon('./images/limaico.png'))
        modulo0 = Form1()


    def entrar(self):

        parser = RawConfigParser()
        parser.read("./data/login.ini")
        passdb = parser.get('pass','pass')
        passus = self.passus_txt.text()
        if passdb == passus:
           
            modulo0.show()
            self.hide()

        else:

            QtGui.QMessageBox.critical(self, 'Error',
            "Password incorrecto", QtGui.QMessageBox.Ok)
            self.passus_txt.setText("")

    def cambiar(self):

        modulo5.show()

    def cerrar(self):

        self.close()

class CambiarPassword(QtGui.QDialog):
    
    def __init__(self, parent=None):
    
        QtGui.QDialog.__init__(self, parent)
        self.ui=loadUi("./GUI/loginc.ui",self)
        self.setWindowTitle("Open LiMa - Cambiar Password")

    def guardar(self):

        parser = RawConfigParser()
        parser.read("./data/login.ini")
        passdb = parser.get('pass','pass')
        passus = self.passus_txt.text()
        passn = self.nuevopass_txt.text()
        passnr = self.repetirpass_txt.text()
        if passdb == passus:
           
            if passn == passnr:
                  
                parser.set('pass','pass',passn)
                self.close()          
                with open('login.ini', 'wb') as login:
        
                    parser.write(login)
            else:

                QtGui.QMessageBox.critical(self, 'Error',
            "Los password no coinciden", QtGui.QMessageBox.Ok)
            self.passus_txt.setText("")


        else:

            QtGui.QMessageBox.critical(self, 'Error',
            "Password incorrecto", QtGui.QMessageBox.Ok)
            self.passus_txt.setText("")

    def cancelar(self):

        self.close()

def ajustart(modulo1):

    size = modulo0.geometry()
    height = size.height()
    width = size.width()
    modulo1.resize(width, height)

def decodificar():
       
    global status
    global decoded
    noint = False
    code = QR()
    code.decode_webcam()
    pre_decoded = code.data
    decoded_vector = pre_decoded.split('#')
    decoded = decoded_vector[0]
    generarid(archlibros) 
    try:
        int(decoded)
    except ValueError:
        noint = True
    if (decoded != "NULL") and (decoded <= countstr) and (noint != True):
        status = 1
        
def errordecodificar():

    msgBox = QtGui.QMessageBox()
    msgBox.setWindowTitle('Error')
    msgBox.setText('No se pudo decodificar. Intentar nuevamente ?')
    btnSi   = QtGui.QPushButton('Si')
    msgBox.addButton(btnSi, QtGui.QMessageBox.YesRole)
    btnNo   = QtGui.QPushButton('No')
    msgBox.addButton(btnNo, QtGui.QMessageBox.NoRole)
    
    reply = msgBox.exec_()
    global status
    if reply == 1:
        
        status = 2
    
    elif reply == 0:
       
        status = 0


def codificar(countstr,modulo2):

    modulo2.qr_perview.resize(145,145)
    qr = QRCode(version=1,box_size=5)
    if editando:
        countstr = decoded
    qr.add_data(str(countstr)+"#\nTitulo : "+titulo+"\nAutor : "+\
    autor+"\nGenero : "+genero)
    imd = qr.make()
    im = qr.make_image()
    im.save("./temp/image.png")
    myPixmap = QtGui.QPixmap("./temp/image.png")
    myScaledPixmap = myPixmap.scaled(modulo2.qr_perview.size())
    modulo2.qr_perview.setPixmap(QtGui.QPixmap(myScaledPixmap))
    modulo2.qr_perview.setScaledContents(True)

def centrar(modulo1):
  
    screen = QtGui.QDesktopWidget().screenGeometry()
    size = modulo1.geometry()
    modulo1.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

def generarid(libros):

        global count
        global countstr
        parser = RawConfigParser() 
        parser.read(libros)
        section = True
        count = -1
        while section == True:
            count += 1
            if section == True:
                section = parser.has_section(str(count))
    
        countstr = str(count)

def parserread():

    global titulo , autor , genero , estado ,nprestamos,prestamoid,fechaprestamo,fechaentrega,nombre,total,cflnula,vfechadeentrega
    parser = RawConfigParser()        
    parser.read(archlibros)
    datos = []
    for x in range(len(opciones)-1):
        info = parser.get(str(decoded),opciones[x]) 
        datos.append(info)
    titulo = datos[0]
    autor = datos[1]
    genero = datos[2]
    estado = datos[3]
    nprestamos = datos[4]
    total = datos[5]
    cflnula = datos[6]
    if (estado == 'Prestado') or (estado == 'Atrasado'):
        prestamoid = parser.get(str(decoded),'prestamoid')
        parser = RawConfigParser()
        parser.read(archtransacciones)
        fechaprestamo = parser.get(prestamoid,'fechaprestamo')
        fechaentrega = parser.get(prestamoid,'fechaentrega')
        nombre = parser.get(prestamoid,'nombre')
    



def readgeneros():
 
    global generos
    archgeneros = open('./data/generos.txt')
    generos = archgeneros.read()
    generos = generos.split(",")
    archgeneros.close()

def writegeneros():

    archgeneros = open('./data/generos.txt','w')
    generosw = ",".join(generos)
    archgeneros.write(generosw)
    archgeneros.close()
    

def parserwrite(countstr):  

    parser = RawConfigParser()        
    parser.read(archlibros)
    if editando == False:    
        
        parser.add_section(countstr)
    
    global error
    for x in range(len(opciones)-1):
        if (datos[x] != "") and (datos[x] != "Seleccionar"):

            parser.set(countstr,opciones[x],datos[x])    

        else:

            error = True

    if error != True:
        with open(archlibros, 'wb') as libros:
        
            parser.write(libros)

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp = Login()
    myapp.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    centrar(myapp)
    myapp.show()
    sys.exit(app.exec_())
