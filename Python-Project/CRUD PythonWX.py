Desarrolla un programa de gestión de datos de datos que utilice una interfaz gráfica. El programa debe permitir cargar, visualizar, modificar, eliminar y buscar datos en una base de datos SQLite. Utiliza controles como DataViewListCtrl, TextCtrl, SearchCtrl, CheckBox, ComboBox y DatePickerCtrl para facilitar la interacción del usuario. Además, implementa una barra de menú que ofrezca opciones para realizar estas acciones.


## wx_alumnos_BD_2020_search_menu.py + creación de base de datos vacía

from wx import *
from wx.dataview import * 
import sqlite3
from sqlite3 import Error
from wx.adv import *

class MyApp(App):

    def OnInit(self):
        self.initUI()
        return True

    def initUI(self):
        # Configuración de la ventana principal
        self.frame = Frame(None, -1, "Listado de Fallecidos", size=(700, 500))
        self.panel = Panel(self.frame)

        # Configuración del DataViewListCtrl
        self.dvlc = DataViewListCtrl(self.panel)
        self.dvlc.Bind(EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.modif)
        self.setupDataViewListCtrl()

        # Controles de entrada
        self.nombreBD = TextCtrl(self.panel, style=TE_PROCESS_ENTER)
        self.search = SearchCtrl(self.panel, size=(-1, 33))
        self.search.Hide()
        self.search.ShowCancelButton(True)
        self.search.Bind(EVT_TEXT, self.buscar)

        # Configuración del layout
        sizer = BoxSizer(VERTICAL)
        sizer.Add(self.dvlc, 1, EXPAND)
        sizer.Add(self.nombreBD, 0, EXPAND)
        sizer.Add(self.search, 0, EXPAND)
        self.panel.SetSizer(sizer)

        # Barra de menú
        self.setupMenuBar()

        # Mostrar ventana principal
        self.frame.Show()

    def setupDataViewListCtrl(self):
        """Configura las columnas del DataViewListCtrl."""
        columns = ['#', 'Apellido y Nombre', 'Fecha', 'Localidad', 'Autorizado', 'Destino']
        widths = [30, 200, 75, 100, 200, 50]
        for col, width in zip(columns, widths):
            mode = DATAVIEW_CELL_EDITABLE if col == 'Destino' else DATAVIEW_CELL_INERT
            self.dvlc.AppendTextColumn(col, width=width, mode=mode)
        
        for c in self.dvlc.Columns:
            c.Sortable = True
            c.Reorderable = True

    def setupMenuBar(self):
        """Configura la barra de menú."""
        menuBar = MenuBar()
        menu1 = Menu()
        menu1.Append(101, "&Carga", "Traer todos los datos")
        menu1.Append(102, "&Alta", "Insertar un dato nuevo")
        menu1.AppendSeparator()
        menu1.Append(103, "&Eliminar", "Borrar fila")
        menu1.AppendSeparator()
        menu1.Append(104, "&Buscar", "Buscar por nombre")
        menu1.Append(105, "&Salir", "Cerrar el programa")
        menuBar.Append(menu1, "&Archivo")
        self.frame.SetMenuBar(menuBar)

        # Bind de eventos del menú
        idList = [101, 102, 103, 104, 105]
        for e in idList:
            self.frame.Bind(EVT_MENU, self.accion, id=e)

    def accion(self, event):
        """Gestiona las acciones del menú."""
        id = event.GetId()
        if id == 101:
            self.cargaDatos()
        elif id == 102:
            self.alta()
        elif id == 103:
            self.borrar()
        elif id == 104:
            self.search.Show()
            self.panel.Layout()
            self.search.SetFocus()
        elif id == 105:
            self.frame.Close()

    def buscar(self, event):
        """Buscar y filtrar los datos mostrados."""
        busco = self.search.GetValue()
        num = self.search.GetLastPosition()
        tot = self.dvlc.GetItemCount()
        for i in range(tot):
            self.dvlc.DeleteItem(0)

        for item in self.busqueda:
            if busco.lower() in item[1].lower()[:num]:
                self.dvlc.AppendItem(item)

    def cargaDatos(self):
        """Carga los datos desde la base de datos."""
        def recupBD():
            try:
                con = sqlite3.connect("muertos.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM datos ORDER BY ApeyNom")
                tuplas = cur.fetchall()
                con.close()
                return [list(e) for e in tuplas]
            except Error as e:
                print(f"Error al conectar a la base de datos: {e}")
                return []

        lista = recupBD()
        for e in lista:
            self.dvlc.AppendItem(e)
        self.busqueda = lista

    def modif(self, evt):
        """Modifica los datos en la base de datos."""
        def grabaBD(id, destino):
            try:
                con = sqlite3.connect("muertos.db")
                cur = con.cursor()
                actu = f"UPDATE datos SET destino='{destino}' WHERE id={id}"
                cur.execute(actu)
                con.commit()
                con.close()
            except Error as e:
                print(f"Error al actualizar la base de datos: {e}")

        row = self.dvlc.GetSelectedRow()
        id = self.dvlc.GetTextValue(row, 0)
        destino = self.dvlc.GetTextValue(row, 5)
        grabaBD(id, destino)

    def alta(self):
        """Abre una ventana para agregar un nuevo registro."""
        f2 = Frame(None, title="Agregar fallecido", size=(500, 350))
        p2 = Panel(f2)
        col1 = GridBagSizer(5, 5)

        # Apellido y Nombre
        l_ape = StaticText(p2, -1, "Apellido y Nombre")
        col1.Add(l_ape, pos=(0, 0), flag=TOP|ALIGN_CENTER, border=5)
        self.ape = TextCtrl(p2, -1, "")
        col1.Add(self.ape, pos=(0, 1), span=(1, 2), flag=EXPAND)

        # Fecha
        l_fna = StaticText(p2, -1, "Fecha")
        col1.Add(l_fna, pos=(2, 0), flag=TOP|ALIGN_CENTER, border=5)
        self.fna = DatePickerCtrl(p2, size=(120, -1), style=DP_DROPDOWN | DP_SHOWCENTURY)
        self.fna.Bind(EVT_DATE_CHANGED, self.OnDateChanged)
        col1.Add(self.fna, pos=(2, 1), span=(1, 2), flag=EXPAND)

        # Localidad
        l_pro = StaticText(p2, -1, "Localidad")
        col1.Add(l_pro, pos=(3, 0), flag=TOP|ALIGN_CENTER, border=5)
        proList = ["Local", "Reinscripcion"]
        self.pro = ComboBox(p2, 500, "", (0, 0), (-1, -1), proList, CB_DROPDOWN | TE_PROCESS_ENTER)
        col1.Add(self.pro, pos=(3, 1), span=(1, 2), flag=EXPAND)

        # Autorización
        l_adi = StaticText(p2, -1, "Se autoriza:")
        col1.Add(l_adi, pos=(4, 0), flag=TOP|ALIGN_CENTER, border=5)
        self.adi1 = CheckBox(p2, -1, "Sepultura")
        self.adi2 = CheckBox(p2, -1, "Cremacion")
        self.adi3 = CheckBox(p2, -1, "Libre traslado")
        col1.Add(self.adi1, pos=(4, 1))
        col1.Add(self.adi2, pos=(4, 2))
        col1.Add(self.adi3, pos=(4, 3))

        # Botón de Alta
        b = Button(p2, -1, "&Alta")
        b.Bind(EVT_BUTTON, self.altaBD)
        col1.Add(b, pos=(5, 3), span=(1, 1))
        p2.SetSizer(col1)
        f2.Show()

    def altaBD(self, event):
        """Agrega un nuevo registro a la base de datos."""
        ApeyNom = self.ape.GetValue()
        fecha = self.fe
        localidad = self.pro.GetValue()
        Autorizado = ""
        if self.adi1.GetValue():
            Autorizado += "Sepultura"
        if self.adi2.GetValue():
            Autorizado += " Cremacion"
        if self.adi3.GetValue():
            Autorizado += " Traslado"
        destino = " "

        self.dvlc.AppendItem(["0", ApeyNom, fecha, localidad, Autorizado, destino])
        try:
            con = sqlite3.connect("muertos.db")
            cur = con.cursor()
            alta = f"INSERT INTO datos (ApeyNom, fecha, localidad, Autorizado, destino) VALUES (?, ?, ?, ?, ?)"
            cur.execute(alta, (ApeyNom, fecha, localidad, Autorizado, destino))
            con.commit()
            con.close()
        except Error as e:
            print(f"Error al insertar en la base de datos: {e}")

    def borrar(self):
        """Elimina un registro de la base de datos."""
        def borraBD(id):
            try:
                con = sqlite3.connect("muertos.db")
                cur = con.cursor()
                dele = f"DELETE FROM datos WHERE id=?"
                cur.execute(dele, (id,))
                con.commit()
                con.close()
            except Error as e:
                print(f"Error al borrar en la base de datos: {e}")

        row = self.dvlc.GetSelectedRow()
        id = self.dvlc.GetTextValue(row, 0)
        self.dvlc.DeleteItem(row)
        borraBD(id)

    def OnDateChanged(self, evt):
        """Maneja el evento de cambio de fecha."""
        d = evt.GetDate()
        self.fe = d.FormatISODate()

prog = MyApp()
prog.MainLoop()

