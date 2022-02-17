import os.path

import pygame

from graphics import graphics
import tools
from graphics.graphic_class.animation_graphic import AnimationGraphic
from graphics.graphic_class.graphic import Graphic
from graphics.graphic_class.reflection_graphic import ReflectionGraphic
from graphics.graphic_class.rotation_graphic import RotationGraphic
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

    # Darken them up a bit. This will pull in some other stuff, but it's fine and actually beneficial
    darker = pygame.Surface((42, 42))
    darker.fill(pygame.Color(0, 0, 0))
    darker.set_alpha(100)
    darker.convert_alpha()
    darker_wires = [[energy_parts[i][j].copy() for j in range(0, 5)] for i in range(0, 3)]
    for row in darker_wires:
        for wire in row:
            wire.blit(darker, (0, 0))

    # Add graphics for the darker wires
    graphics.add(RotationSwitchGraphic(darker_wires[1][1], darker_wires[2][1]), "energy_wire_through_dark")
    graphics.add(RotationSwitchGraphic(darker_wires[1][2], darker_wires[2][2]), "energy_wire_turn_dark")
    graphics.add(RotationSwitchGraphic(darker_wires[1][3], darker_wires[2][3]), "energy_wire_t_junction_dark")
    graphics.add(RotationSwitchGraphic(darker_wires[1][4], darker_wires[2][4]), "energy_wire_cross_junction_dark")

    graphics.add(RotationReflectionSectionalSwitchGraphic(energy_parts[2][5], energy_parts[1][5], [
        cp_section(energy_parts[2][5], (14, 34, 10, 8)),
        cp_section(energy_parts[2][5], (8, 32, 30, 6)),
        cp_section(energy_parts[2][5], (8, 26, 30, 6)),
        cp_section(energy_parts[2][5], (8, 20, 30, 6)),
        cp_section(energy_parts[2][5], (8, 14, 30, 6)),
        cp_section(energy_parts[2][5], (8, 8, 30, 6)),
        cp_section(energy_parts[2][5], (8, 0, 30, 8))
    ]), "energy_delay")

    transistor_graphic = RotationReflectionSectionalSwitchGraphic(energy_parts[1][7], energy_parts[2][7], [
        cp_section(energy_parts[2][7], (0, 14, 16, 14)),
        cp_section(energy_parts[2][7], (16, 14, 10, 16)),
        cp_section(energy_parts[2][7], (26, 14, 16, 14)),
        cp_section(energy_parts[4][7], (16, 24, 14, 18)),
        cp_section(energy_parts[4][7], (16, 14, 10, 12))
    ])
    graphics.add(transistor_graphic, "energy_transistor")

    graphics.add(RotationSwitchGraphic(energy_parts[1][6], energy_parts[2][6]), "energy_force_field")

    graphics.add(RotationGraphic(energy_parts[0][5]), "force_field")
