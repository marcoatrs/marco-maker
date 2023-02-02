import pygame
import settings

from pygame.mouse import get_pressed, get_pos
from .menu_images import MenuImages
from .button import Button


class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_menu_space()
        self.create_buttons()
        self.menu_index = 0
        self.menu_images = MenuImages()
        self.selected_item = 0

    def create_menu_space(self):
        width = settings.MENU_COLS * settings.TILE_SIZE + (
            settings.MENU_MARGIN * (settings.MENU_COLS + 1))
        height = settings.MENU_ROWS * settings.TILE_SIZE + (
            settings.MENU_MARGIN * (settings.MENU_ROWS + 1))

        left = settings.WINDOW_WIDTH - width - settings.MENU_SPACING
        top = settings.WINDOW_HEIGHT // 2 - height // 2

        self.menu_surface = pygame.Surface((width, height))
        self.rect = self.menu_surface.get_rect()
        self.rect.topleft = (left, top)

    def create_buttons(self):
        self.buttons = pygame.sprite.Group()
        for row in range(settings.MENU_ROWS):
            for col in range(settings.MENU_COLS):
                idx = 2 * row + col
                left = self.rect.left + settings.MENU_MARGIN * (
                    col + 1) + col * settings.TILE_SIZE
                top = self.rect.top + settings.MENU_MARGIN * (
                    row + 1) + row * settings.TILE_SIZE
                Button(self.buttons, left, top, settings.TILE_SIZE,
                       settings.TILE_SIZE, idx)

    def draw_buttons(self):
        menu = settings.MENU_ITEMS[self.menu_index]
        images = self.menu_images(menu)
        self.buttons.update(images)
        self.buttons.draw(self.display_surface)
        self.highlight_selected()

    def highlight_selected(self):
        button: Button = list(self.buttons)[self.selected_item]
        rect = button.rect
        x = rect.left
        y = rect.top
        w = rect.width
        surface = button.image_surface
        surface.fill(settings.MENU_HL_COLOR)
        radius = w // 16
        center = x + radius // 2 + settings.MENU_MARGIN, y + \
            radius // 2 + settings.MENU_MARGIN
        pygame.draw.circle(self.display_surface, settings.MENU_BG, center,
                           radius)
        self.display_surface.blit(surface, (rect.topleft))

    def click(self, event: pygame.event.Event):
        if not get_pressed()[0]:
            return
        mouse = get_pos()
        for idx, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse):
                self.selected_item = idx
                return

    def update(self, event: pygame.event.Event):
        self.menu_surface.fill(settings.MENU_BG)
        self.display_surface.blit(self.menu_surface, self.rect.topleft)
        self.draw_buttons()