import settings
import json
from menu.tile_surface import TileSurface
from pygame.image import load


def read_metadata(path) -> dict:
    with open(path, 'r') as json_file:
        json_dict = json.load(json_file)
    return json_dict


class MenuImages:
    def __init__(self):
        self.menu_images: dict[str, dict] = {}
        self.load_images()

    def load_images(self):
        for menu in settings.MENU_ITEMS:
            path = settings.TILES_PATH / menu
            if not menu in self.menu_images:
                self.menu_images[menu]: dict = {}
            metataba_path = path / f'{menu}.json'
            metadata = read_metadata(
                metataba_path) if metataba_path.exists() else {}
            for file in path.rglob('*.png'):
                image_name = file.stem.split('-')
                if len(image_name) > 1:
                    name, place = image_name
                else:
                    name = image_name[0]
                    place = 'top'
                if not name in self.menu_images[menu]:
                    self.menu_images[menu][name] = {}
                self.menu_images[menu][name][place] = TileSurface(
                    load(str(file)), f"{menu}-{name}-{place}", metadata.get(name, {}))

    def __call__(self, menu: str, alt: bool = False) -> list:
        if not menu in self.menu_images:
            return []
        images: dict = self.menu_images[menu]
        images_list = list()
        for value in images.values():
            if 'top' in value:
                images_list.append(value['top'])
            elif 'middle' in value:
                images_list.append(value['middle'])
            elif 'bottom' in value:
                images_list.append(value['bottom'])
            elif 'unique' in value:
                images_list.append(value['unique'])
        return images_list