from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import threading
import time

class ColoredBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 25
        self.background_color = (0.05, 0.05, 0.1, 1)  # Dark background

class ExamTimerApp(App):
    def build(self):
        self.main_layout = ColoredBoxLayout()
        
        self.title_label = Label(text="Exam Timer", font_size=32, color=(1, 0.5, 0, 1), bold=True)
        self.main_layout.add_widget(self.title_label)
        
        self.info_label = Label(
            text="There is a 3-second head start before the timer starts.\n\nReading Time: 15 mins\nWriting Time: 3 hours (Normal) & 2 hours (Computer)",
            font_size=18, color=(1, 1, 0, 1))
        self.main_layout.add_widget(self.info_label)
        self.main_layout.add_widget(Label(size_hint_y=None, height=20))  # Spacer to add more space before buttons
        
        self.exam_choice_layout = BoxLayout(orientation='horizontal', spacing=20)
        self.normal_exam_button = Button(text="Normal Exam", background_color=(0, 0.7, 1, 1), font_size=18, color=(1,1,1,1), bold=True, on_press=self.set_normal_exam)
        self.computer_exam_button = Button(text="Computer Exam", background_color=(1, 0.4, 0, 1), font_size=18, color=(1,1,1,1), bold=True, on_press=self.set_computer_exam)
        
        self.exam_choice_layout.add_widget(self.normal_exam_button)
        self.exam_choice_layout.add_widget(self.computer_exam_button)
        self.main_layout.add_widget(self.exam_choice_layout)
        
        self.countdown_label = Label(text="", font_size=50, color=(1, 1, 1, 1))
        self.main_layout.add_widget(self.countdown_label)
        
        self.timer_label = Label(text="00:00:00", font_size=48, color=(0, 1, 0.5, 1), bold=True)
        self.main_layout.add_widget(self.timer_label)
        
        self.status_label = Label(text="", font_size=22, color=(1, 0.8, 0, 1))
        self.main_layout.add_widget(self.status_label)
        
        self.start_button = Button(text="Start", background_color=(0, 1, 0, 1), font_size=20, color=(0,0,0,1), bold=True, on_press=self.start_timer, disabled=True, opacity=0)
        self.main_layout.add_widget(self.start_button)
        
        self.pause_button = Button(text="Pause", background_color=(1, 0, 0, 1), font_size=20, color=(1,1,1,1), bold=True, on_press=self.toggle_pause, disabled=True, opacity=0)
        self.main_layout.add_widget(self.pause_button)
        
        self.total_seconds = 15 * 60
        self.long_timer_seconds = 0
        self.paused = False
        self.remaining_time = 0
        self.running = False
        
        self.sound = SoundLoader.load("alarm.mp3")
        
        return self.main_layout
    
    def start_timer(self, instance):
        self.start_button.disabled = True
        self.start_button.opacity = 0
        self.status_label.text = "Reading Time"
        self.remaining_time = self.total_seconds
        self.running = True
        self.start_countdown()
    
    def start_countdown(self, count=3):
        if count > 0:
            self.countdown_label.text = str(count)
            Clock.schedule_once(lambda dt: self.start_countdown(count - 1), 1)
        else:
            self.countdown_label.text = ""
            if self.sound:
                self.sound.play()
            self.run_timer(self.remaining_time, long_timer=False)
    
    def run_timer(self, seconds, long_timer=False):
        if seconds > 0 and not self.paused:
            minutes, sec = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            self.timer_label.text = f"{hours:02}:{minutes:02}:{sec:02}"
            Clock.schedule_once(lambda dt: self.run_timer(seconds - 1, long_timer), 1)
        else:
            if self.sound:
                self.sound.play()
            if not long_timer:
                self.start_writing_time()
            else:
                self.show_time_over_screen()
    
    def start_writing_time(self):
        self.status_label.text = "Writing Time"
        self.run_timer(self.long_timer_seconds, long_timer=True)
    
    def toggle_pause(self, instance):
        if not self.running:
            return
        self.paused = not self.paused
        self.pause_button.text = "Resume" if self.paused else "Pause"
        if not self.paused:
            self.run_timer(self.remaining_time, True)
    
    def set_normal_exam(self, instance):
        self.long_timer_seconds = 3 * 60 * 60
        self.start_button.disabled = False
        self.start_button.opacity = 1
        self.exam_choice_layout.opacity = 0
    
    def set_computer_exam(self, instance):
        self.long_timer_seconds = 2 * 60 * 60
        self.start_button.disabled = False
        self.start_button.opacity = 1
        self.exam_choice_layout.opacity = 0
    
    def show_time_over_screen(self):
        self.status_label.text = "!!TIME OVER!!"
        self.timer_label.text = "00:00:00"
        self.pause_button.disabled = True
        self.pause_button.opacity = 0
    
if __name__ == "__main__":
    ExamTimerApp().run()
