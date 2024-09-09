from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from navbar import NavBar
from table_display import DisplayDocs


class MyApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")

        nav_section = NavBar(size_hint=(1, 0.2))
        display_doc = DisplayDocs(size_hint=(1, 0.8))

        main_layout.add_widget(nav_section)
        main_layout.add_widget(display_doc)

        return main_layout


if __name__ == "__main__":
    MyApp().run()
