from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty, StringProperty
from datetime import datetime, timedelta


def minutes_since_midnight(dt: datetime):
    return dt.hour * 60 + dt.minute


class Activity(BoxLayout):
    start_time = NumericProperty()
    duration = NumericProperty()
    name = StringProperty()

    def __init__(self, start_time, duration, name, timeline, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=40, **kwargs)
        self.start_time = start_time
        self.duration = duration
        self.name = name
        self.timeline = timeline

        self.lbl = Label(text=self.display_text())
        self.add_widget(self.lbl)

        finish_btn = Button(text="Finish")
        finish_btn.bind(on_release=self.finish_activity)
        self.add_widget(finish_btn)

    def time_to_string(self, mins):
        return f"{mins // 60:02d}:{mins % 60:02d}"

    def display_text(self):
        start = self.time_to_string(self.start_time)
        end = self.time_to_string(self.start_time + self.duration)
        return f"{self.name}: {start}–{end}"

    def finish_activity(self, instance):
        now = datetime.now()
        actual_finish = minutes_since_midnight(now)

        scheduled_finish = self.start_time + self.duration
        diff = actual_finish - scheduled_finish  # +late, -early

        # Update this activity's duration
        self.duration = actual_finish - self.start_time
        self.lbl.text = self.display_text()

        # Shift everything after it
        if diff != 0:
            self.timeline.shift_after(self, diff)


class Timeline(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.activities = []
        self.current_time = minutes_since_midnight(datetime.now())

    def add_activity(self, name, duration):
        act = Activity(self.current_time, duration, name, self)
        self.activities.append(act)
        self.add_widget(act)
        self.current_time += duration

    def shift_after(self, activity, diff):
        found = False
        for act in self.activities:
            if act == activity:
                found = True
                continue

            if found:  # affects all later activities
                act.start_time += diff
                act.lbl.text = act.display_text()

        self.current_time += diff


class MainUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.timeline = Timeline()

        top = BoxLayout(size_hint_y=None, height=50)
        self.add_widget(top)

        self.name_input = TextInput(hint_text="Activity name")
        self.duration_input = TextInput(hint_text="Minutes", input_filter="int")
        add_btn = Button(text="Add Activity", size_hint_x=0.3)
        add_btn.bind(on_release=self.add_activity)

        top.add_widget(self.name_input)
        top.add_widget(self.duration_input)
        top.add_widget(add_btn)

        scroll = ScrollView()
        scroll.add_widget(self.timeline)
        self.add_widget(scroll)

    def add_activity(self, instance):
        name = self.name_input.text.strip() or "Activity"
        try:
            duration = int(self.duration_input.text)
        except:
            duration = 30  # default duration

        self.timeline.add_activity(name, duration)
        self.name_input.text = ""
        self.duration_input.text = ""


class CalendarApp(App):
    def build(self):
        return MainUI()


if __name__ == "__main__":
    CalendarApp().run()
