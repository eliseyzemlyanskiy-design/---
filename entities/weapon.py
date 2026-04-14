# -*- coding: utf-8 -*-

WEAPON_AUTO = 0
WEAPON_SHOTGUN = 1
WEAPON_GRENADE = 2


def damage_for(weapon: int, dark_mode: bool) -> int:
    if weapon == WEAPON_AUTO:
        d = 50
    elif weapon == WEAPON_SHOTGUN:
        d = 20
    elif weapon == WEAPON_GRENADE:
        d = 100
    else:
        d = 50
    return d * 2 if dark_mode else d
