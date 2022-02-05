import os.path

import pygame

from graphics import graphics
import tools
from graphics.graphic_class.animation_graphic import AnimationGraphic
from graphics.graphic_class.graphic import Graphic
from graphics.graphic_class.reflection_graphic import ReflectionGraphic
from graphics.graphic_class.rotation_reflection_sectional_switch_graphic import RotationReflectionSectionalSwitchGraphic
from graphics.graphic_class.rotation_switch_graphic import RotationSwitchGraphic
from tools.transform import get_clear_surface, cp_section


def assemble():
    energy_parts = (tools.transform.split_sheet(
        pygame.image.load(os.path.join("resources", "images", "blocks", "energy_parts.png"))
    ))

    graphics.add(AnimationGraphic(energy_parts[0][0:5]), "energy_sphere_decreasing_animation")
    graphics.add(AnimationGraphic([energy_parts[0][0]]), "energy_sphere_static_animation")
    graphics.add(Graphic(energy_parts[0][0]), "energy_sphere")

    graphics.add(RotationSwitchGraphic(energy_parts[1][0], energy_parts[2][0]), "energy_receiver_time")
    graphics.add(RotationSwitchGraphic(energy_parts[3][0], energy_parts[4][0]), "energy_receiver_toggle")

    graphics.add(RotationSwitchGraphic(energy_parts[1][1], energy_parts[2][1]), "energy_wire_through")
    graphics.add(RotationSwitchGraphic(energy_parts[1][2], energy_parts[2][2]), "energy_wire_turn")
    graphics.add(RotationSwitchGraphic(energy_parts[1][3], energy_parts[2][3]), "energy_wire_t_junction")
    graphics.add(RotationSwitchGraphic(energy_parts[1][4], energy_parts[2][4]), "energy_wire_cross_junction")

    graphics.add(RotationReflectionSectionalSwitchGraphic(energy_parts[2][5], energy_parts[1][5], [
        cp_section(energy_parts[2][5], (7, 17, 5, 4)),
        cp_section(energy_parts[2][5], (4, 16, 15, 3)),
        cp_section(energy_parts[2][5], (4, 13, 15, 3)),
        cp_section(energy_parts[2][5], (4, 10, 15, 3)),
        cp_section(energy_parts[2][5], (4, 7, 15, 3)),
        cp_section(energy_parts[2][5], (4, 4, 15, 3)),
        cp_section(energy_parts[2][5], (4, 0, 15, 4))
    ]), "energy_delay")

    transistor_graphic = RotationReflectionSectionalSwitchGraphic(energy_parts[1][7], energy_parts[2][7], [
        cp_section(energy_parts[2][7], (0, 7, 8, 7)),
        cp_section(energy_parts[2][7], (8, 7, 5, 6)),
        cp_section(energy_parts[2][7], (13, 7, 8, 7)),
        cp_section(energy_parts[4][7], (8, 12, 7, 9)),
        cp_section(energy_parts[4][7], (8, 7, 5, 6))
    ])
    graphics.add(transistor_graphic, "energy_transistor")
