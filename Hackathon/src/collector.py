import kivy
from kivy.uix.button import *
from kivy.uix.label import *
from kivy.uix.gridlayout import *
from kivy.uix.textinput import *
from kivy.uix.popup import *
import src.report_handler as report_handler


class NameAgePopup(Popup):
    def __init__(self, **kwargs):
        super(NameAgePopup, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, rows=1, spacing=10, padding=50)
        self.layout.add_widget(Label(text='Please enter your name and age', font_size=30))
        self.add_widget(self.layout)
        # Once the user enters their name and age, store the information in a .csv file using report_handler.py
        self.name = TextInput(text='Name')
        self.age = TextInput(text='Age')
        self.layout.add_widget(self.name)
        self.layout.add_widget(self.age)
        self.layout.add_widget(Button(text='Submit', on_press=self.submit))
        self.add_widget(self.layout)

    def submit(self, instance):
        name = self.name.text
        age = self.age.text
        report_handler.add_name_age(name, age)
        self.dismiss()
