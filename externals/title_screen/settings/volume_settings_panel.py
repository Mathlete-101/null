from engine.settings import settings
from externals.title_screen.settings.button import Button
from externals.title_screen.settings.settings_panel import SettingsPanel
from externals.title_screen.settings.slider import Slider
from misc.wrapped_sprite import WrappedSprite
from sound import sounds
from tools.duple import ScreenPosition
from tools.text import render_font_cool as Text


class VolumeSettingsPanel(SettingsPanel):
    def __init__(self, dim, controller):
        super().__init__(dim, controller)
        self.dim = dim
        self.controller = controller

        self.master_text = WrappedSprite(Text("Master Volume"), self.sp((0.34, 0.13)))
        self.add(self.master_text)
        self.master_slider = Slider(500, 10, self.sp((0.3, 0.2)), int(settings.get(["sound", "volume", "master"]) * 10),
                                    "100%", "0%")
        self.add_settings_item(self.master_slider, "master")

        self.music_text = WrappedSprite(Text("Music Volume"), self.sp((0.34, 0.28)))
        self.add(self.music_text)
        self.music_slider = Slider(500, 10, self.sp((0.3, 0.35)), int(settings.get(["sound", "volume", "music"]) * 10),
                                   "100%", "0%")
        self.add_settings_item(self.music_slider, "music")

        self.sfx_text = WrappedSprite(Text("SFX Volume"), self.sp((0.34, 0.43)))
        self.add(self.sfx_text)
        self.sfx_slider = Slider(500, 10, self.sp((0.3, 0.5)), int(settings.get(["sound", "volume", "sfx"]) * 10),
                                 "100%", "0%")
        self.add_settings_item(self.sfx_slider, "sfx")

        self.back_button = Button("Back", self.sp((0.3, 0.8)), "back")
        self.add_settings_item(self.back_button, "back")

    def on_item_click(self, result):
        if result == "back":
            return True
        else:
            settings.set(["sound", "volume", self.selected_item_name], self.selected_item.val / 10)
            sounds.update_volume()
