import pygame.sprite

from externals.title_screen.selector import Selector
from externals.title_screen.settings.controller_settings_panel import ControllerSettingsPanel
from externals.title_screen.settings.exit_settings_panel import ExitSettingsPanel
from externals.title_screen.settings.gameplay_settings_panel import GameplaySettingsPanel
from externals.title_screen.settings.settings_panel import SettingsPanel
from externals.title_screen.settings.volume_settings_panel import VolumeSettingsPanel
from sound import sounds
from tools import duple

class Settings(pygame.sprite.Group):
    def __init__(self, dim, controller):
        super().__init__()
        self.state = 0
        self.controller = controller
        self.sp = duple.ScreenPosition(dim)
        self.setting_selector = Selector(["Volume", "Controllers", "Gameplay", "Back"], self.sp((0.02, 0.05)), controller, alignment="left", spacing=100)
        self.add(self.setting_selector)
        self.panels = [VolumeSettingsPanel(dim, controller), ControllerSettingsPanel(dim, controller), GameplaySettingsPanel(dim, controller), ExitSettingsPanel(dim, controller)]
        self.initialized = False

    def reset_panel(self):
        self.empty()
        self.add(self.setting_selector)

    @property
    def current_panel(self):
        return self.panels[self.setting_selector.currently_selected_number]

    def update(self):
        if not self.initialized:
            for panel in self.panels:
                panel.update()
            self.initialized = True

        if self.state == 0:
            if self.setting_selector.update() in [0, 1]:
                self.reset_panel()
                self.add(self.current_panel)
            if self.controller.start_enter:
                if self.current_panel.exit:
                    return True
                else:
                    self.current_panel.active = True
                    self.setting_selector.active = False
                    self.state = 1
            elif self.controller.start_back:
                return True
        elif self.state == 1:
            if self.current_panel.update() or self.controller.start_back:
                self.current_panel.active = False
                self.setting_selector.active = True
                self.state = 0
                sounds.play_sound("select")
        return False
