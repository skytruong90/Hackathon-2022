import kivy
from kivy.app import *
from kivy.uix.button import *
from kivy.uix.label import *
from kivy.uix.gridlayout import *
from kivy.uix.textinput import *
from kivy.uix.screenmanager import *
from kivy.uix.popup import *
from kivy.uix.image import *
import src.report_handler
import src.collector
import src.nearest_hospital
from src import report_handler

sm = ScreenManager()

# The time crunch forces bad decisions, like global variables. When I graduate in 2.5 years and if I'm working for
# you, I'll fix this :).
global confidence_level
confidence_level = 0.0
global level
level = 0
global name
name = ""
global age
age = 0
# Mode options
# Pain = 1
# Drowsiness = 2
# Mental Health = 3
# Suicidal Thoughts = 4
global mode
mode = 0


class ConfidencePopup(Popup):
    def __init__(self, **kwargs):
        super(ConfidencePopup, self).__init__(**kwargs)
        self.layout = GridLayout(cols=4, rows=4, spacing=10, padding=50)
        # The follow labels depend on mode.
        # Pain = 1
        # Drowsiness = 2
        # Mental Health = 3
        if mode == 1:
            self.title = "Pain Level Confirmation"
            self.layout.add_widget(Label(text="At level 1, pain may be barely\n"
                                              "noticeable and easily ignored.\n"
                                              "Level 2 pain is annoying and may\n"
                                              "flare into occasional stronger\n"
                                              "twinges. Pain at level 3 is\n"
                                              "distracting, but you can learn\n"
                                              "to adapt to it.", font_size=24))
            self.layout.add_widget(Label(text=" You may be able to push level 4\n"
                                              " pain aside for periods while\n"
                                              " involved in a task, but it is\n"
                                              " still very distracting. Level 5\n"
                                              " pain can’t be ignored for more\n"
                                              " than a few minutes, but you can\n"
                                              " push through it with effort. At\n"
                                              " level 6, the pain may make it\n"
                                              " hard for you to concentrate on\n"
                                              " regular tasks.", font_size=24))
            self.layout.add_widget(Label(text="At level 7, the pain demands your\n"
                                              "attention and keeps you from\n"
                                              "performing tasks. It may even\n"
                                              "interfere with your sleep.\n"
                                              "Level 8 pain is intense, limiting\n"
                                              "physical activity and even making\n"
                                              "conversation difficult. Pain at\n"
                                              "level 9 leaves you unable to\n"
                                              "converse. You may just be moaning\n"
                                              "or crying uncontrollably. The\n"
                                              "greatest pain, level 10, leaves\n"
                                              "you bedridden or even delirious.", font_size=24))
        elif mode == 2:
            self.title = "Drowsiness Level Confirmation"
            self.layout.add_widget(Label(text="Drowsiness goes from 0-10,\n"
                                              "where 0 is fully alert and 10 is\n"
                                              "impossible to stay awake.\n", font_size=24))
            self.layout.add_widget(Label(text="Drowsiness is not as well defined\n"
                                              "as other measures (like pain).\n"
                                              "A general rule of thumb is that\n"
                                              "if you are barely tired, it'sa 1.\n"
                                              "If your tiredness is\n"
                                              "distracting you and causing\n"
                                              "you to have trouble with\n"
                                              "everyday activites, it's a 5.\n"
                                              "If you literally can\n"
                                              "not stay awake for more\n"
                                              "than a few moments, it's\n"
                                              "a 10.", font_size=24))
            self.layout.add_widget(Label(text="Consider how much your\n"
                                              "tiredness truly affects\n"
                                              "your activities.", font_size=24))
        elif mode == 3:
            self.title = "Mental Health Level Confirmation"
            self.layout.add_widget(Label(text=" ", font_size=24))
            self.layout.add_widget(Label(text="  0 = Life is perfect.\n"
                                              "  1 = Life is nearly as perfect as it can be.\n"
                                              "  2 = You're a little disappointed or frustrated, but you can easily be cheered up.\n"
                                              "  3 = Things are bothering you, but you're coping. You might be overtired or hungry.\n"
                                              "  4 = Today is a bad day, but you can still get through it.\n"
                                              "  5 = Your mental health is starting to impact your everyday life. Easy things are slightly more difficult.\n"
                                              "  6 = You can't do the things you usually do. Impulsive thoughts are hard to cope with.\n"
                                              "  7 = You're avoiding things that make you feel distressed, and it's making it worse. This is serious.\n"
                                              "  8 = You can't hide your struggles anymore. Issues sleeping, eating, working... all parts of life affected.\n"
                                              "  9 = Critical point: You can no longer function, and you may be a danger to others and yourself.\n"
                                              "10 = You can not take care of yourself. Things can not be worse. You need to contact help immediately.",
                                         font_size=24))
            self.layout.add_widget(Label(text=" ", font_size=24))
        self.layout.add_widget(Button(text='Back', on_press=self.back))
        self.layout.add_widget(Button(text='Possibly inaccurate', on_press=self.possibly_inaccurate))
        self.layout.add_widget(Button(text='Accurate', on_press=self.accurate))
        self.layout.add_widget(Button(text='Mostly accurate', on_press=self.mostly_accurate))
        self.layout.add_widget(Button(text='Perfectly accurate', on_press=self.perfectly_accurate))
        self.add_widget(self.layout)

    def back(self, instance):
        self.dismiss()
        sm.current = 'welcome'

    def possibly_inaccurate(self, instance):
        confidence = 0.2
        if mode == 1:
            self.dismiss()
            src.report_handler.add_pain_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 2:
            self.dismiss()
            src.report_handler.add_drowsiness_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 3:
            self.dismiss()
            src.report_handler.add_mental_health_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 4:
            self.dismiss()
            src.report_handler.add_suicidal_thoughts_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)

    def accurate(self, instance):
        confidence = 0.5
        if mode == 1:
            self.dismiss()
            src.report_handler.add_pain_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 2:
            self.dismiss()
            src.report_handler.add_drowsiness_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 3:
            self.dismiss()
            src.report_handler.add_mental_health_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 4:
            self.dismiss()
            src.report_handler.add_suicidal_thoughts_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)

    def mostly_accurate(self, instance):
        confidence = 0.7
        if mode == 1:
            self.dismiss()
            src.report_handler.add_pain_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 2:
            self.dismiss()
            src.report_handler.add_drowsiness_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 3:
            self.dismiss()
            src.report_handler.add_mental_health_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 4:
            self.dismiss()
            src.report_handler.add_suicidal_thoughts_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)

    def perfectly_accurate(self, instance):
        confidence = 1.0
        if mode == 1:
            self.dismiss()
            src.report_handler.add_pain_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 2:
            self.dismiss()
            src.report_handler.add_drowsiness_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 3:
            self.dismiss()
            src.report_handler.add_mental_health_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)
        elif mode == 4:
            self.dismiss()
            src.report_handler.add_suicidal_thoughts_report(self, name, age, level, confidence)
            sm.current = 'welcome'
            show_success(self)


def show_success(self):
    self.popup = Popup(title='Success!', size_hint=(None, None), size=(800, 400))
    self.popup_layout = GridLayout(cols=1, rows=1, spacing=10, padding=50)
    EmailPopup().open()
    self.popup_layout.add_widget(Label(text='Information has been recorded.\nPlease let your provider know you have '
                                            'the file ready.\nYou should inform them even if you try to\nemail them '
                                            'with this application.', font_size=30))
    self.popup.add_widget(self.popup_layout)
    self.popup.open()


class PainReport(Screen):
    def __init__(self, **kwargs):
        super(PainReport, self).__init__(**kwargs)
        self.layout = GridLayout(cols=3, rows=2, spacing=10, padding=50)
        self.layout.add_widget(
            Label(text='Please enter your pain level from 0-10\n  0 = No pain\n10 = Extreme pain', font_size=30))
        self.add_widget(self.layout)
        self.pain_level = TextInput(text='')
        self.layout.add_widget(self.pain_level)
        self.layout.add_widget(Button(text='Submit', on_press=self.submit))
        self.layout.add_widget(Image(source='../images/pain_scale.png'))
        # Disable the nearest_hospital function for now, it's too risky to share my API key.
        # self.layout.add_widget(Label(text=str(src.nearest_hospital.hospital_finder()), font_size=30))
        self.layout.add_widget(Label(text='South Georgia Medical Center\nCall: 229-433-1000', font_size=30))
        self.layout.add_widget(Button(text='Back', on_press=self.go_to_welcome))

    def submit(self, instance):
        global mode
        mode = 1
        try:
            global level
            level = int(self.pain_level.text)
            print("(Debug) Pain level: " + str(level))
            if level < 0 or level > 10:
                raise ValueError
            else:
                ConfidencePopup().open()
        except ValueError:
            self.popup = Popup(title='Error', size_hint=(None, None), size=(400, 400))
            self.popup_layout = GridLayout(cols=1, rows=1, spacing=10, padding=50)
            self.popup_layout.add_widget(Label(text='Please enter a valid number\n(0-10)', font_size=30))
            self.popup.add_widget(self.popup_layout)
            self.popup.open()

    @staticmethod
    def go_to_welcome(instance):
        sm.current = 'welcome'


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.layout = GridLayout(cols=3, rows=4, spacing=10, padding=50)
        self.layout.add_widget(Image(source='../images/AZALEA_LOGO.png'))
        self.layout.add_widget(Label(text='Welcome to AIRS!\nAccurate Interactive Report System', font_size=30))
        self.layout.add_widget(Button(text='Report pain', on_press=self.go_to_pain_report))
        self.layout.add_widget(Button(text='Report drowsiness', on_press=self.go_to_drowsiness_report))
        self.layout.add_widget(Button(text='Report mental health', on_press=self.go_to_mental_health_report))
        self.layout.add_widget(Button(text='Report suicidal thoughts', on_press=self.go_to_suicidal_thoughts_report))
        self.add_widget(self.layout)

    @staticmethod
    def go_to_pain_report(instance):
        NamePopup().open()
        sm.current = 'pain_report'

    @staticmethod
    def go_to_drowsiness_report(instance):
        NamePopup().open()
        sm.current = 'drowsiness_report'

    @staticmethod
    def go_to_mental_health_report(instance):
        NamePopup().open()
        sm.current = 'mental_health_report'

    @staticmethod
    def go_to_suicidal_thoughts_report(instance):
        # This person is suicidal, so we just want them to get help.
        # We don't need data here.
        sm.current = 'suicidal_thoughts_report'


class NamePopup(Popup):
    def __init__(self, **kwargs):
        super(NamePopup, self).__init__(**kwargs)
        self.title = 'Please enter your name and age to get started.'
        self.layout = GridLayout(cols=2, rows=5, spacing=10, padding=50)
        self.layout.add_widget(Label(text='Please enter your name', font_size=30))
        self.name = TextInput(text='')
        self.layout.add_widget(self.name)
        self.layout.add_widget(Label(text='Please enter your age', font_size=30))
        self.age = TextInput(text='')
        self.layout.add_widget(self.age)
        self.layout.add_widget(Button(text='Submit', on_press=self.submit))
        self.add_widget(self.layout)

    def submit(self, instance):
        print("(Debug) Name: " + self.name.text)
        print("(Debug) Age: " + self.age.text)
        global name
        global age
        name = self.name.text
        age = self.age.text
        self.dismiss()


class DrowsinessReport(Screen):
    def __init__(self, **kwargs):
        super(DrowsinessReport, self).__init__(**kwargs)
        self.layout = GridLayout(cols=3, rows=2, spacing=10, padding=50)
        self.layout.add_widget(
            Label(text='Please enter your drowsiness level\nfrom 0-10\n  0 = Alert\n10 = Extremely drowsy',
                  font_size=30))
        self.add_widget(self.layout)
        self.level = TextInput(text='')
        self.layout.add_widget(self.level)
        self.layout.add_widget(Button(text='Submit', on_press=self.submit))
        self.layout.add_widget(Image(source='../images/tired.jpg'))
        # Disable the nearest_hospital function for now, it's too risky to share my API key.
        # self.layout.add_widget(Label(text=str(src.nearest_hospital.hospital_finder()), font_size=30))
        self.layout.add_widget(Label(text='South Georgia Medical Center\nCall: 229-433-1000', font_size=30))
        self.layout.add_widget(Button(text='Back', on_press=self.go_to_welcome))

    def submit(self, instance):
        global mode
        mode = 2
        try:
            global level
            level = int(self.level.text)
            print("(Debug) Pain level: " + str(level))
            if level < 0 or level > 10:
                raise ValueError
            else:
                ConfidencePopup().open()
        except ValueError:
            self.popup = Popup(title='Error', size_hint=(None, None), size=(400, 400))
            self.popup_layout = GridLayout(cols=1, rows=1, spacing=10, padding=50)
            self.popup_layout.add_widget(Label(text='Please enter a valid number\n(0-10)', font_size=30))
            self.popup.add_widget(self.popup_layout)
            self.popup.open()

    @staticmethod
    def go_to_welcome(instance):
        sm.current = 'welcome'


class MentalHealthReport(Screen):
    def __init__(self, **kwargs):
        super(MentalHealthReport, self).__init__(**kwargs)
        self.layout = GridLayout(cols=3, rows=2, spacing=10, padding=50)
        self.layout.add_widget(
            Label(text='Please enter your mental health level\nfrom 0-10\n  0 = Worst\n10 = Best', font_size=30))
        self.add_widget(self.layout)
        self.level = TextInput(text='')
        self.layout.add_widget(self.level)
        self.layout.add_widget(Button(text='Submit', on_press=self.submit))
        self.layout.add_widget(Image(source='../images/happy_face_scale.jpg'))
        # Disable the nearest_hospital function for now, it's too risky to share my API key.
        # self.layout.add_widget(Label(text=str(src.nearest_hospital.hospital_finder()), font_size=30))
        self.layout.add_widget(Label(text='South Georgia Medical Center\nCall: 229-433-1000', font_size=30))
        # This option is to go back to welcome screen
        self.layout.add_widget(Button(text='Back', on_press=self.go_to_welcome))

    def submit(self, instance):
        global mode
        mode = 3
        try:
            global level
            level = int(self.level.text)
            print("(Debug) Mental Health level: " + str(level))
            if level < 0 or level > 10:
                raise ValueError
            else:
                ConfidencePopup().open()
        except ValueError:
            self.popup = Popup(title='Error', size_hint=(None, None), size=(400, 400))
            self.popup_layout = GridLayout(cols=1, rows=1, spacing=10, padding=50)
            self.popup_layout.add_widget(Label(text='Please enter a valid number\n(0-10)', font_size=30))
            self.popup.add_widget(self.popup_layout)
            self.popup.open()

    @staticmethod
    def go_to_welcome(instance):
        sm.current = 'welcome'


class SuicidalThoughtsReport(Screen):
    def __init__(self, **kwargs):
        super(SuicidalThoughtsReport, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, rows=1, spacing=10, padding=50)
        self.layout.add_widget(Label(
            text='You are not alone.\nPlease call one of these numbers right now.\n\nSuicide Hotline\n1-800-273-8255\n\nVeteran\'s Crisis Hotline\n1-800-273-8255, Press 1\n\nTransgender lifeline\n1-877-565-8860\n\nTrevor Lifeline (LGBTQ youth)\n1-866-488-7386\n\n',
            font_size=60))
        self.add_widget(self.layout)
        # No file made here, because the emergency is more important than the data.


class EmailPopup(Popup):
    def __init__(self, **kwargs):
        super(EmailPopup, self).__init__(**kwargs)
        self.title = 'Sign in to email your report.'
        self.layout = GridLayout(cols=2, rows=5, spacing=10, padding=50)
        self.layout.add_widget(Label(text='Please enter your email and password\nNote, this only works for gmail.', font_size=30))
        self.layout.add_widget(Label(text=''))
        self.add_widget(self.layout)
        self.layout.add_widget(Label(text='Email:'))
        self.email = TextInput(text='')
        self.layout.add_widget(self.email)
        self.layout.add_widget(Label(text='Password: ', font_size=30))
        self.password = TextInput(text='')
        self.password.password = True
        self.layout.add_widget(self.password)
        self.layout.add_widget(Button(text='Submit', on_press=self.submit))
        self.layout.add_widget(Button(text='No thanks', on_press=self.dismiss))

    def submit(self, instance):
        email = self.email.text
        password = self.password.text
        # Usually email_to would be the researching address. I guess for testing I'll use my public email.
        email_to = 'skilledapplegaming@gmail.com'
        print("(Debug) Email: " + email)
        report_handler.send_email(self, name, email, password, email_to)
        self.dismiss()


# email failed popup
class EmailFailedPopup(Popup):
    def __init__(self, **kwargs):
        super(EmailFailedPopup, self).__init__(**kwargs)
        self.title = 'Email failed!'
        self.layout = GridLayout(cols=1, rows=2, spacing=10, padding=50)
        self.layout.add_widget(Label(text='EMAIL FAILED TO SEND!\nDon\'t worry, just let your provider know and they will inform you on how to manually get it to them.', font_size=30))
        self.layout.add_widget(Button(text='OK', on_press=self.dismiss))
        self.add_widget(self.layout)


class WelcomeApp(App):
    def build(self):
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(PainReport(name='pain_report'))
        sm.add_widget(DrowsinessReport(name='drowsiness_report'))
        sm.add_widget(MentalHealthReport(name='mental_health_report'))
        sm.add_widget(SuicidalThoughtsReport(name='suicidal_thoughts_report'))
        return sm




if __name__ == '__main__':
    WelcomeApp().run()
