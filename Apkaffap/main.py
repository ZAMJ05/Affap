from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataAdapter
import sqlite3

class GestorPrestamosApp(App):
    def build(self):
        self.conn = sqlite3.connect('prestamos.db')
        self.c = self.conn.cursor()

        # Crear la interfaz
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campos de entrada
        self.promotora_input = TextInput(hint_text="Promotora", multiline=False)
        self.cliente_input = TextInput(hint_text="Cliente", multiline=False)
        self.aval_input = TextInput(hint_text="Aval", multiline=False)
        self.deuda_input = TextInput(hint_text="Deuda", multiline=False)
        self.demanda_input = TextInput(hint_text="Demanda", multiline=False)

        # Botones
        btn_guardar = Button(text="Guardar", on_press=self.guardar)
        btn_mostrar = Button(text="Mostrar Todos", on_press=self.mostrar_todos)

        # Lista de clientes
        self.lista_clientes = RecycleView()

        # Agregar widgets al layout
        layout.add_widget(self.promotora_input)
        layout.add_widget(self.cliente_input)
        layout.add_widget(self.aval_input)
        layout.add_widget(self.deuda_input)
        layout.add_widget(self.demanda_input)
        layout.add_widget(btn_guardar)
        layout.add_widget(btn_mostrar)
        layout.add_widget(self.lista_clientes)

        return layout

    def guardar(self, instance):
        promotora = self.promotora_input.text
        cliente = self.cliente_input.text
        aval = self.aval_input.text
        deuda = float(self.deuda_input.text)
        demanda = float(self.demanda_input.text)

        self.c.execute("INSERT INTO clientes (promotora, cliente, aval, deuda, demanda) VALUES (?, ?, ?, ?, ?)",
                       (promotora, cliente, aval, deuda, demanda))
        self.conn.commit()
        self.mostrar_todos()

    def mostrar_todos(self, instance=None):
        self.c.execute("SELECT promotora, cliente, aval, deuda, demanda FROM clientes")
        datos = self.c.fetchall()

        # Actualizar la lista de clientes
        self.lista_clientes.data = [{'text': f"{row[0]} - {row[1]} - ${row[3]:,.2f}"} for row in datos]

    def on_stop(self):
        self.conn.close()

if __name__ == '__main__':
    GestorPrestamosApp().run()