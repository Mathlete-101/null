from controller.controller import Controller


class MergedController(Controller):
    """A controller that merges the results of multiple controllers."""

    def __init__(self, controllers):
        super().__init__("merged")
        self.controllers = controllers

    @property
    def controller_type(self):
        if len(self.controllers) == 1:
            return self.controllers[0].controller_type
        else:
            return self._controller_type

    @controller_type.setter
    def controller_type(self, value):
        self._controller_type = value

    @property
    def types(self):
        return [c.types for c in self.controllers]

    @property
    def enter_door(self):
        """Returns whether the player is trying to enter a door."""
        return any(c.enter_door for c in self.controllers)

    def update(self):
        """Updates the merged controller."""
        for controller in self.controllers:
            controller.update()

    def add_event(self, event):
        """Adds an event to the merged controller."""
        for controller in self.controllers:
            if controller.uses_event(event):
                controller.add_event(event)

    def uses_event(self, event):
        """Returns whether the merged controller uses the given event."""
        for controller in self.controllers:
            if controller.uses_event(event):
                return True
        return False

    @property
    def shoot(self):
        for controller in self.controllers:
            if controller.shoot:
                return True
        return False

    @property
    def ladder_up(self):
        for controller in self.controllers:
            if controller.ladder_up:
                return True
        return False

    @property
    def ladder_down(self):
        """Returns whether the player is trying to climb down a ladder."""
        for controller in self.controllers:
            if controller.ladder_down:
                return True
        return False

    @property
    def left(self):
        """Returns whether the player is trying to move left."""
        for controller in self.controllers:
            if controller.left:
                return True
        return False

    @property
    def right(self):
        """Returns whether the player is trying to move right."""
        for controller in self.controllers:
            if controller.right:
                return True
        return False

    def clear(self):
        """Clears the merged controller."""
        for controller in self.controllers:
            controller.clear()

    @property
    def jump(self):
        """Returns whether the player is trying to jump."""
        for controller in self.controllers:
            if controller.jump:
                return True
        return False

    @property
    def double_jump(self):
        """Returns whether the player is trying to double jump."""
        for controller in self.controllers:
            if controller.double_jump:
                return True
        return False

    @property
    def dash_left(self):
        """Returns whether the player is trying to dash left."""
        for controller in self.controllers:
            if controller.dash_left:
                return True
        return False

    @property
    def dash_right(self):
        """Returns whether the player is trying to dash right."""
        for controller in self.controllers:
            if controller.dash_right:
                return True
        return False

    @property
    def yoyo(self):
        """Returns whether the player is trying to yoyo."""
        for controller in self.controllers:
            if controller.yoyo:
                return True
        return False

    @property
    def start_up(self):
        """Returns whether the player is trying to start the game."""
        for controller in self.controllers:
            if controller.start_up:
                return True
        return False

    @property
    def start_down(self):
        """Returns whether the player is trying to start the game."""
        for controller in self.controllers:
            if controller.start_down:
                return True
        return False

    @property
    def start_enter(self):
        """Returns whether the player is trying to start the game."""
        for controller in self.controllers:
            if controller.start_enter:
                return True
        return False

    @property
    def start_back(self):
        """Returns whether the player is trying to start the game."""
        for controller in self.controllers:
            if controller.start_back:
                return True
        return False

    @property
    def start_left(self):
        """Returns whether the player is trying to start the game."""
        for controller in self.controllers:
            if controller.start_left:
                return True
        return False

    @property
    def start_right(self):
        """Returns whether the player is trying to start the game."""
        for controller in self.controllers:
            if controller.start_right:
                return True
        return False

    def clear_movement_belt(self):
        """Clears the movement belt."""
        for controller in self.controllers:
            controller.clear_movement_belt()



