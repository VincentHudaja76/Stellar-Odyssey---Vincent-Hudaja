# Stellar Odyssey
# Created by Vincent Hudaja

# Imports
import pygame
import sys
import math
import random
from pygame import mixer

# Imports from other created modules
from auth import register_user, authenticate_user, validate_credentials
from save_load import save_user_inventory, load_user_inventory
from factfile_data import factfile_data
from surface_feature_data import surface_feature_data
from feature_facts_data import feature_facts_data

# Initialise pygame and set up game assets
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stellar Odyssey")

WORLD_WIDTH, WORLD_HEIGHT = 7000, 7000

# Sounds
mixer.music.load('music/spacebg_music.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.5)

button_click_sound = pygame.mixer.Sound("music/button_click.mp3")
button_click_sound.set_volume(0.7)
item_collect_sound = pygame.mixer.Sound("music/item_collect.mp3")

# Function to play button click sound
def play_button_click():
    button_click_sound.play()

# Function to play item collect sound
def play_item_collect():
    item_collect_sound.play()

bg_tile = pygame.image.load("space_bg.png").convert()
bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width() * 2, bg_tile.get_height() * 2))
bg_tile_width = bg_tile.get_width()
bg_tile_height = bg_tile.get_height()
solar_system_button = pygame.image.load("buttons/solar_system_button.png").convert_alpha()
solar_system_button_hover = pygame.image.load("buttons/solar_system_button_hover.png").convert_alpha()
solar_system_button_rect = solar_system_button.get_rect(topleft=(30, 30))

bg_image = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
for x in range(0, WORLD_WIDTH, bg_tile_width):
    for y in range(0, WORLD_HEIGHT, bg_tile_height):
        bg_image.blit(bg_tile, (x, y))

# Fonts
font_path = "fonts/stellar.otf"
font_path2 = "fonts/audiowide.ttf"

default_font = pygame.font.Font(font_path2, 30)
title_font = pygame.font.Font(font_path, 100)
label_font = pygame.font.Font(font_path2, 26)
factfile_name_font = pygame.font.Font(font_path, 80)
factfile_content_font = pygame.font.Font(font_path2, 30)
surface_label_font = pygame.font.Font(font_path2, 26)
hover_instruction_font = pygame.font.Font(font_path2, 28)

# Player Setup
player_size = (72, 72)
player_default = pygame.transform.scale(pygame.image.load("player_graphics/player.png").convert_alpha(), player_size)
player_images = {
    "up": pygame.transform.scale(pygame.image.load("player_graphics/player_up.png").convert_alpha(), player_size),
    "down": pygame.transform.scale(pygame.image.load("player_graphics/player_down.png").convert_alpha(), player_size),
    "left": pygame.transform.scale(pygame.image.load("player_graphics/player_left.png").convert_alpha(), player_size),
    "right": pygame.transform.scale(pygame.image.load("player_graphics/player_right.png").convert_alpha(), player_size),
}
player_image = player_default

# Sun Setup
sun_center = (WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
sun_size = (512, 512)
sun_image = pygame.transform.scale(pygame.image.load("game_graphics/sun.png").convert_alpha(), sun_size)
sun_default_image = sun_image.copy()
sun_draw_pos = (sun_center[0] - sun_size[0] // 2, sun_center[1] - sun_size[1] // 2)

arrow_image = pygame.image.load("game_graphics/arrow.png").convert_alpha()
arrow_image = pygame.transform.scale(arrow_image, (40, 40))
game_menu_button = pygame.image.load("buttons/game_menu.png").convert_alpha()
game_menu_button_hover = pygame.image.load("buttons/game_menu_hover.png").convert_alpha()
game_menu_button = pygame.transform.scale(game_menu_button, (100, 100))
game_menu_button_hover = pygame.transform.scale(game_menu_button_hover, (100, 100))
game_menu_button_rect = game_menu_button.get_rect(topright=(WIDTH - 30, 30))
in_menu = False

# Menu Buttons Setup
raw_play_button = pygame.image.load("buttons/play_button.png").convert_alpha()
raw_play_button_hover = pygame.image.load("buttons/play_button_hover.png").convert_alpha()

target_width = 300
aspect_ratio = raw_play_button.get_height() / raw_play_button.get_width()
target_height = int(target_width * aspect_ratio)

play_button = pygame.transform.scale(raw_play_button, (target_width, target_height))
play_button_hover = pygame.transform.scale(raw_play_button_hover, (target_width, target_height))

play_button_rect = play_button.get_rect(midtop=(WIDTH // 2, int(HEIGHT // 2 + 5)))

raw_login_button = pygame.image.load("buttons/login_button.png").convert_alpha()
raw_login_button_hover = pygame.image.load("buttons/login_button_hover.png").convert_alpha()
login_button = pygame.transform.scale(raw_login_button, (target_width, target_height))
login_button_hover = pygame.transform.scale(raw_login_button_hover, (target_width, target_height))
login_button_rect = login_button.get_rect(midtop=(WIDTH // 2, play_button_rect.bottom + 20))

sign_in_button = pygame.transform.scale(pygame.image.load("buttons/sign_in_button.png").convert_alpha(), (target_width, target_height))
sign_in_button_hover = pygame.transform.scale(pygame.image.load("buttons/sign_in_button_hover.png").convert_alpha(), (target_width, target_height))
sign_up_button = pygame.transform.scale(pygame.image.load("buttons/sign_up_button.png").convert_alpha(), (target_width, target_height))
sign_up_button_hover = pygame.transform.scale(pygame.image.load("buttons/sign_up_button_hover.png").convert_alpha(), (target_width, target_height))

button_y = HEIGHT // 2 + 140
sign_in_button_rect = sign_in_button.get_rect(midtop=(WIDTH // 2, button_y))
sign_up_button_rect = sign_up_button.get_rect(midtop=(WIDTH // 2, button_y))

raw_help_button = pygame.image.load("buttons/help_button.png").convert_alpha()
raw_help_button_hover = pygame.image.load("buttons/help_button_hover.png").convert_alpha()
help_button = pygame.transform.scale(raw_help_button, (target_width, target_height))
help_button_hover = pygame.transform.scale(raw_help_button_hover, (target_width, target_height))
help_button_rect = help_button.get_rect(midtop=(WIDTH // 2, login_button_rect.bottom + 20))

return_menu_button_size = (100, 100)

return_menu_button = pygame.transform.scale(
    pygame.image.load("buttons/return_menu.png").convert_alpha(), return_menu_button_size
)
return_menu_button_hover = pygame.transform.scale(
    pygame.image.load("buttons/return_menu_hover.png").convert_alpha(), return_menu_button_size
)
return_menu_button_rect = return_menu_button.get_rect(bottomleft=(30, HEIGHT - 30))

close_button = pygame.image.load("buttons/close_button.png").convert_alpha()
close_button_hover = pygame.image.load("buttons/close_button_hover.png").convert_alpha()
close_button = pygame.transform.scale(close_button, (100, 100))
close_button_hover = pygame.transform.scale(close_button_hover, (100, 100))
close_button_rect = close_button.get_rect(topright=(WIDTH - 30, 30))

eye_icon = pygame.image.load("buttons/eye_icon.png").convert_alpha()
eye_icon = pygame.transform.scale(eye_icon, (40, 40))
eye_closed_icon = pygame.image.load("buttons/eye_closed_icon.png").convert_alpha()
eye_closed_icon = pygame.transform.scale(eye_closed_icon, (40, 40))

sign_out_button = pygame.transform.scale(
    pygame.image.load("buttons/sign_out.png").convert_alpha(), (target_width / 1.5, target_height / 1.5)
)
sign_out_button_hover = pygame.transform.scale(
    pygame.image.load("buttons/sign_out_hover.png").convert_alpha(), (target_width / 1.5, target_height / 1.5)
)
sign_out_button_rect = sign_out_button.get_rect(topleft=(20, 80))

button_size = (100, 100)
solar_system_button = pygame.transform.scale(
    pygame.image.load("buttons/solar_system_button.png").convert_alpha(), button_size
)
solar_system_button_hover = pygame.transform.scale(
    pygame.image.load("buttons/solar_system_button_hover.png").convert_alpha(), button_size
)
solar_system_button_rect = solar_system_button.get_rect(topleft=(30, 30))

inventory_button = pygame.transform.scale(
    pygame.image.load("buttons/inventory_button.png").convert_alpha(), (100, 100)
)
inventory_button_hover = pygame.transform.scale(
    pygame.image.load("buttons/inventory_button_hover.png").convert_alpha(), (100, 100)
)
inventory_button_rect = inventory_button.get_rect(bottomright=(WIDTH - 30, HEIGHT - 30))

plasma_img = pygame.image.load("inventory_items/plasma.png").convert_alpha()
plasma_touch_img = pygame.image.load("inventory_items/plasma_touch.png").convert_alpha()
plasma_rect = plasma_img.get_rect(topleft=(600, 150))

arrows_on_img = pygame.transform.scale(pygame.image.load("buttons/arrows_on.png").convert_alpha(), (50, 50))
arrows_off_img = pygame.transform.scale(pygame.image.load("buttons/arrows_off.png").convert_alpha(), (50, 50))
arrows_button_rect = arrows_on_img.get_rect(topright=(WIDTH - 610, 155))

# Load surface images
surface_images = {
    "Sun": pygame.image.load("surfaces/sun_surface.png").convert(),
    "Mercury": pygame.image.load("surfaces/mercury_surface.png").convert(),
    "Venus": pygame.image.load("surfaces/venus_surface.png").convert(),
    "Earth": pygame.image.load("surfaces/earth_surface.png").convert(),
    "Mars": pygame.image.load("surfaces/mars_surface.png").convert(),
    "Jupiter": pygame.image.load("surfaces/jupiter_surface.png").convert(),
    "Saturn": pygame.image.load("surfaces/saturn_surface.png").convert(),
    "Uranus": pygame.image.load("surfaces/uranus_surface.png").convert(),
    "Neptune": pygame.image.load("surfaces/neptune_surface.png").convert(),
    "Pluto": pygame.image.load("surfaces/pluto_surface.png").convert()
}

"""Stellar Odyssey - Classes"""

# SurfaceFeatureSet Class
class SurfaceFeatureSet:
    # Initialise SurfaceFeatureSet with list of features
    def __init__(self, features):
        self.features = []
        for feature in features: # Load each feature's normal and touch images
            normal_img = pygame.image.load(f"game_graphics/surface_graphics/{feature['name']}.png").convert_alpha()
            touch_img = pygame.image.load(f"game_graphics/surface_graphics/{feature['name']}_touch.png").convert_alpha()
            rect = normal_img.get_rect(topleft=feature["pos"])
            self.features.append({
                "name": feature["name"],
                "image": normal_img,
                "touch_image": touch_img,
                "rect": rect,
                "hovered": False
            })
        self.current_hovered_feature = None

    # Draw all features on screen, highlighting hovered feature
    def draw(self, screen, player_rect, mouse_pos):
        self.current_hovered_feature = None
        for feature in self.features: # Iterate through each feature
            is_touching = player_rect.colliderect(feature["rect"])
            is_hovering = feature["rect"].collidepoint(mouse_pos)
            feature["hovered"] = is_touching or is_hovering

            current_img = feature["touch_image"] if feature["hovered"] else feature["image"]
            screen.blit(current_img, feature["rect"].topleft)

            if feature["hovered"]: # If feature is hovered or touched, display its label
                self.current_hovered_feature = feature
                display_name = feature["name"].replace("_", " ").title()
                label = surface_label_font.render(display_name, True, (255, 255, 255))
                label_rect = label.get_rect(midbottom=(feature["rect"].centerx, feature["rect"].top - 10))

                padding = 8
                bg_rect = pygame.Rect(
                    label_rect.left - padding,
                    label_rect.top - padding,
                    label_rect.width + 2 * padding,
                    label_rect.height + 2 * padding
                )
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, 160))
                screen.blit(bg_surface, (bg_rect.left, bg_rect.top))

                screen.blit(label, label_rect)

    # Handle mouse events for features
    def get_hovered_feature(self):
        return self.current_hovered_feature

# InputBox Class
class InputBox:
    # Initialise InputBox with position, size, font and password mode
    def __init__(self, x, y, w, h, font, is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.color_inactive = pygame.Color('white')
        self.color_active = pygame.Color('deepskyblue')
        self.color_hover = pygame.Color('lightskyblue')
        self.color = self.color_inactive
        self.text = ''
        self.txt_surface = font.render('', True, self.color)
        self.active = False
        self.is_password = is_password
        self.show_password = False 
        self.scroll_offset = 0

    # Handle events for the input box
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos) # Check if clicked inside the box
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN: # Continue when 'Enter' key pressed
                return 'submit'
            elif event.key == pygame.K_BACKSPACE: # Remove character when backspace pressed
                self.text = self.text[:-1]
            else: # Handle other keys
                if len(self.text) < 20:
                    self.text += event.unicode
            if self.is_password: # If password mode, update display text
                display_text = self.text if self.show_password else '*' * len(self.text)
            else:
                display_text = self.text
            self.txt_surface = self.font.render(display_text, True, self.color)

            text_width = self.txt_surface.get_width()
            if text_width > self.rect.width - 20: # If text exceeds box width, enable scrolling
                self.scroll_offset = text_width - (self.rect.width - 20)
            else:
                self.scroll_offset = 0

        return None

    # Update input box state
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos): # Check if mouse is hovering over box
            if not self.active: # If box not active, change colour to hover colour
                border_color = self.color_hover
            else:
                border_color = self.color_active
        else:
            border_color = self.color_active if self.active else self.color_inactive

        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 3)

        # Create surface for text and fill with a dark colour
        text_clip_surface = pygame.Surface((self.rect.width - 6, self.rect.height - 6))
        text_clip_surface.fill((30, 30, 30))

        text_clip_surface.blit(self.txt_surface, (-self.scroll_offset, 0))

        screen.blit(text_clip_surface, (self.rect.x + 3, self.rect.y + 3))

    # Get current text in input box
    def get_text(self):
        return self.text

    # Clear input box text
    def clear(self):
        self.text = ''
        self.txt_surface = self.font.render('', True, self.color)

    # Toggle password visibility
    def toggle_password_visibility(self):
        if self.is_password: # Only toggle if in password mode
            self.show_password = not self.show_password
            display_text = self.text if self.show_password else '*' * len(self.text)
            self.txt_surface = self.font.render(display_text, True, self.color)

# FactFile Class
class FactFile:
    # Initialise FactFile with planet data
    def __init__(self, name, classification, size, mass, distance_from_sun, temperature,
                 position, gravity, rotation_period, orbital_period, composition=None):
        self.name = name
        self.classification = classification
        self.size = size
        self.mass = mass
        self.distance_from_sun = distance_from_sun
        self.temperature = temperature
        self.position = position
        self.gravity = gravity
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.scroll_offset = 0
        self.scroll_velocity = 0
        self.scroll_speed = 600
        self.scroll_direction = 0
        self.dragging_scrollbar = False
        self.drag_start_y = 0
        self.initial_scroll_offset = 0
        self.composition = composition or {}

    # Handle scroll events for fact file
    def handle_scroll(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # Scroll up when 'Up' key pressed
                self.scroll_direction = 1
            elif event.key == pygame.K_DOWN: # Scroll down when 'Down' key pressed
                self.scroll_direction = -1
        elif event.type == pygame.KEYUP: # Stop scrolling when key released
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.scroll_direction = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: # Scroll up with mouse wheel
                self.scroll_offset += 60
            elif event.button == 5: # Scroll down with mouse wheel
                self.scroll_offset -= 60
            elif event.button == 1: # Left mouse button pressed
                mouse_x, mouse_y = event.pos
                thumb_rect = self._get_scroll_thumb_rect()
                if thumb_rect.collidepoint(mouse_x, mouse_y): # Check if clicked on scrollbar thumb
                    self.dragging_scrollbar = True
                    self.drag_start_y = mouse_y
                    self.initial_scroll_offset = self.scroll_offset

        elif event.type == pygame.MOUSEBUTTONUP: # Release mouse button
            if event.button == 1:
                self.dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION: # Mouse moved
            if self.dragging_scrollbar: # If dragging scrollbar
                dy = event.pos[1] - self.drag_start_y
                content_height = self._get_content_height()
                visible_height = HEIGHT // 2
                max_offset = max(1, content_height - visible_height)
                scrollable_area = visible_height - self._get_thumb_height(content_height)
                if scrollable_area > 0: # Prevent division by zero
                    scroll_ratio = dy / scrollable_area
                    self.scroll_offset = self.initial_scroll_offset - scroll_ratio * max_offset

    # Update scroll offset based on scroll speed and direction
    def update_scroll(self, dt):
        self.scroll_velocity = self.scroll_speed * self.scroll_direction
        self.scroll_offset += self.scroll_velocity * dt
        self.scroll_offset = min(0, self.scroll_offset)

    # Draw fact file on screen
    def draw(self, screen):
        draw_parallax_bg()
        
        # Set Up
        name_font = pygame.font.Font("fonts/stellar.otf", 80)
        content_font = default_font
        composition_font = pygame.font.Font("fonts/audiowide.ttf", 36)

        # Render Fact File Content
        lines = [
            f"{self.name}",
            f"Classification: {self.classification}",
            f"Position in Solar System: {self.position}",
            f"Distance from Sun: {self.distance_from_sun}",
            f"Diameter: {self.size}",
            f"Mass: {self.mass}",
            f"Surface Gravity: {self.gravity}",
            f"Rotation Period: {self.rotation_period}",
            f"Orbital Period: {self.orbital_period}",
            f"Average Surface Temperature: {self.temperature}"
        ]
        
        title_text = factfile_name_font.render(lines[0], True, (255, 255, 255))

        line_spacing = 20
        start_y = HEIGHT // 4 + self.scroll_offset

        for line in lines[1:]: # Render each line of fact file
            text_surface = factfile_content_font.render(line, True, (255, 255, 255))
            faded_surface = factfile_content_font.render(line, True, (180, 180, 180))

        content_height = self._get_content_height()
        visible_height = HEIGHT // 2
        min_scroll = min(0, visible_height - content_height)

        if self.scroll_offset < min_scroll: # Clamp scroll offset to minimum
            self.scroll_offset = min_scroll
        elif self.scroll_offset > 0: # Clamp scroll offset to maximum
            self.scroll_offset = 0

        # Draw Title
        title_y = 50 + self.scroll_offset
        title_text = name_font.render(lines[0], True, (255, 255, 255))
        screen.blit(title_text, (solar_system_button_rect.right + 20, title_y))

        # Draw Divider
        divider_y = title_y + name_font.get_height() + 10
        pygame.draw.line(screen, (100, 100, 100), (solar_system_button_rect.right + 20, divider_y), (WIDTH - 60, divider_y), 2)

        y_offset = divider_y + 30

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for line in lines[1:]: # Render each line of fact file
            wrapped_lines = wrap_text(line, content_font, WIDTH - 100)
            for wrapped_line in wrapped_lines: # Wrap text to fit within width
                text_surface = content_font.render(wrapped_line, True, (255, 255, 255))
                faded_surface = content_font.render(wrapped_line, True, (180, 180, 180))

                text_rect = text_surface.get_rect(topleft=(solar_system_button_rect.right + 20, y_offset))

                if text_rect.collidepoint(mouse_x, mouse_y): # Check if mouse is hovering over text
                    screen.blit(text_surface, text_rect.topleft)
                else:
                    screen.blit(faded_surface, text_rect.topleft)

                y_offset += content_font.get_height() + 10

            y_offset += 60

        y_offset += 10
        pygame.draw.line(screen, (150, 150, 150), (solar_system_button_rect.right + 20, y_offset),
                         (WIDTH - 60, y_offset), 2)
        y_offset += 30

        composition_title = composition_font.render("Composition", True, (255, 255, 255))
        screen.blit(composition_title, (solar_system_button_rect.right + 20, y_offset))
        y_offset += composition_title.get_height() + 20

        for layer, details in self.composition.items(): # Render composition details
            layer_title = content_font.render(f"{layer}:", True, (200, 200, 200))
            screen.blit(layer_title, (solar_system_button_rect.right + 20, y_offset))
            y_offset += layer_title.get_height() + 10

            wrapped_lines = wrap_text(details, content_font, WIDTH - 250)
            for line in wrapped_lines: # Wrap text to fit within width
                text_surface = content_font.render(line, True, (255, 255, 255))
                faded_surface = content_font.render(line, True, (180, 180, 180))
                text_rect = text_surface.get_rect(topleft=(solar_system_button_rect.right + 40, y_offset))

                if text_rect.collidepoint(mouse_x, mouse_y): # Check if mouse is hovering over text
                    screen.blit(text_surface, text_rect.topleft)
                else:
                    screen.blit(faded_surface, text_rect.topleft)

                y_offset += content_font.get_height() + 20

            y_offset += 20

        self._composition_height = y_offset

        # Draw Scrollbar
        scrollbar_height = HEIGHT // 2
        scrollbar_y = HEIGHT // 4
        pygame.draw.rect(screen, (50, 50, 50), (WIDTH - 40, scrollbar_y, 20, scrollbar_height))

        thumb_rect = self._get_scroll_thumb_rect()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered = thumb_rect.collidepoint(mouse_x, mouse_y)
        thumb_color = (220, 220, 220, 255) if hovered else (180, 180, 180, 180)
        thumb_surface = pygame.Surface((thumb_rect.width, thumb_rect.height), pygame.SRCALPHA)
        thumb_surface.fill(thumb_color)
        screen.blit(thumb_surface, thumb_rect.topleft)

        screen.blit(solar_system_button, solar_system_button_rect.topleft)

    # Calculate total height of content for scrolling
    def _get_content_height(self):
        base_line_spacing = 60
        base_lines = 10
        composition_lines = 1

        for layer, details in self.composition.items(): # Calculate height of composition details
            composition_lines += 1
            wrapped = wrap_text(details, factfile_content_font, WIDTH - 100)
            composition_lines += len(wrapped)

        return 80 + base_lines * (30 + base_line_spacing) + composition_lines * (factfile_content_font.get_height() + 25) + 20 * len(self.composition) + 50

    # Calculate height of scrollbar thumb based on content height
    def _get_thumb_height(self, content_height):
        scrollbar_height = HEIGHT // 2
        return max(scrollbar_height * scrollbar_height // content_height, 30)

    # Get rectangle for scrollbar thumb based on scroll offset
    def _get_scroll_thumb_rect(self):
        content_height = self._get_content_height()
        scrollbar_height = HEIGHT // 2
        scrollbar_y = HEIGHT // 4
        thumb_height = self._get_thumb_height(content_height)
        max_offset = max(1, content_height - scrollbar_height)
        scroll_ratio = -self.scroll_offset / max_offset
        thumb_y = scrollbar_y + scroll_ratio * (scrollbar_height - thumb_height)

        thumb_y = max(scrollbar_y, min(scrollbar_y + scrollbar_height - thumb_height, thumb_y))

        return pygame.Rect(WIDTH - 40, thumb_y, 20, thumb_height)

# Planet Class
class Planet:
    # Initialise Planet with name, image path, size, radius, speed and angle
    def __init__(self, name, image_path, size, radius, speed, angle=None):
        self.name = name
        self.original_image_path = image_path
        self.touch_image_path = image_path.replace(".png", "_touch.png")
        self.size = size
        self.radius = radius
        self.speed = speed
        self.angle = angle if angle is not None else random.uniform(0, 2 * math.pi)
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
        self.original_image = self.image.copy()
        self.touched = False
        self.position = (0, 0)

    # Update planet position based on angle and speed
    def update_position(self, center, dt):
        self.angle += self.speed * dt
        cx, cy = center
        self.position = (
            cx + math.cos(self.angle) * self.radius - self.size[0] // 2,
            cy + math.sin(self.angle) * self.radius - self.size[1] // 2
        )

    # Update touch state based on player rectangle
    def update_touch_state(self, player_rect):
        planet_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        if planet_rect.colliderect(player_rect): # Check if player touching planet
            if not self.touched: # If not already touched, change image to touch image
                try:
                    self.image = pygame.transform.scale(pygame.image.load(self.touch_image_path).convert_alpha(), self.size)
                except:
                    pass
                self.touched = True
        else: # If player not touching planet, reset image to original
            if self.touched:
                self.image = self.original_image.copy()
                self.touched = False

    # Draw planet on screen at its current position
    def draw(self, screen, camera_x, camera_y, zoom):
        scaled = pygame.transform.smoothscale(self.image, (int(self.size[0] * zoom), int(self.size[1] * zoom)))
        screen.blit(scaled, ((self.position[0] - camera_x) * zoom, (self.position[1] - camera_y) * zoom))

# Collectible Class
class Collectible:
    # Initialise Collectible with name, planet, fact flags, collected attribute, image, touch image, rectangle and label color
    def __init__(self, name, planet, fact_flags, collected_attr, img, touch_img, rect, label_color):
        self.name = name
        self.planet = planet
        self.fact_flags = fact_flags
        self.collected_attr = collected_attr
        self.img = img
        self.touch_img = touch_img
        self.rect = rect
        self.label_color = label_color

    # Check if collectible is available to collect
    def is_available(self):
        if all(self.fact_flags.values()) and not getattr(sys.modules[__name__], self.collected_attr): # Check if all fact flags are true and collectible not collected
            normalized_inventory = [item.lower().replace(" ", "_") for item in player_inventory.get_items()]
            normalized_name = self.name.lower().replace(" ", "_")
            return normalized_name not in normalized_inventory

        return False

    # Draw collectible on screen
    def draw(self, screen, player_rect, label_font):
        if not self.is_available(): # If collectible not available, do not draw
            return

        hovered = player_rect.colliderect(self.rect)
        screen.blit(self.touch_img if hovered else self.img, self.rect.topleft)

        if hovered: # If collectible is hovered, display its label
            label = label_font.render(self.name, True, (255, 255, 255))
            label_rect = label.get_rect(midbottom=(self.rect.centerx, self.rect.top - 10))
            bg_rect = pygame.Rect(label_rect.left - 8, label_rect.top - 8, label_rect.width + 16, label_rect.height + 16)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill(self.label_color)
            screen.blit(bg_surface, (bg_rect.left, bg_rect.top))
            screen.blit(label, label_rect)

# Inventory Class
class Inventory:
    # Initialise Inventory with empty item list
    def __init__(self):
        self.items = []

    # Add item to inventory if not already present
    def add(self, item_name):
        if item_name not in self.items: # Check if item already exists
            self.items.append(item_name)

    # Remove item from inventory if it exists
    def remove(self, item_name):
        if item_name in self.items: # Check if item exists before removing
            self.items.remove(item_name)

    # Check if item is in inventory
    def contains(self, item_name):
        return item_name in self.items

    # Clear all items from inventory
    def get_items(self):
        return list(self.items)

    # Draw inventory items on screen
    def draw(self, screen, font, rect, item_size=100, columns=6, padding=20):
        pygame.draw.rect(screen, (30, 30, 30), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        title_text = font.render("Inventory", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(rect.centerx, rect.top + 30))
        screen.blit(title_text, title_rect)

        start_x = rect.left + padding
        start_y = rect.top + 70
        for index, item in enumerate(self.items): # Iterate through each item in inventory
            row = index // columns
            col = index % columns
            x = start_x + col * (item_size + padding)
            y = start_y + row * (item_size + padding)

            try: # Load item image and draw on screen
                img = pygame.image.load(f"inventory_items/{item}.png").convert_alpha()
                img = pygame.transform.scale(img, (item_size, item_size))
                screen.blit(img, (x, y))
            except:
                pass

# Wrap block of text so each line fits within specified width
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words: # Iterate through each word in text
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width: # Check if adding word exceeds max width
            current_line = test_line
        else: # If it does, add current line to lines and start new line
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line: # If any remaining text in current line, add to lines
        lines.append(current_line.strip())

    return lines

# Surface Feature Data
surface_features = {
    name: SurfaceFeatureSet(features)
    for name, features in surface_feature_data.items()
}

feature_facts = feature_facts_data

# Clamp given screen position to the screen edges
def clamp_to_screen_edge(target_screen_pos):
    x, y = target_screen_pos
    margin = 40
    x = max(margin, min(WIDTH - margin, x))
    y = max(margin, min(HEIGHT - margin, y))
    if target_screen_pos[0] < 0: x = margin
    if target_screen_pos[0] > WIDTH: x = WIDTH - margin
    if target_screen_pos[1] < 0: y = margin
    if target_screen_pos[1] > HEIGHT: y = HEIGHT - margin

    return x, y

# Planet attributes and data loading
planet_data = [
    ("Mercury", "game_graphics/mercury.png", (128, 128), 500, 0.2),
    ("Venus", "game_graphics/venus.png", (192, 192), 800, 0.1),
    ("Earth", "game_graphics/earth.png", (256, 256), 1100, 0.08),
    ("Mars", "game_graphics/mars.png", (192, 192), 1400, 0.06),
    ("Jupiter", "game_graphics/jupiter.png", (256, 256), 1800, 0.04),
    ("Saturn", "game_graphics/saturn.png", (256, 256), 2200, 0.03),
    ("Uranus", "game_graphics/uranus.png", (192, 192), 2600, 0.02),
    ("Neptune", "game_graphics/neptune.png", (192, 192), 3000, 0.015),
    ("Pluto", "game_graphics/pluto.png", (128, 128), 3400, 0.01),
]

# Load fact file data
fact_files = {
    name: FactFile(
        name,
        data["classification"],
        data["size"],
        data["mass"],
        data["distance_from_sun"],
        data["temperature"],
        data["position"],
        data["gravity"],
        data["rotation_period"],
        data["orbital_period"],
        data.get("composition", {})
    )
    for name, data in factfile_data.items()
}

planets = [Planet(name, path, size, radius, speed) for name, path, size, radius, speed in planet_data]

# Player Movement Logic Variables
player_pos = [WORLD_WIDTH // 2 - player_size[0] // 2, WORLD_HEIGHT // 2 - player_size[1] // 2]
player_vel = [0.0, 0.0]
acceleration = 0.5
friction = 0.95
base_acceleration = 1.0
max_speed = 10

#Game State
clock = pygame.time.Clock()
running = True
in_game = False
zoom = 1.0
zoom_min = 0.5
zoom_max = 2.0
zoom_step = 0.1
in_fact_file = False
active_planet = None
in_login_screen = False
in_help_screen = False
current_user = None
menu_scroll_speed_x = 20
menu_scroll_speed_y = 10
show_arrows = True
in_inventory = False
on_surface = False
current_surface_name = None
surface_player_pos = [50, HEIGHT // 2]
surface_player_vel = [0.0, 0.0]
feature_fact_active = False
active_feature_fact = None
confirm_exit_unsaved = False
movement_tip_alpha = 0
movement_tip_timer = 0
show_movement_tip = False
eligible_collectible_planets = {"Sun", "Mercury", "Venus", "Earth", "Mars", "Saturn", "Uranus", "Pluto"}
show_tip = False
tip_timer = 0
tip_alpha = 0
item_added_timer = 0
show_item_added = False

login_mode = "sign_in"
input_username = InputBox(WIDTH // 2 - 150, HEIGHT // 3, 300, 50, default_font)
input_password = InputBox(WIDTH // 2 - 150, HEIGHT // 3 + 70, 300, 50, default_font, is_password=True)
login_message = ""

# Collectibles (State)
sun_fact_opened = {"sunspot": False, "solar_flare": False}
plasma_collected = False
player_inventory = Inventory()
mercury_fact_opened = {"caloris_basin": False, "hollow": False, "cliff": False, "crater": False}
silicate_rock_collected = False
silicate_rock_img = pygame.image.load("inventory_items/silicate_rock.png").convert_alpha()
silicate_rock_touch_img = pygame.image.load("inventory_items/silicate_rock_touch.png").convert_alpha()
silicate_rock_rect = silicate_rock_img.get_rect(topleft=(150, 550))
venus_fact_opened = {"maat_mons": False, "lava_plains": False, "tessera": False}
basalt_collected = False
basalt_img = pygame.image.load("inventory_items/basalt.png").convert_alpha()
basalt_touch_img = pygame.image.load("inventory_items/basalt_touch.png").convert_alpha()
basalt_rect = basalt_img.get_rect(topleft=(750, 210))
earth_fact_opened = {"life": False, "biomes": False, "continents": False}
leaf_collected = False
leaf_img = pygame.image.load("inventory_items/leaf.png").convert_alpha()
leaf_touch_img = pygame.image.load("inventory_items/leaf_touch.png").convert_alpha()
leaf_rect = leaf_img.get_rect(topleft=(800, 300))
mars_fact_opened = {"ice_caps": False, "valles_marineris": False, "olympus_mons": False}
blueberries_collected = False
blueberries_img = pygame.image.load("inventory_items/blueberries.png").convert_alpha()
blueberries_touch_img = pygame.image.load("inventory_items/blueberries_touch.png").convert_alpha()
blueberries_rect = blueberries_img.get_rect(topleft=(780, 260))
saturn_fact_opened = {"saturn_surface": False, "saturn_rings": False, "hexagon": False}
water_ice_collected = False
water_ice_img = pygame.image.load("inventory_items/water_ice.png").convert_alpha()
water_ice_touch_img = pygame.image.load("inventory_items/water_ice_touch.png").convert_alpha()
water_ice_rect = water_ice_img.get_rect(topleft=(830, 220))
uranus_fact_opened = {"tilt": False, "uranus_surface": False}
methane_ice_collected = False
methane_ice_img = pygame.image.load("inventory_items/methane_ice.png").convert_alpha()
methane_ice_touch_img = pygame.image.load("inventory_items/methane_ice_touch.png").convert_alpha()
methane_ice_rect = methane_ice_img.get_rect(topleft=(750, 240))
pluto_fact_opened = {"tombaugh_regio": False, "icy_mountains": False}
frozen_nitrogen_collected = False
frozen_nitrogen_img = pygame.image.load("inventory_items/frozen_nitrogen.png").convert_alpha()
frozen_nitrogen_touch_img = pygame.image.load("inventory_items/frozen_nitrogen_touch.png").convert_alpha()
frozen_nitrogen_rect = frozen_nitrogen_img.get_rect(topleft=(750, 220))

# Collectibles List
collectibles = [
    Collectible("Plasma", "Sun", sun_fact_opened, 'plasma_collected', plasma_img, plasma_touch_img, plasma_rect, (100, 255, 100, 120)),
    Collectible("Silicate Rock", "Mercury", mercury_fact_opened, 'silicate_rock_collected', silicate_rock_img, silicate_rock_touch_img, silicate_rock_rect, (200, 200, 100, 120)),
    Collectible("Basalt", "Venus", venus_fact_opened, 'basalt_collected', basalt_img, basalt_touch_img, basalt_rect, (160, 120, 60, 140)),
    Collectible("Leaf", "Earth", earth_fact_opened, 'leaf_collected', leaf_img, leaf_touch_img, leaf_rect, (80, 255, 80, 140)),
    Collectible("Blueberries", "Mars", mars_fact_opened, 'blueberries_collected', blueberries_img, blueberries_touch_img, blueberries_rect, (150, 150, 255, 130)),
    Collectible("Water Ice", "Saturn", saturn_fact_opened, 'water_ice_collected', water_ice_img, water_ice_touch_img, water_ice_rect, (180, 220, 255, 130)),
    Collectible("Methane Ice", "Uranus", uranus_fact_opened, 'methane_ice_collected', methane_ice_img, methane_ice_touch_img, methane_ice_rect, (100, 200, 255, 130)),
    Collectible("Frozen Nitrogen", "Pluto", pluto_fact_opened, 'frozen_nitrogen_collected', frozen_nitrogen_img, frozen_nitrogen_touch_img, frozen_nitrogen_rect, (220, 255, 255, 130)),
]

# Function for drawing the parallax background effect
def draw_parallax_bg():
    mouse_x, mouse_y = pygame.mouse.get_pos()

    offset_x = (mouse_x - WIDTH / 2) / (WIDTH / 2)
    offset_y = (mouse_y - HEIGHT / 2) / (HEIGHT / 2)

    parallax_strength = 30
    scroll_x = int(offset_x * parallax_strength)
    scroll_y = int(offset_y * parallax_strength)

    for x in range(-bg_tile_width, WIDTH + bg_tile_width, bg_tile_width): # Loop through background tiles
        for y in range(-bg_tile_height, HEIGHT + bg_tile_height, bg_tile_height):
            screen.blit(bg_tile, (x - scroll_x, y - scroll_y))

# Function to draw the home menu screen
def draw_menu():
    mouse_x, mouse_y = pygame.mouse.get_pos()

    offset_x = (mouse_x - WIDTH / 2) / (WIDTH / 2)
    offset_y = (mouse_y - HEIGHT / 2) / (HEIGHT / 2)

    # Parallax Effect
    parallax_strength = 30
    scroll_x = int(offset_x * parallax_strength)
    scroll_y = int(offset_y * parallax_strength)

    for x in range(-bg_tile_width, WIDTH + bg_tile_width, bg_tile_width): # Loop through background tiles
        for y in range(-bg_tile_height, HEIGHT + bg_tile_height, bg_tile_height):
            screen.blit(bg_tile, (x - scroll_x, y - scroll_y))

    # Draw Title
    title_line1 = title_font.render("Stellar", True, (255, 255, 255))
    title_line2 = title_font.render("Odyssey", True, (255, 255, 255))
    spacing = 10
    start_y = HEIGHT // 7

    screen.blit(title_line1, (WIDTH // 2 - title_line1.get_width() // 2, start_y))
    screen.blit(title_line2, (WIDTH // 2 - title_line2.get_width() // 2, start_y + title_line1.get_height() + spacing))

    if play_button_rect.collidepoint((mouse_x, mouse_y)): # Play button hover effect
        screen.blit(play_button_hover, play_button_rect.topleft)
    else:
        screen.blit(play_button, play_button_rect.topleft)

    if login_button_rect.collidepoint((mouse_x, mouse_y)): # Login button hover effect
        screen.blit(login_button_hover, login_button_rect.topleft)
    else:
        screen.blit(login_button, login_button_rect.topleft)

    if help_button_rect.collidepoint((mouse_x, mouse_y)): # Help button hover effect
        screen.blit(help_button_hover, help_button_rect.topleft)
    else:
        screen.blit(help_button, help_button_rect.topleft)

    if close_button_rect.collidepoint((mouse_x, mouse_y)): # Close button hover effect
        screen.blit(close_button_hover, close_button_rect.topleft)
    else:
        screen.blit(close_button, close_button_rect.topleft)

    pygame.display.flip()

# Main Game Script
while running:
    # Set events and framerate
    dt = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    # Show movement guide when player enters main game
    if show_movement_tip:
        movement_tip_timer += dt

        if movement_tip_timer < 1: # Fade in movement tip
            movement_tip_alpha = int((movement_tip_timer / 1.0) * 255)
        elif movement_tip_timer < 4:
            movement_tip_alpha = 255
        elif movement_tip_timer < 6: # Fade out movement tip
            movement_tip_alpha = int((1 - (movement_tip_timer - 4) / 2.0) * 255)
        else:
            show_movement_tip = False

    # Show item message for player guide
    if show_item_added:
        item_added_timer += dt
        if item_added_timer >= 3:
            show_item_added = False

    # Show tip for collectibles for player guide
    if show_tip:
        tip_timer += dt
        if tip_timer < 1: # Fade in tip
            tip_alpha = int((tip_timer / 1.0) * 255)
        elif tip_timer < 4:
            tip_alpha = 255
        elif tip_timer < 6: # Fade out tip
            tip_alpha = int((1 - (tip_timer - 4) / 2.0) * 255)
        else:
            show_tip = False

    # In Game Menu Logic
    if in_menu:
        screen.fill((0, 0, 0))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw menu texts
        menu_title_font = pygame.font.Font(font_path, 60)
        title_text = menu_title_font.render("Menu", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 70))
        screen.blit(title_text, title_rect)

        # Divider specifications
        divider_width = 900
        divider_y = 130
        divider_x_start = (WIDTH - divider_width) // 2
        divider_x_end = divider_x_start + divider_width
        pygame.draw.line(screen, (150, 150, 150), (divider_x_start, divider_y), (divider_x_end, divider_y), 2)

        # Button interactions
        if solar_system_button_rect.collidepoint((mouse_x, mouse_y)): # Solar System button hover effect
            screen.blit(solar_system_button_hover, solar_system_button_rect.topleft)
        else:
            screen.blit(solar_system_button, solar_system_button_rect.topleft)

        if return_menu_button_rect.collidepoint((mouse_x, mouse_y)): # Return to home menu button hover effect
            screen.blit(return_menu_button_hover, return_menu_button_rect.topleft)
        else:
            screen.blit(return_menu_button, return_menu_button_rect.topleft)
        
        if close_button_rect.collidepoint((mouse_x, mouse_y)): # Close button hover effect
            screen.blit(close_button_hover, close_button_rect.topleft)
        else:
            screen.blit(close_button, close_button_rect.topleft)
        
        # Label specifications
        label_font_small = pygame.font.Font(font_path2, 20)

        # 'Back' Label
        back_label = label_font_small.render("Back", True, (255, 255, 255))
        back_label_rect = back_label.get_rect(center=(solar_system_button_rect.centerx, solar_system_button_rect.bottom + 15))
        screen.blit(back_label, back_label_rect)

        # 'Home' Label
        home_label = label_font_small.render("Home", True, (255, 255, 255))
        home_label_rect = home_label.get_rect(center=(return_menu_button_rect.centerx, return_menu_button_rect.top - 20))
        screen.blit(home_label, home_label_rect)

        menu_label_font = pygame.font.Font(font_path2, 32)
        arrow_label = menu_label_font.render("Show indicative arrows:", True, (255, 255, 255))
        screen.blit(arrow_label, (190, 160))

        if show_arrows: # Show arrows button
            screen.blit(arrows_on_img, arrows_button_rect.topleft)
        else:
            screen.blit(arrows_off_img, arrows_button_rect.topleft)

        # Second divider
        divider_x_start = (WIDTH - 900) // 2
        divider_x_end = divider_x_start + 900
        pygame.draw.line(screen, (150, 150, 150), (divider_x_start, 230), (divider_x_end, 230), 2)

        # Instructions text information
        instruction_font_small = pygame.font.Font(font_path2, 24)
        instruction_font_large = pygame.font.Font(font_path2, 32)

        instruction_start_x = 190
        instruction_start_y = 250
        line_spacing = 30

        controls_title = instruction_font_large.render("Controls", True, (255, 255, 255))
        screen.blit(controls_title, (instruction_start_x, instruction_start_y))
        y_offset = instruction_start_y + line_spacing + 5

        instruction_lines = [
            ("(WASD) - Move", instruction_font_small),
            ("(F) - Open Fact File", instruction_font_small),
            ("(E) - Explore Surface", instruction_font_small),
            ("(I) - Open Inventory", instruction_font_small),
        ]

        for text, font in instruction_lines: # Render control instructions
            rendered = font.render(text, True, (200, 200, 200))
            screen.blit(rendered, (instruction_start_x, y_offset))
            y_offset += line_spacing

        pygame.draw.line(screen, (150, 150, 150), (divider_x_start, y_offset + 10), (divider_x_end, y_offset + 10), 2)

        # In Surface Controls
        y_offset += 30
        in_surface_title = instruction_font_large.render("In Surface", True, (255, 255, 255))
        screen.blit(in_surface_title, (instruction_start_x, y_offset))
        y_offset += line_spacing + 5

        surface_lines = [
            ("(Space) - Open Fact Box", instruction_font_small),
            ("(C) - Collect Item", instruction_font_small)
        ]

        for text, font in surface_lines: # Render surface control instructions
            rendered = font.render(text, True, (200, 200, 200))
            screen.blit(rendered, (instruction_start_x, y_offset))
            y_offset += line_spacing

        if show_arrows: # Show arrows button
            screen.blit(arrows_on_img, arrows_button_rect.topleft)
        else:
            screen.blit(arrows_off_img, arrows_button_rect.topleft)

        pygame.display.flip()

        # Button logic inside game menu
        for event in events:
            if event.type == pygame.QUIT:
                if current_user: # If user is logged in, save their inventory before quitting
                    save_user_inventory(current_user, player_inventory.get_items())
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if solar_system_button_rect.collidepoint(event.pos): # Return to Solar System
                    play_button_click()
                    in_menu = False
                elif in_menu and return_menu_button_rect.collidepoint(event.pos): # Return to home menu
                    play_button_click()
                    if current_user: 
                        in_menu = False
                        in_game = False
                    else:
                        confirm_exit_unsaved = True
                        in_menu = False
                elif close_button_rect.collidepoint(event.pos): # Close the game
                    play_button_click()
                    running = False
                elif arrows_button_rect.collidepoint(event.pos): # Toggle arrows visibility
                    play_button_click()
                    show_arrows = not show_arrows
                    pygame.time.wait(150)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Exit menu with escape key
                in_menu = False

        continue
    
    # Home Menu Logic
    for event in events:
        if event.type == pygame.QUIT: # Close the game
            running = False

        if not in_game and not in_login_screen and not in_help_screen: # Home menu events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos): # Start the game
                    play_button_click()
                    if current_user is None: # Reset inventory and collectible states for signed out players
                        player_inventory.items.clear()
                        plasma_collected = False
                        silicate_rock_collected = False
                        basalt_collected = False
                        leaf_collected = False
                        blueberries_collected = False
                        water_ice_collected = False
                        methane_ice_collected = False
                        frozen_nitrogen_collected = False
                        for d in [ # Reset all fact-opened dictionaries for each celestial body
                            sun_fact_opened,
                            mercury_fact_opened,
                            venus_fact_opened,
                            earth_fact_opened,
                            mars_fact_opened,
                            saturn_fact_opened,
                            uranus_fact_opened,
                            pluto_fact_opened
                        ]:
                            for key in d: # 
                                d[key] = False
                    in_game = True
                    show_movement_tip = True
                    movement_tip_alpha = 0
                    movement_tip_timer = 0
                    on_surface = False
                    in_fact_file = False
                    in_inventory = False
                    current_surface_name = None
                    feature_fact_active = False
                    active_feature_fact = None
                    active_planet = None
                    zoom = 1.0
                    player_pos = [sun_center[0] - player_size[0] // 2, sun_center[1] - player_size[1] // 2]
                    player_vel = [0.0, 0.0]
                    surface_player_pos = [50, HEIGHT // 2]
                    surface_player_vel = [0.0, 0.0]
                elif login_button_rect.collidepoint(event.pos): # Open login screen
                    play_button_click()
                    in_login_screen = True
                elif close_button_rect.collidepoint(event.pos): # Close the game
                    play_button_click()
                    running = False
                elif help_button_rect.collidepoint(event.pos): # Open help screen
                    play_button_click()
                    in_help_screen = True

        elif in_fact_file and active_planet: # Fact file events
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                in_fact_file = False
                active_planet = None
            else:
                fact_files[active_planet.name].handle_scroll(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if solar_system_button_rect.collidepoint(event.pos): # Return to Solar System
                        play_button_click()
                        in_fact_file = False
                        active_planet = None

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # Scroll up to zoom in
                    zoom = min(zoom + zoom_step, zoom_max)
                elif event.button == 5: # Scroll down to zoom out
                    zoom = max(zoom - zoom_step, zoom_min)
                elif event.button == 1:
                    if game_menu_button_rect.collidepoint(event.pos) and not in_inventory: # Open game menu
                        play_button_click()
                        in_menu = True
                    elif in_game and inventory_button_rect.collidepoint(event.pos) and not in_inventory: # Open inventory
                        play_button_click()
                        in_inventory = True
                        pygame.time.wait(150)

                    elif current_user and not in_inventory and not on_surface and sign_out_button_rect.collidepoint(event.pos): # Sign out
                        play_button_click()
                        save_user_inventory(current_user, player_inventory.get_items())
                        current_user = None
                        player_inventory.items.clear()
                        plasma_collected = False
                        silicate_rock_collected = False
                        basalt_collected = False
                        leaf_collected = False
                        blueberries_collected = False
                        water_ice_collected = False
                        methane_ice_collected = False
                        frozen_nitrogen_collected = False
                        for d in [ # Reset all fact-opened dictionaries for each celestial body
                            sun_fact_opened,
                            mercury_fact_opened,
                            venus_fact_opened,
                            earth_fact_opened,
                            mars_fact_opened,
                            saturn_fact_opened,
                            uranus_fact_opened,
                            pluto_fact_opened
                        ]:
                            for key in d:
                                d[key] = False
                        in_game = False
                        in_menu = False
                        in_login_screen = False
                        login_message = ""
                        input_username.clear()
                        input_password.clear()
                        pygame.time.wait(200)
                        continue

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if in_game and not in_inventory and not in_menu: # Open fact file
                        for planet in planets: # Check each planet for player collision
                            planet_rect = pygame.Rect(
                                planet.position[0], planet.position[1],
                                planet.size[0], planet.size[1]
                            )
                            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
                            if player_rect.colliderect(planet_rect): # Ensure player touching planet for fact file
                                in_fact_file = True
                                active_planet = planet
                                break

                        sun_rect = pygame.Rect(sun_draw_pos[0], sun_draw_pos[1], sun_size[0], sun_size[1])
                        sun_rect.inflate_ip(-40, -40)
                        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
                        if player_rect.colliderect(sun_rect): # Fact file collision detection for Sun
                            in_fact_file = True
                            active_planet = type("SunObject", (), {"name": "Sun"})()
                elif event.key == pygame.K_r: # Reset player position to centre
                    if in_game and not on_surface and not in_inventory:
                        player_pos = [sun_center[0] - player_size[0] // 2, sun_center[1] - player_size[1] // 2]
                        player_vel = [0.0, 0.0]
                elif event.key == pygame.K_i: # Toggle inventory
                    if in_game and not in_login_screen and not in_help_screen:
                        in_inventory = not in_inventory
                elif event.key == pygame.K_e: # Explore surface
                    if in_game and not on_surface and not in_inventory:
                        for planet in planets:
                            planet_rect = pygame.Rect(planet.position[0], planet.position[1], planet.size[0], planet.size[1])
                            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
                            if player_rect.colliderect(planet_rect): # Enter surface exploration mode
                                surface_player_pos = [50, HEIGHT // 2]
                                surface_player_vel = [0.0, 0.0]
                                current_surface_name = planet.name
                                on_surface = True
                                if current_surface_name in eligible_collectible_planets: # Check if surface has collectibles
                                    item_name = next((c.name for c in collectibles if c.planet == current_surface_name), None)
                                    if item_name:
                                        normalized = item_name.lower().replace(" ", "_")
                                        if normalized not in [i.lower().replace(" ", "_") for i in player_inventory.get_items()]: # Collectible not in inventory
                                            show_tip = True
                                            tip_alpha = 0
                                            tip_timer = 0
                                break

                        sun_rect = pygame.Rect(sun_draw_pos[0], sun_draw_pos[1], sun_size[0], sun_size[1])
                        if player_rect.colliderect(sun_rect.inflate(-40, -40)): # Enter Sun surface exploration mode
                            surface_player_pos = [50, HEIGHT // 2]
                            surface_player_vel = [0.0, 0.0]
                            current_surface_name = "Sun"
                            on_surface = True
                            if current_surface_name in eligible_collectible_planets: # Check if surface has collectibles
                                item_name = next((c.name for c in collectibles if c.planet == current_surface_name), None)
                                if item_name:
                                    normalized = item_name.lower().replace(" ", "_")
                                    if normalized not in [i.lower().replace(" ", "_") for i in player_inventory.get_items()]: # Collectible not in inventory
                                        show_tip = True
                                        tip_alpha = 0
                                        tip_timer = 0

        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT: # Close the game
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if in_menu and return_menu_button_rect.collidepoint(event.pos): # Return to home menu
                    play_button_click()
                    in_login_screen = False
                    pygame.time.wait(100)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Exit game menu with escape key
                in_login_screen = False

        continue

    # Login Screen Logic
    if in_login_screen:
        draw_parallax_bg()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        # Eye icon for password visibility toggle
        eye_rect = eye_icon.get_rect()
        eye_rect.topleft = (input_password.rect.right + 10, input_password.rect.y + 5)

        for event in events:
            if event.type == pygame.QUIT: # Close the game
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Exit login screen with escape key
                in_login_screen = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_menu_button_rect.collidepoint(event.pos): # Return to home menu
                    play_button_click()
                    in_login_screen = False

                if eye_rect.collidepoint(event.pos): # Toggle password visibility
                    play_button_click()
                    input_password.toggle_password_visibility()

            # Handle input box events
            result1 = input_username.handle_event(event)
            result2 = input_password.handle_event(event)

            if result1 == 'submit' or result2 == 'submit': # Validate credentials on submit
                username = input_username.get_text()
                password = input_password.get_text()

                valid, validation_msg = validate_credentials(username, password)
                
                if not valid: # Invalid credentials
                    login_message = validation_msg
                else:
                    if login_mode == "sign_in":
                        if authenticate_user(username, password): # Load game for successfully logged in player
                            login_message = f"Welcome, {username}!"
                            in_login_screen = False
                            current_user = username
                            player_inventory.items = load_user_inventory(username)
                            in_game = True
                            show_movement_tip = True
                            movement_tip_alpha = 0
                            movement_tip_timer = 0

                            player_pos = [sun_center[0] - player_size[0] // 2, sun_center[1] - player_size[1] // 2]
                            player_vel = [0.0, 0.0]
                            surface_player_pos = [50, HEIGHT // 2]
                            surface_player_vel = [0.0, 0.0]

                            on_surface = False
                            in_fact_file = False
                            in_inventory = False
                            current_surface_name = None
                            feature_fact_active = False
                            active_feature_fact = None
                            active_planet = None
                            zoom = 1.0

                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                if play_button_rect.collidepoint(event.pos): # Start the game
                                    play_button_click()
                                    in_game = True
                                    show_movement_tip = True
                                    movement_tip_alpha = 0
                                    movement_tip_timer = 0
                                    on_surface = False
                                    in_fact_file = False
                                    in_inventory = False
                                    current_surface_name = None
                                    feature_fact_active = False
                                    active_feature_fact = None
                                    active_planet = None
                                    zoom = 1.0

                                    player_pos = [sun_center[0] - player_size[0] // 2, sun_center[1] - player_size[1] // 2]
                                    player_vel = [0.0, 0.0]

                                    surface_player_pos = [50, HEIGHT // 2]
                                    surface_player_vel = [0.0, 0.0]
                        else: # Invalid credentials
                            login_message = "Invalid credentials."
                    else: # Sign up mode
                        success, msg = register_user(username, password)
                        login_message = msg
                        if success:
                            input_username.clear()
                            input_password.clear()

        # Draw input boxes and buttons
        input_username.draw(screen)
        input_password.draw(screen)

        if input_password.show_password: # Show closed eye icon if password is visible
            screen.blit(eye_closed_icon, eye_rect)
        else:
            screen.blit(eye_icon, eye_rect)

        # Draw buttons
        label = title_font.render("Log In" if login_mode == "sign_in" else "Sign Up", True, (255, 255, 255))
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 6))

        button_rect = sign_in_button_rect if login_mode == "sign_in" else sign_up_button_rect
        button_default = sign_in_button if login_mode == "sign_in" else sign_up_button
        button_hover = sign_in_button_hover if login_mode == "sign_in" else sign_up_button_hover

        if button_rect.collidepoint((mouse_x, mouse_y)): # Button hover effect
            screen.blit(button_hover, button_rect.topleft)
            if mouse_clicked: # Button click event
                username = input_username.get_text()
                password = input_password.get_text()

                valid, validation_msg = validate_credentials(username, password) # Validate credentials
                
                if not valid: # Invalid credentials
                    login_message = validation_msg
                else:
                    if login_mode == "sign_in": # Sign in mode
                        if authenticate_user(username, password): # Enter game if credentials are valid
                            login_message = f"Welcome, {username}!"
                            in_login_screen = False
                            current_user = username
                            player_inventory.items = load_user_inventory(username)
                            in_game = True
                            show_movement_tip = True
                            movement_tip_alpha = 0
                            movement_tip_timer = 0

                            player_pos = [sun_center[0] - player_size[0] // 2, sun_center[1] - player_size[1] // 2]
                            player_vel = [0.0, 0.0]
                            surface_player_pos = [50, HEIGHT // 2]
                            surface_player_vel = [0.0, 0.0]

                            on_surface = False
                            in_fact_file = False
                            in_inventory = False
                            current_surface_name = None
                            feature_fact_active = False
                            active_feature_fact = None
                            active_planet = None
                            zoom = 1.0
                        else: # Invalid credentials
                            login_message = "Invalid credentials."
                    else: # Sign up mode
                        success, msg = register_user(username, password)
                        login_message = msg
                        if success:
                            input_username.clear()
                            input_password.clear()

                pygame.time.wait(200)
        else:
            screen.blit(button_default, button_rect.topleft)

        # Switch to Sign Up/Log In Button
        switch_text = "Switch to Sign Up" if login_mode == "sign_in" else "Switch to Log In"

        temp_label = default_font.render(switch_text, True, (0, 0, 0))
        switch_rect = temp_label.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 160))

        hovered = switch_rect.collidepoint((mouse_x, mouse_y))
        switch_color = (100, 200, 255) if hovered else (60, 120, 200)

        switch_label = default_font.render(switch_text, True, switch_color)
        screen.blit(switch_label, switch_rect)

        if hovered and mouse_clicked: # Switch login mode on click
            login_mode = "sign_up" if login_mode == "sign_in" else "sign_in"
            pygame.time.wait(200)
        
        if login_message.lower().startswith("welcome") or login_message.lower().startswith("user registered successfully"): # Success message
            msg_color = (100, 255, 100)
        else:
            msg_color = (255, 100, 100)

        message_render = default_font.render(login_message, True, msg_color)
        screen.blit(message_render, (WIDTH // 2 - message_render.get_width() // 2, HEIGHT // 3 + 200))

        if return_menu_button_rect.collidepoint((mouse_x, mouse_y)): # Return to home menu button
            screen.blit(return_menu_button_hover, return_menu_button_rect.topleft)
        else:
            screen.blit(return_menu_button, return_menu_button_rect.topleft)

        pygame.display.flip()
        continue
    
    # Help Screen Logic
    if in_help_screen:
        draw_parallax_bg()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        # Draw help screen texts
        help_title_font = pygame.font.Font(font_path, 60)
        help_title = help_title_font.render("Help", True, (255, 255, 255))
        help_title_rect = help_title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(help_title, help_title_rect)

        pygame.draw.line(screen, (150, 150, 150), (100, 160), (WIDTH - 100, 160), 2)

        objective_title_font = pygame.font.Font(font_path2, 32)
        objective_text_font = pygame.font.Font(font_path2, 24)

        objective_title = objective_title_font.render("Objective", True, (255, 255, 255))
        screen.blit(objective_title, (100, 180))

        objective_lines = [
            "> Press 'Play' and explore the Solar System!",
            "> When touching a celestial body, open fact files or explore their surfaces!",
            "> When in a fact file, read some facts about the celestial body!",
            "> When inside a surface, explore the surface and learn interesting facts on their unique features and collect unique items to add to your inventory"
        ]

        max_text_width = WIDTH - 200
        y_offset = 220

        for raw_line in objective_lines: # Wrap and render objective lines
            wrapped = wrap_text(raw_line, objective_text_font, max_text_width)
            for line in wrapped:
                rendered = objective_text_font.render(line, True, (200, 200, 200))
                screen.blit(rendered, (100, y_offset))
                y_offset += 30

        pygame.draw.line(screen, (150, 150, 150), (100, y_offset + 10), (WIDTH - 100, y_offset + 10), 2)
        y_offset += 30

        # Other Information Section
        other_title_font = pygame.font.Font(font_path2, 32)
        other_text_font = pygame.font.Font(font_path2, 24)

        other_title = other_title_font.render("Other", True, (255, 255, 255))
        screen.blit(other_title, (100, y_offset))
        y_offset += 40

        other_lines = [
            "> Press 'Login' to sign in or sign up to save your game progress!",
            "> Signing in and playing allows you to keep your collected items in your inventory",
            "> To view game controls, press 'Play' and click the menu button on the top right"
        ]

        for raw_line in other_lines: # Wrap and render other lines
            wrapped = wrap_text(raw_line, other_text_font, WIDTH - 200)
            for line in wrapped:
                rendered = other_text_font.render(line, True, (200, 200, 200))
                screen.blit(rendered, (100, y_offset))
                y_offset += 30

        if return_menu_button_rect.collidepoint((mouse_x, mouse_y)): # Return to home menu button
            screen.blit(return_menu_button_hover, return_menu_button_rect.topleft)
        else:
            screen.blit(return_menu_button, return_menu_button_rect.topleft)

        for event in events: # Handle events in help screen
            if event.type == pygame.QUIT: # Close the game
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Exit help screen with escape key
                in_help_screen = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_menu_button_rect.collidepoint(event.pos): # Return to home menu
                    play_button_click()
                    in_help_screen = False

        pygame.display.flip()
        continue

    # Confirm Exit Unsaved Message Logic
    if confirm_exit_unsaved:
        draw_parallax_bg()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        # Message Content
        local_title_font = pygame.font.Font(font_path, 42)
        local_sub_font = pygame.font.Font(font_path, 30)
        local_info_font = pygame.font.Font(font_path2, 22)
        local_button_font = pygame.font.Font(font_path2, 30)

        max_width = WIDTH - 100
        title_lines = wrap_text("Are you sure you want to exit session?", local_title_font, max_width)
        sub_lines = wrap_text("(Progress will not be saved)", local_sub_font, max_width)
        info_lines = wrap_text("To save game progress please sign in.", local_info_font, max_width)

        all_lines = [(line, local_title_font, (255, 255, 255)) for line in title_lines]
        all_lines += [(line, local_sub_font, (255, 100, 100)) for line in sub_lines]
        all_lines += [(line, local_info_font, (200, 200, 200)) for line in info_lines]

        spacing = 10
        total_height = sum(font.get_height() + spacing for _, font, _ in all_lines)
        y = HEIGHT // 2 - total_height // 2

        for text, font, color in all_lines: # Iterate through each text
            rendered = font.render(text, True, color)
            rect = rendered.get_rect(center=(WIDTH // 2, y))
            screen.blit(rendered, rect)
            y += font.get_height() + spacing

        # Yes/Cancel Button
        yes_default = (100, 200, 255)
        cancel_default = (100, 200, 255)

        yes_rect = pygame.Rect(0, 0, 100, 40)
        cancel_rect = pygame.Rect(0, 0, 120, 40)
        yes_rect.center = (WIDTH // 2 - 100, y + 30)
        cancel_rect.center = (WIDTH // 2 + 100, y + 30)

        yes_hover = (100, 255, 100) if yes_rect.collidepoint((mouse_x, mouse_y)) else yes_default
        cancel_hover = (255, 100, 100) if cancel_rect.collidepoint((mouse_x, mouse_y)) else cancel_default

        yes_text = local_button_font.render("Yes", True, yes_hover)
        cancel_text = local_button_font.render("Cancel", True, cancel_hover)

        screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
        screen.blit(cancel_text, cancel_text.get_rect(center=cancel_rect.center))

        for event in events:
            if event.type == pygame.QUIT: # Close the game
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_rect.collidepoint(event.pos): # Return to in home menu
                    play_button_click()
                    in_game = False
                    confirm_exit_unsaved = False
                elif cancel_rect.collidepoint(event.pos): # Return to in game menu
                    play_button_click()
                    in_menu = True
                    confirm_exit_unsaved = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Return to in game menu using 'esc' key
                in_menu = True
                confirm_exit_unsaved = False

        pygame.display.flip()
        continue

    # Surface Logic
    if on_surface and current_surface_name:
        keys = pygame.key.get_pressed()
        surface_acceleration = 0.6
        surface_friction = 0.9
        surface_max_speed = 6

        # Movement Logic
        moving = False
        if keys[pygame.K_w]:
            surface_player_vel[1] -= surface_acceleration
            player_image = player_images["up"]
            moving = True
        elif keys[pygame.K_s]:
            surface_player_vel[1] += surface_acceleration
            player_image = player_images["down"]
            moving = True
        if keys[pygame.K_a]:
            surface_player_vel[0] -= surface_acceleration
            player_image = player_images["left"]
            moving = True
        elif keys[pygame.K_d]:
            surface_player_vel[0] += surface_acceleration
            player_image = player_images["right"]
            moving = True
        if not moving:
            player_image = player_default

        # Apply friction and limit speed
        surface_player_vel[0] *= surface_friction
        surface_player_vel[1] *= surface_friction
        surface_player_vel[0] = max(-surface_max_speed, min(surface_max_speed, surface_player_vel[0]))
        surface_player_vel[1] = max(-surface_max_speed, min(surface_max_speed, surface_player_vel[1]))
        surface_player_pos[0] += surface_player_vel[0]
        surface_player_pos[1] += surface_player_vel[1]

        surface_player_pos[0] = max(0, min(WIDTH - player_size[0], surface_player_pos[0]))
        surface_player_pos[1] = max(0, min(HEIGHT - player_size[1], surface_player_pos[1]))

        screen.blit(pygame.transform.scale(surface_images[current_surface_name], (WIDTH, HEIGHT)), (0, 0))

        player_rect = pygame.Rect(surface_player_pos[0], surface_player_pos[1], player_size[0], player_size[1])
        mouse_pos = pygame.mouse.get_pos()

        if current_surface_name in surface_features: # Draw surface features
            player_rect = pygame.Rect(surface_player_pos[0], surface_player_pos[1], player_size[0], player_size[1])
            mouse_pos = pygame.mouse.get_pos()
            surface_features[current_surface_name].draw(screen, player_rect, mouse_pos)

            hovered_feature = surface_features[current_surface_name].get_hovered_feature()
            if hovered_feature: # Show feature fact box if hovering over a feature
                instruction_text = hover_instruction_font.render("(SPACE) - Open/Close Fact Box", True, (255, 255, 255))

                padding_x, padding_y = 10, 5
                bg_width = instruction_text.get_width() + padding_x * 2
                bg_height = instruction_text.get_height() + padding_y * 2
                instruction_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
                instruction_bg.fill((0, 0, 0, 180))

                space_blue = (20, 40, 100)
                pygame.draw.rect(instruction_bg, space_blue, instruction_bg.get_rect(), 2)

                bg_x = WIDTH // 2 - bg_width // 2
                bg_y = 20
                screen.blit(instruction_bg, (bg_x, bg_y))
                screen.blit(instruction_text, (bg_x + padding_x, bg_y + padding_y))

        for collectible in collectibles: # Draw collectibles on the surface
            if collectible.planet == current_surface_name: # Check if collectible is on the current surface
                collectible.draw(screen, player_rect, label_font)
        
        surface_player_rect = pygame.Rect(surface_player_pos[0], surface_player_pos[1], player_size[0], player_size[1])

        for collectible in collectibles: # Check if player can collect an item
            if collectible.planet == current_surface_name and collectible.is_available(): # Check if collectible is on the current surface and available
                if surface_player_rect.colliderect(collectible.rect): # Check if player collides with collectible
                    collect_text = hover_instruction_font.render("(C) - Collect Item", True, (255, 255, 255))

                    padding_x, padding_y = 10, 5
                    bg_width = collect_text.get_width() + padding_x * 2
                    bg_height = collect_text.get_height() + padding_y * 2
                    collect_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
                    collect_bg.fill((0, 0, 0, 180))

                    pygame.draw.rect(collect_bg, (20, 40, 100), collect_bg.get_rect(), 2)

                    bg_x = WIDTH // 2 - bg_width // 2
                    bg_y = 70
                    screen.blit(collect_bg, (bg_x, bg_y))
                    screen.blit(collect_text, (bg_x + padding_x, bg_y + padding_y))
                    break
        
        player_scaled = pygame.transform.smoothscale(player_image, player_size)
        screen.blit(player_scaled, surface_player_pos)

        if on_surface and show_tip and current_surface_name in eligible_collectible_planets: # Show tip if on a surface with collectibles
            tip_font = pygame.font.Font(font_path2, 26)
            tip_text = tip_font.render("Tip: Open all fact boxes to reveal a collectable item", True, (255, 255, 255))

            padding = 10
            tip_rect = tip_text.get_rect(topleft=(30 + padding, HEIGHT - 80 + padding))

            bg_rect = pygame.Rect(
                tip_rect.left - padding,
                tip_rect.top - padding,
                tip_rect.width + 2 * padding,
                tip_rect.height + 2 * padding
            )

            # Create semi-transparent background for tip
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.set_alpha(tip_alpha)
            bg_surface.fill((0, 0, 0, 180))

            text_surface = pygame.Surface(tip_text.get_size(), pygame.SRCALPHA)
            text_surface.set_alpha(tip_alpha)
            text_surface.blit(tip_text, (0, 0))

            screen.blit(bg_surface, (bg_rect.left, bg_rect.top))
            screen.blit(text_surface, tip_rect.topleft)

        if on_surface and show_item_added: # Show item added notification
            notify_font = pygame.font.Font(font_path2, 26)
            notify_text = notify_font.render("Item Added to Inventory", True, (255, 255, 255))

            padding = 10
            text_rect = notify_text.get_rect(topright=(WIDTH - 30 - padding, 30 + padding))
            bg_rect = pygame.Rect(
                text_rect.left - padding,
                text_rect.top - padding,
                text_rect.width + 2 * padding,
                text_rect.height + 2 * padding
            )

            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 160))
            screen.blit(bg_surface, bg_rect.topleft)

            pygame.draw.rect(screen, (100, 255, 100), bg_rect, 2)

            screen.blit(notify_text, text_rect.topleft)

        if feature_fact_active and active_feature_fact: # Show feature fact box
            raw_lines = feature_facts.get(
                active_feature_fact,
                ["Unknown feature.", "No data available."]
            )
            feature_title = active_feature_fact.replace("_", " ").title()
            
            box_margin = 40
            box_width = WIDTH // 3 - box_margin
            box_height = HEIGHT - 2 * box_margin
            box_x = WIDTH - box_width - box_margin
            box_y = box_margin

            pygame.draw.rect(screen, (20, 20, 20), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (100, 100, 255), (box_x, box_y, box_width, box_height), 2)

            y_offset = box_y + 20
            label = label_font.render(feature_title, True, (255, 255, 255))
            screen.blit(label, (box_x + 15, y_offset))
            y_offset += label.get_height() + 10

            max_text_width = box_width - 30
            line_spacing = 30

            divider_start = (box_x + 15, y_offset)
            divider_end = (box_x + box_width - 15, y_offset)
            pygame.draw.line(screen, (180, 180, 180), divider_start, divider_end, 2)
            y_offset += 20

            for raw_line in raw_lines: # Wrap and render feature fact lines
                wrapped_lines = wrap_text(raw_line, label_font, max_text_width)
                for i, wrap_line in enumerate(wrapped_lines): # Render each wrapped line
                    label = label_font.render(wrap_line, True, (255, 255, 255))
                    screen.blit(label, (box_x + 15, y_offset))
                    y_offset += line_spacing
                y_offset += 20 

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if solar_system_button_rect.collidepoint((mouse_x, mouse_y)): # Solar System button hover effect
            screen.blit(solar_system_button_hover, solar_system_button_rect.topleft)
        else:
            screen.blit(solar_system_button, solar_system_button_rect.topleft)

        if in_inventory: # Show inventory overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            inv_width = WIDTH * 0.8
            inv_height = HEIGHT * 0.6
            inv_x = (WIDTH - inv_width) // 2
            inv_y = (HEIGHT - inv_height) // 2
            inv_rect = pygame.Rect(inv_x, inv_y, inv_width, inv_height)

            player_inventory.draw(screen, label_font, inv_rect)

        for event in events: # Handle events in surface exploration mode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Exit surface exploration mode
                on_surface = False
                current_surface_name = None
                feature_fact_active = False
                active_feature_fact = None
            
            # Collect Item Logic
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                if current_surface_name == "Sun" and all(sun_fact_opened.values()) and not plasma_collected: # Check if all facts are opened
                    if player_rect.colliderect(plasma_rect): # Check if player collides with plasma item
                        plasma_collected = True
                        if not player_inventory.contains("plasma"): # Check if item is not already in inventory
                            play_item_collect()
                            player_inventory.add("plasma")
                            show_item_added = True
                            item_added_timer = 0
                            if current_user: # Save inventory if user is logged in
                                save_user_inventory(current_user, player_inventory.get_items())
                if current_surface_name == "Mercury" and all(mercury_fact_opened.values()) and not silicate_rock_collected:
                    if player_rect.colliderect(silicate_rock_rect):
                        silicate_rock_collected = True
                        if not player_inventory.contains("silicate_rock"):
                            play_item_collect()
                            player_inventory.add("silicate_rock")
                            show_item_added = True
                            item_added_timer = 0
                            if current_user:
                                save_user_inventory(current_user, player_inventory.get_items())
                if current_surface_name == "Venus" and all(venus_fact_opened.values()) and not basalt_collected:
                    if player_rect.colliderect(basalt_rect):
                        basalt_collected = True
                        if not player_inventory.contains("basalt"):
                            play_item_collect()
                            player_inventory.add("basalt")
                            show_item_added = True
                            item_added_timer = 0
                            if current_user:
                                save_user_inventory(current_user, player_inventory.get_items())
                if current_surface_name == "Earth" and all(earth_fact_opened.values()) and not leaf_collected:
                    if player_rect.colliderect(leaf_rect):
                        leaf_collected = True
                        if not player_inventory.contains("leaf"):
                            play_item_collect()
                            player_inventory.add("leaf")
                            show_item_added = True
                            item_added_timer = 0
                            if current_user:
                                save_user_inventory(current_user, player_inventory.get_items())
                if current_surface_name == "Mars" and all(mars_fact_opened.values()) and not blueberries_collected:
                    if player_rect.colliderect(blueberries_rect):
                        blueberries_collected = True
                        if not player_inventory.contains("blueberries"):
                            play_item_collect()
                            player_inventory.add("blueberries")
                            show_item_added = True
                            item_added_timer = 0
                            if current_user:
                                save_user_inventory(current_user, player_inventory.get_items())
                if current_surface_name == "Saturn" and all(saturn_fact_opened.values()) and not water_ice_collected:
                    if player_rect.colliderect(water_ice_rect):
                        water_ice_collected = True
                        if not player_inventory.contains("water_ice"):
                            play_item_collect()
                            player_inventory.add("water_ice")
                            show_item_added = True
                            item_added_timer = 0
                            if current_user:
                                save_user_inventory(current_user, player_inventory.get_items())
                if current_surface_name == "Uranus" and all(uranus_fact_opened.values()) and not methane_ice_collected:
                    if player_rect.colliderect(methane_ice_rect):
                        methane_ice_collected = True
                        if not player_inventory.contains("methane_ice"):
                            play_item_collect()
                            player_inventory.add("methane_ice")
                            show_item_added = True
                            item_added_timer = 0
                            if current_user:
                                save_user_inventory(current_user, player_inventory.get_items())
                if current_surface_name == "Pluto" and all(pluto_fact_opened.values()) and not frozen_nitrogen_collected:
                    if player_rect.colliderect(frozen_nitrogen_rect):
                        frozen_nitrogen_collected = True
                        if not player_inventory.contains("frozen_nitrogen"):
                            play_item_collect()
                            player_inventory.add("frozen_nitrogen")
                            show_item_added = True
                            item_added_timer = 0
                            if current_user:
                                save_user_inventory(current_user, player_inventory.get_items())

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Toggle feature fact box
                current_feature_set = surface_features.get(current_surface_name)
                if feature_fact_active: # Close feature fact box
                    feature_fact_active = False
                    active_feature_fact = None
                else: # Open feature fact box
                    if current_feature_set:
                        hovered = current_feature_set.get_hovered_feature()
                        if hovered: # Check if a feature is hovered
                            feature_fact_active = True
                            active_feature_fact = hovered["name"]
                            # Mark the fact as opened
                            if current_surface_name == "Sun" and active_feature_fact in sun_fact_opened:
                                sun_fact_opened[active_feature_fact] = True
                            if current_surface_name == "Mercury" and active_feature_fact in mercury_fact_opened:
                                mercury_fact_opened[active_feature_fact] = True
                            if current_surface_name == "Venus" and active_feature_fact in venus_fact_opened:
                                venus_fact_opened[active_feature_fact] = True
                            if current_surface_name == "Earth" and active_feature_fact in earth_fact_opened:
                                earth_fact_opened[active_feature_fact] = True
                            if current_surface_name == "Mars" and active_feature_fact in mars_fact_opened:
                                mars_fact_opened[active_feature_fact] = True
                            if current_surface_name == "Saturn" and active_feature_fact in saturn_fact_opened:
                                saturn_fact_opened[active_feature_fact] = True
                            if current_surface_name == "Uranus" and active_feature_fact in uranus_fact_opened:
                                uranus_fact_opened[active_feature_fact] = True
                            if current_surface_name == "Pluto" and active_feature_fact in pluto_fact_opened:
                                pluto_fact_opened[active_feature_fact] = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if solar_system_button_rect.collidepoint(event.pos): # Solar System button click
                    play_button_click()
                    on_surface = False
                    current_surface_name = None
                    feature_fact_active = False
                    active_feature_fact = None
                    break

                if feature_fact_active and active_feature_fact: # Check if clicking outside the fact box
                    box_margin = 40
                    box_width = WIDTH // 3 - box_margin
                    box_height = HEIGHT - 2 * box_margin
                    box_x = WIDTH - box_width - box_margin
                    box_y = box_margin
                    fact_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

                    if not fact_box_rect.collidepoint(event.pos): # Click outside the fact box
                        feature_fact_active = False
                        active_feature_fact = None
                else: # Check if clicking on a feature to open its fact box
                    current_feature_set = surface_features.get(current_surface_name)
                    if current_feature_set: # Check if there are features on the surface
                        hovered = current_feature_set.get_hovered_feature()
                        if hovered: # Check if a feature is hovered
                            feature_fact_active = True
                            active_feature_fact = hovered["name"]
        
        pygame.display.flip()
        continue
    
    # If not in game, draw the main menu
    if not in_game:
        draw_menu()
        continue

    # Fact File Logic
    if in_fact_file and active_planet:
        active_fact_file = fact_files[active_planet.name]
        active_fact_file.update_scroll(dt)
        active_fact_file.draw(screen, default_font)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if solar_system_button_rect.collidepoint((mouse_x, mouse_y)): # Solar System button hover effect
            screen.blit(solar_system_button_hover, solar_system_button_rect.topleft)
        else:
            screen.blit(solar_system_button, solar_system_button_rect.topleft)

        pygame.display.flip()
        continue
    
    # Inventory Logic
    if in_inventory:
        screen.fill((0, 0, 0))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if solar_system_button_rect.collidepoint((mouse_x, mouse_y)): # Solar System button hover effect
            screen.blit(solar_system_button_hover, solar_system_button_rect.topleft)
        else:
            screen.blit(solar_system_button, solar_system_button_rect.topleft)

        for event in events: # Handle events in inventory
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if solar_system_button_rect.collidepoint(event.pos): # Solar System button click
                    play_button_click()
                    in_inventory = False
                    pygame.time.wait(150)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Exit inventory with escape key
                in_inventory = False
        
        # Inventory UI
        divider_width = 900
        divider_x_start = (WIDTH - divider_width) // 2
        divider_y = 130

        inventory_title_font = pygame.font.Font(font_path, 60)
        inventory_title = inventory_title_font.render("Inventory", True, (255, 255, 255))
        inventory_title_rect = inventory_title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(inventory_title, inventory_title_rect)

        pygame.draw.line(screen, (150, 150, 150), (divider_x_start, divider_y), (divider_x_start + divider_width, divider_y), 2)

        item_x = 100
        item_y = 200
        items_per_row = 5
        item_spacing = 250

        # Draw Items in Inventory
        for index, item_name in enumerate(player_inventory.get_items()):
            if item_name == "plasma":
                item_img = pygame.image.load("inventory_items/plasma.png").convert_alpha()
                label_text = "Plasma"
            elif item_name == "silicate_rock":
                item_img = pygame.image.load("inventory_items/silicate_rock.png").convert_alpha()
                label_text = "Silicate Rock"
            elif item_name == "basalt":
                item_img = pygame.image.load("inventory_items/basalt.png").convert_alpha()
                label_text = "Basalt"
            elif item_name == "leaf":
                item_img = pygame.image.load("inventory_items/leaf.png").convert_alpha()
                label_text = "Leaf"
            elif item_name == "blueberries":
                item_img = pygame.image.load("inventory_items/blueberries.png").convert_alpha()
                label_text = "Blueberries"
            elif item_name == "water_ice":
                item_img = pygame.image.load("inventory_items/water_ice.png").convert_alpha()
                label_text = "Water Ice"
            elif item_name == "methane_ice":
                item_img = pygame.image.load("inventory_items/methane_ice.png").convert_alpha()
                label_text = "Methane Ice"
            elif item_name == "frozen_nitrogen":
                item_img = pygame.image.load("inventory_items/frozen_nitrogen.png").convert_alpha()
                label_text = "Frozen Nitrogen"
            else:
                continue

            item_img = pygame.transform.scale(item_img, (100, 100))

            # Grid Layout
            col = index % items_per_row
            row = index // items_per_row
            draw_x = item_x + col * item_spacing
            draw_y = item_y + row * item_spacing

            screen.blit(item_img, (draw_x, draw_y))
            label = default_font.render(label_text, True, (255, 255, 255))
            screen.blit(label, (draw_x + 50 - label.get_width() // 2, draw_y + 110))

        pygame.display.flip()
        continue
    
    # Update Game Logic
    for planet in planets:
        planet.update_position(sun_center, dt)

    acceleration = base_acceleration

    moving = False

    # Movement Logic
    if keys[pygame.K_w]:
        player_vel[1] -= acceleration
        player_image = player_images["up"]
        moving = True
    elif keys[pygame.K_s]:
        player_vel[1] += acceleration
        player_image = player_images["down"]
        moving = True
    if keys[pygame.K_a]:
        player_vel[0] -= acceleration
        player_image = player_images["left"]
        moving = True
    elif keys[pygame.K_d]:
        player_vel[0] += acceleration
        player_image = player_images["right"]
        moving = True
    if not moving:
        player_image = player_default

    # Apply friction and limit speed
    player_vel[0] *= friction
    player_vel[1] *= friction
    player_vel[0] = max(-max_speed, min(max_speed, player_vel[0]))
    player_vel[1] = max(-max_speed, min(max_speed, player_vel[1]))

    player_pos[0] += player_vel[0]
    player_pos[1] += player_vel[1]
    player_pos[0] = max(0, min(WORLD_WIDTH - player_size[0], player_pos[0]))
    player_pos[1] = max(0, min(WORLD_HEIGHT - player_size[1], player_pos[1]))

    camera_x = max(0, min(WORLD_WIDTH - WIDTH / zoom, player_pos[0] + player_size[0] / 2 - (WIDTH / (2 * zoom))))
    camera_y = max(0, min(WORLD_HEIGHT - HEIGHT / zoom, player_pos[1] + player_size[1] / 2 - (HEIGHT / (2 * zoom))))

    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
    
    for planet in planets: # Update planet touch states
        planet.update_touch_state(player_rect)

    sun_rect = pygame.Rect(sun_draw_pos[0], sun_draw_pos[1], sun_size[0], sun_size[1])
    sun_touched = sun_rect.colliderect(player_rect)
    if sun_touched: # If player touches  sun, set sun touched state
        try:
            sun_image = pygame.transform.scale(pygame.image.load("game_graphics/sun_touch.png").convert_alpha(), sun_size)
        except:
            pass
    else:
        sun_image = sun_default_image.copy()

    # Draw Background & Planets
    camera_rect = pygame.Rect(camera_x, camera_y, int(WIDTH / zoom), int(HEIGHT / zoom))
    camera_surface = pygame.Surface((int(WIDTH / zoom), int(HEIGHT / zoom)))
    camera_surface.blit(bg_image, (0, 0), camera_rect)
    scaled_surface = pygame.transform.smoothscale(camera_surface, (WIDTH, HEIGHT))
    screen.blit(scaled_surface, (0, 0))

    sun_screen_x = (sun_draw_pos[0] - camera_x) * zoom
    sun_screen_y = (sun_draw_pos[1] - camera_y) * zoom
    sun_scaled = pygame.transform.smoothscale(sun_image, (int(sun_size[0] * zoom), int(sun_size[1] * zoom)))
    screen.blit(sun_scaled, (sun_screen_x, sun_screen_y))

    for planet in planets: # Draw each planet
        planet.draw(screen, camera_x, camera_y, zoom)

    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])

    hovered_name = None
    for planet in planets: # Check if player is hovering over a planet
        planet_rect = pygame.Rect(planet.position[0], planet.position[1], planet.size[0], planet.size[1])
        if player_rect.colliderect(planet_rect):
            hovered_name = planet.name
            break

    sun_rect = pygame.Rect(sun_draw_pos[0], sun_draw_pos[1], sun_size[0], sun_size[1])
    sun_rect.inflate_ip(-40, -40)
    if player_rect.colliderect(sun_rect): # Check if player is hovering over sun
        hovered_name = "Sun"

    if hovered_name: # If hovering over planet or sun, draw hover box
        name_heading_font = pygame.font.Font(font_path2, 38)
        name_text = name_heading_font.render(hovered_name, True, (255, 255, 255))
        fact_text = hover_instruction_font.render("(F) Fact File", True, (200, 200, 200))
        explore_text = hover_instruction_font.render("(E) Explore", True, (200, 200, 200))

        structure_img = None
        try: # Attempt to load structure image for hovered planet
            structure_img = pygame.image.load(f"game_graphics/{hovered_name.lower()}_structure.png").convert_alpha()
            structure_img = pygame.transform.scale(structure_img, (120, 120))
        except:
            pass

        # Create Hover Box
        padding_x, padding_y = 10, 8
        text_width = max(name_text.get_width(), fact_text.get_width(), explore_text.get_width())
        image_height = structure_img.get_height() if structure_img else 0
        image_width = structure_img.get_width() if structure_img else 0

        box_width = max(text_width, image_width) + padding_x * 2
        box_height = (
            name_text.get_height() +
            fact_text.get_height() +
            explore_text.get_height() +
            image_height +
            padding_y * 5
        )

        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 180))
        pygame.draw.rect(box_surface, (20, 40, 100), box_surface.get_rect(), 2)

        box_surface.blit(name_text, ((box_width - name_text.get_width()) // 2, padding_y))
        box_surface.blit(fact_text, ((box_width - fact_text.get_width()) // 2, padding_y + name_text.get_height() + 4))
        box_surface.blit(explore_text, ((box_width - explore_text.get_width()) // 2, padding_y + name_text.get_height() + fact_text.get_height() + 8))

        if structure_img: # If structure image exists, draw it
            image_x = (box_width - structure_img.get_width()) // 2
            image_y = padding_y + name_text.get_height() + fact_text.get_height() + explore_text.get_height() + 12
            box_surface.blit(structure_img, (image_x, image_y))

        margin = 30
        box_x = margin
        box_y = HEIGHT - box_height - margin
        screen.blit(box_surface, (box_x, box_y))

    # Draw Player
    screen_x = (player_pos[0] - camera_x) * zoom
    screen_y = (player_pos[1] - camera_y) * zoom
    player_scaled = pygame.transform.smoothscale(player_image, (int(player_size[0] * zoom), int(player_size[1] * zoom)))
    screen.blit(player_scaled, (screen_x, screen_y))

    player_screen_center = (WIDTH // 2, HEIGHT // 2)

    # Arrow Drawing Logic
    if show_arrows:
        for obj in planets + [type("SunObject", (), {"position": sun_draw_pos})()]: # Include sun in arrow logic
            world_x, world_y = obj.position
            screen_x = (world_x - camera_x) * zoom
            screen_y = (world_y - camera_y) * zoom

            if not (0 <= screen_x <= WIDTH and 0 <= screen_y <= HEIGHT): # Check if object is off-screen
                dx = screen_x - player_screen_center[0]
                dy = screen_y - player_screen_center[1]
                angle = math.atan2(dy, dx)
                angle_deg = -math.degrees(angle)

                arrow_pos = clamp_to_screen_edge((screen_x, screen_y))
                rotated_arrow = pygame.transform.rotate(arrow_image, angle_deg)
                rotated_rect = rotated_arrow.get_rect(center=arrow_pos)
                screen.blit(rotated_arrow, rotated_rect.topleft)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Game Menu Open Logic
    if game_menu_button_rect.collidepoint((mouse_x, mouse_y)):
        screen.blit(game_menu_button_hover, game_menu_button_rect.topleft)
    else:
        screen.blit(game_menu_button, game_menu_button_rect.topleft)

    # Draw Player Username & Sign Out Button
    if in_game and not in_menu and not in_fact_file and current_user:
        username_text = default_font.render(f"Player: {current_user}", True, (255, 255, 255))
        screen.blit(username_text, (20, 20))

        if sign_out_button_rect.collidepoint((mouse_x, mouse_y)): # Sign Out button hover effect
            screen.blit(sign_out_button_hover, sign_out_button_rect.topleft)
        else:
            screen.blit(sign_out_button, sign_out_button_rect.topleft)

    # Inventory Button Hover Logic
    if in_game and not in_menu and not in_fact_file and not in_inventory:
        if inventory_button_rect.collidepoint((mouse_x, mouse_y)):
            screen.blit(inventory_button_hover, inventory_button_rect.topleft)
        else:
            screen.blit(inventory_button, inventory_button_rect.topleft)

    # Movement Tip Logic
    if show_movement_tip and movement_tip_alpha > 0:
        tip_text = default_font.render("(WASD) Move", True, (255, 255, 255))
        tip_surface = tip_text.copy()
        tip_surface.set_alpha(movement_tip_alpha)
        tip_rect = tip_text.get_rect(midtop=(WIDTH // 2, 20))
        screen.blit(tip_surface, tip_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()