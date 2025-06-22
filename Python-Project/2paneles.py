Construye una aplicación gráfica utilizando la biblioteca wxPython que contenga dos paneles de diferentes colores: uno en la parte superior y otro en la parte inferior de la ventana. En el panel superior, coloca un botón con el texto "Saludar". Al hacer clic en este botón, se debe cambiar el texto de un StaticText ubicado en el panel inferior para que muestre el mensaje "Hi Kissling!". Utiliza la clase App proporcionada por wxPython para inicializar y mostrar la aplicación.


from wx import *


class MyApp(App):
    def OnInit(self):
         frame = Frame(None, size=(500, 800))
         panel = Panel(frame)
         panel1 = Panel(panel, pos=(0,0), size=(-1, 400))
         panel1.SetBackgroundColour('cyan')
         button1 = Button(panel1, -1, label="Saludar")
         button1.Bind(EVT_BUTTON, self.mostrar)

         panel2 = Panel(panel, pos=(0,400), size=(-1, 400))
         panel2.SetBackgroundColour('maroon')
         self.st = StaticText(panel2)
         sizer = BoxSizer(VERTICAL)
         sizer.Add(panel1,0,EXPAND|ALL,border=10)
         sizer.Add(panel2,0,EXPAND|ALL,border=10)
         panel.SetSizer(sizer)
         frame.Show(True)
         return True

    def mostrar(self, event):
        self.st.SetLabel("Hi Kissling!")


app = MyApp()
app.MainLoop()
