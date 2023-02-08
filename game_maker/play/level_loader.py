import json
import typing

import pygame as pg
import settings
from pygame.image import load as load_image

if typing.TYPE_CHECKING:
    from .level import Level

from assets_loader import Asset

from .animated_player import AnimatedPlayer
from .animated_tile import AnimatedLevelTile
from .player import Player
from .tile import LevelTile


class LevelLoader:
    def __init__(self):
        self.display_surface = pg.display.get_surface()

    def __call__(self, level: 'Level', canvas: dict[tuple[int, int], str], assets: dict) -> Player:
        player = None
        for loc, path in canvas.items():
            menu, name, state = path.split('-')
            images = assets[menu][name]

            x = loc[0] * settings.TILE_SIZE
            y = loc[1] * settings.TILE_SIZE

            # Search Player
            if 'player' in path:
                groups = [level.draw_sprites, level.update_sprites]
                player = AnimatedPlayer(
                    images, (x, y), groups, level.collision_sprites)
                continue

            _meta = assets[menu]['metadata']

            if state in _meta.get(name, {}).get('animated', []):
                # Animated Tile
                groups = [level.draw_sprites,
                          level.update_sprites, level.collision_sprites]
                AnimatedLevelTile(images, (x, y), groups)
                continue

            image = assets[menu][name][state][0]
            groups = [level.draw_sprites, level.collision_sprites]
            LevelTile(image, (x, y), groups)

        return player
