Crea una aplicación de escritorio utilizando la librería wxPython que permita al usuario ingresar dos números y calcular su suma. La aplicación debe contar con las siguientes características:

Una interfaz gráfica con dos campos de texto donde el usuario pueda ingresar los números.
Un botón "Sumar" que, al ser presionado, calcule la suma de los dos números ingresados.
Un área de texto donde se muestre el resultado de la suma.
Validación de entrada: los campos de texto sólo deben aceptar números reales (enteros o decimales).

La aplicación debe estar estructurada en dos archivos:

Un archivo principal que contenga la lógica de la interfaz gráfica y la funcionalidad de la suma.
Un archivo separado que contenga una clase de validación personalizada para los campos de texto.

Al ejecutar la aplicación, el usuario podrá ingresar dos números en los campos de texto correspondientes, presionar el botón "Sumar" y ver el resultado de la suma en el área de texto designada para ello. Si el usuario ingresa valores no numéricos en los campos de texto, la aplicación debe evitar que se realice la operación y mostrar un mensaje de error.

from wx import *
from validador import *

class MyApp(App):
    def OnInit(self):
        f = Frame(None)
        p = Panel(f)

# fila 2 - las cajas de texto        
        self.n1 = n1 = TextCtrl(p, validator=MyValidator())
        self.n2 = n2 = TextCtrl(p, validator=MyValidator())
        fila2 = BoxSizer(HORIZONTAL)
        fila2.Add(n1, 0, ALL, 10)
        fila2.Add(n2, 0, ALL, 10)

# main sizer
        s = BoxSizer(VERTICAL)
        flags = ALL|CENTER
        solicitud = StaticText(p, -1, "Ingrese dos números")
        s.Add(solicitud, 0, flags, 10)
        
        s.Add(fila2, 0, flags, 10)
        
        self.b = b = Button(p, label="Sumar")
        b.Bind(EVT_BUTTON, self.suma)
        s.Add(b, 0, flags, 10)

        self.t = t = StaticText(p, label="Resultado")
        s.Add(t, 0, flags, 25)

        p.SetSizer(s)
        f.Show()
        return True

    def suma(self, event):
        s = str(float(self.n1.GetValue()) + float(self.n2.GetValue()))
        s = self.t.GetLabel() + " = " + s
        self.t.SetLabel(s)
        

app = MyApp()
app.MainLoop()
