class Controller:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def uses_event(self, event):
        return False

    def update(self):
        pass

    @property
    def shoot(self):
        return False

    @property
    def ladder_up(self):
        return False

    @property
    def ladder_down(self):
        return False

    @property
    def left(self):
        return False

    @property
    def right(self):
        return False

    @property
    def jump(self):
        return False

    @property
    def double_jump(self):
        return False

    @property
    def dash_left(self):
        return False

    @property
    def dash_right(self):
        return False

    @property
    def yoyo(self):
        return False

    @property
    def start_up(self):
        return False

    @property
    def start_down(self):
        return False

    @property
    def start_enter(self):
        return False

    @property
    def start_back(self):
        return False

    @property
    def enter_door(self):
        return False

    @property
    def supress_yoyo_while_ladder_down(self):
        return True