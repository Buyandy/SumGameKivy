from kivy.animation import Animation
from kivy.app import App
from kivy.uix.label import Label 
from kivy.uix.button import Button 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from random import randint


Builder.load_file("my.kv")



class MyAnimations:
    @staticmethod
    def error(object: Label):
        anima = Animation(x=50+object.pos[0], duration=0) + Animation(x=0+object.pos[0], duration=0.5, t="out_elastic")
        anima &= Animation(color=(1,0,0,1), d=0) + Animation(color=(1,1,1,1), d=0.5)
        anima.start(object)


    @staticmethod
    def success(object: Label):
        anima = Animation(color=(0,1,0,1), d=0) + Animation(color=(1,1,1,1), d=0.5)
        anima.start(object)
                


    @staticmethod
    def flow(object):
        pos = object.pos
        anima = Animation(y=-10+pos[1], duration=2.5, t="in_out_cubic") + Animation(y=10+pos[1], duration=2.5, t="in_out_cubic")
        anima.repeat = True
        anima.start(object)


# function
class UpBox(BoxLayout):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.label = Label(text="0 + 0 = ?")
        self.label.font_size = 60

        self.add_widget(self.label)


    def generate(self, max_num: int) -> int:
        a: int = randint(1, max_num)
        b: int = randint(1, max_num)
        self.label.text = f"{a} + {b} = ?"
        return a + b



class DownBox(BoxLayout):
    def __init__(self, max_buttons: int, func_check, **kwarg):
        super().__init__(**kwarg)

        self.max_buttons = max_buttons
        self.func_check = func_check
        self.uid_button: dict = {}

        self.orientation = "horizontal"
        self.size_hint = (1.0, 0.8)
        

        self.buttons: list[Button] = []

        for i in range(self.max_buttons):
            widget_for_button = BoxLayout()
            widget_for_button.padding = (10, 10, 10, 10)

            button = Button(text="0")
            
            self.uid_button[button] = None
            self.buttons.append(button)
            widget_for_button.add_widget(button)
            self.add_widget(widget_for_button)
        

    def cbind(self, button: Button, func, *args, **kwargs):
        if self.uid_button[button]:
            button.unbind_uid("on_release", self.uid_button[button])
        self.uid_button[button] = button.fbind("on_release", func, *args, **kwargs)



    def generate(self, right_num: int, max_num: int):
        right_button = randint(0, self.max_buttons-1)
        n = -1
        for button in self.buttons:
            n += 1
            if n == right_button:
                button.text = str(right_num)
            else:
                button.text = str(randint(2, max_num*2))
            
            self.cbind(button, self.func_check, num=int(button.text))

            





class MainBox(BoxLayout):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

        self.orientation = "vertical"
        self.max_buttons = 5
        self.max_num = 100
        
        self.up_box = UpBox()
        self.right_num = self.up_box.generate(max_num=self.max_num)
        self.add_widget(self.up_box)

        self.down_box = DownBox(max_buttons=self.max_buttons, func_check=self.check)
        self.down_box.generate(right_num=self.right_num, max_num=self.max_num)
        self.add_widget(self.down_box)

        # Animations
    #        MyAnimations.flow(self.up_box)



    def check(self, *args, **kwargs):
        if self.right_num == kwargs["num"]:
            self.right_num = self.up_box.generate(max_num=self.max_num)
            self.down_box.generate(right_num=self.right_num, max_num=self.max_num)
            MyAnimations.success(self.up_box.label)
        else:
            MyAnimations.error(self.up_box.label)


class MyApp(App):
    def build(self):
        main_box = MainBox()
        return main_box


if __name__ == "__main__":
    MyApp().run()
