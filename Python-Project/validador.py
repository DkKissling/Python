
Consigna de Ejercicio
Implementar un validador en wxPython que permita solo números y punto decimal en un control de texto.

Instrucciones:
Definir la clase MyValidator que herede de wx.Validator:

En el constructor (__init__), asocia el evento de carácter (wx.EVT_CHAR) con el método OnChar.
Implementa el método Clone para devolver una nueva instancia del validador.
Implementa el método OnChar para permitir solo números, punto decimal y la tecla TAB.
Crear una ventana (MyFrame) que contenga un control de texto (wx.TextCtrl) con el validador MyValidator

import wx

class MyValidator(wx.Validator):
    def __init__(self):
        super().__init__()
        # Asocia el evento de carácter con el método OnChar
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        # Devuelve una nueva instancia de MyValidator
        return MyValidator()

    def OnChar(self, event):
        # Define los caracteres válidos
        caracteres_validos = set("0123456789.")
        key = event.GetKeyCode()
        
        # Verifica si la tecla es TAB o un carácter válido
        if key == wx.WXK_TAB or chr(key) in caracteres_validos:
            # Permite que el evento sea procesado más adelante
            event.Skip()
        else:
            # No procesa el evento más adelante
            return

# Ejemplo de uso en una aplicación simple de wxPython
class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Crea un control de texto con el validador personalizado
        text_ctrl = wx.TextCtrl(panel, validator=MyValidator())
        sizer.Add(text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        
        panel.SetSizer(sizer)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, title="Ejemplo de Validador")
    app.MainLoop()



