from engine.settings import settings
from externals.title_screen.settings.button import Button
from externals.title_screen.settings.settings_panel import SettingsPanel
from externals.title_screen.settings.switch import Switch
from tools.duple import ScreenPosition


class GameplaySettingsPanel(SettingsPanel):
    def __init__(self, dim, controller):
        super().__init__(dim, controller)
        self.assistive_signs_switch = Switch((self.sp((0.3, 0.3))), "Assistive signs", settings.get("assistive_signs"))
        self.add_settings_item(self.assistive_signs_switch, "assistive_signs")
        self.back_button = Button("Back", self.sp((0.3, 0.8)), "back")
        self.add_settings_item(self.back_button)

    def on_item_click(self, result):
        if self.selected_item_name == "assistive_signs":
            settings.set("assistive_signs", self.assistive_signs_switch.val)
        if result == "back":
            return True
        return False
