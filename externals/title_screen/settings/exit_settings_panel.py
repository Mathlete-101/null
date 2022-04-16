from externals.title_screen.settings.settings_panel import SettingsPanel


class ExitSettingsPanel(SettingsPanel):
    @property
    def exit(self):
        return True
