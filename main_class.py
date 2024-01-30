import os
import pygame
import copy
import re


# Load images from the same folder, e.g. Button or Cloud Background
def load_images(folder):
  images = {}
  for filename in os.listdir(folder):
    if filename.endswith('.png') or filename.endswith('.jpg'):
      #Load image with the convert_alpha option to preserve color quality
      file = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
      button_name = filename.split('.')[0]
      images[button_name] = file
  return images


# Attributes and behaviors for all buttons
class Button():

  def __init__(self, image, x, y,
               scale):  # image = filename; pos = center position coordinates
    self.image = pygame.transform.scale_by(image, scale)
    #draw a Rect object in the size of the image, in order to detect mouse collision
    self.rect = self.image.get_rect(center=(x, y))
    self.is_clicked = False

  #Draw the buttons
  def draw(self, surface):
    surface.blit(self.image, self.rect.center)

  def click(self):
    action = False
    mouse_pos = pygame.mouse.get_pos()
    # Check if mouse hovers over the button
    if self.rect.collidepoint(mouse_pos):
      # Click when the left mouse button is pressed and the button hasn't activated yet
      if pygame.mouse.get_pressed()[0] == 1 and self.is_clicked == False:
        self.is_clicked = True
        action = True
      elif pygame.mouse.get_pressed()[0] == 0:
        self.is_clicked = False

    return action  #bool variable


#Class for instructional texts on the screen
class Text:

  def __init__(self, content, scale_factor, bg_color, color, font_size):
    self.content = content
    self.scale_factor = scale_factor
    self.bg_color = bg_color
    size = font_size * self.scale_factor
    self.font = pygame.font.Font(None, size)
    self.color = color


#Function to display "wrapped" text: each line does not exceed 120 letters

  def display_text_wrapped(self, x, y, multiline: bool, truncated: bool,
                           surface):  # surface = SCREEN or a textbox
    #Create a surface on the text box of which height is equal to the number of lines
    if len(self.content) > 120:
      if multiline:
        lines = []
        k = re.sub("#", "\n", copy.copy(self.content))
        sentences = k.split('\n')
        # Cut sentences into 90 letters per line, and keep the modulo as the last line.
        for i in sentences:
          lines_per_s = [i[j:j + 90] for j in range(0, len(i), 90)]
          lines += lines_per_s

    elif not multiline or len(self.content) <= 120:
      lines = [copy.copy(self.content)]
      # When truncated, the text will only show 1 line
      if truncated:
        for j in lines:
          lines.append(j[:100].append('[...]'))

    #Create a separate text surface for each line of text, then stack them onto each other
    displayed = []
    total_height = 0

    for i in range(len(lines)):
      rendered_line = self.font.render(lines[i], False, self.color,
                                       self.bg_color)
      displayed.append(rendered_line)
      _, line_height = self.font.size(lines[i])
      total_height += line_height

    text_box_surface = pygame.Surface(
        (self.font.size(lines[0])[0] + 200,
         total_height))  # +200 pixels to avoid missing text on the right
    text_box_surface.fill(self.bg_color)

    for t in range(len(displayed)):
      text_box_surface.blit(displayed[t], (0, t * line_height))

    # Blit the whole text box onto the screen
    surface.blit(text_box_surface, (x, y))
    return surface
    #The 'surface' variable is now type Rect.
    #If surface != SCREEN, the program will blit this onto the SCREEN in the main.py file
