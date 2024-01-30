import os
import pygame
import copy
import re

def load_images(folder):
  images = {} # files in 1 same class, e.g. class Button or class Cloud
  for filename in os.listdir(folder):
    if filename.endswith('.png') or filename.endswith('.jpg'):
      file = pygame.image.load(os.path.join(folder, filename)).convert_alpha() #convert_alpha to preserve color quality
      button_name = filename.split('.')[0]
      images[button_name] = file
  return images

class Button(): # attributes and behaviors for all buttons
  def __init__(self, image, x, y, scale): # image = filename; pos = center position coordinates
      self.image = pygame.transform.scale_by(image, scale)
      #draw a rectangular area in the size of the image, starting from coordinates (x,y)
      #self.scale = pygame.transform.scale_by(self.image, scale)
      self.rect = self.image.get_rect(center=(x, y))
      self.is_clicked = False

  def draw(self, surface): #draw the buttons
      surface.blit(self.image, self.rect.center)
  def click(self):
      action = False
      mouse_pos = pygame.mouse.get_pos()
      if self.rect.collidepoint(mouse_pos): # check if mouse hovers over the button
        # click when the left mouse button is pressed and the button hasn't activated yet
          if pygame.mouse.get_pressed()[0] == 1 and self.is_clicked == False: # not MOUSEBUTTONDOWN because this is outside the event loop
              self.is_clicked = True
              action = True
          elif pygame.mouse.get_pressed()[0] == 0:
              self.is_clicked = False
      
      return action #bool variable

class Text: #class for instructional texts on the screen
  def __init__(self, content, scale_factor, bg_color, color, font_size): 
    self.content = content
    self.scale_factor = scale_factor
    self.bg_color = bg_color
    size = font_size * self.scale_factor
    self.font = pygame.font.Font(None, size)
    self.color = color

  def display_text_wrapped(self, x,y, multiline:bool, truncated:bool, surface): # surface = SCREEN or another textbox
#create a surface on the text box of which height is equal to the number of lines
    if len(self.content)>120:
      if multiline:
        lines = []
        k = re.sub("#","\n",copy.copy(self.content))
        sentences = k.split('\n')
        for i in sentences:
            lines_per_s = [i[j:j + 90] for j in range(0, len(i), 90)] # cut sentences into 90 letters and the remaining part
            lines += lines_per_s
      
        '''
        new_lines = []
        text = re.findall('.{90}', self.content)
        re_string = rf'?<={text[-1]}'
        final_sent = re.search(re_string, self.content)
        for i in text:
          k = copy.copy(i) + '\n'
          k = re.sub("#","\n",k)
          new_lines.append(k)
        new_lines.append(final_sent)
        lines = ' '.join(new_lines).split('\n') # in case there are more \n symbols in some text
      '''
    elif not multiline or len(self.content)<=120:
      lines = [copy.copy(self.content)]
      if truncated:
        for j in lines:
          lines.append(j[:100].append('[...]')) # When truncated, the text will only show 1 line
       
    
    displayed = []
    total_height = 0

    for i in range(len(lines)):
        rendered_line = self.font.render(lines[i], False, self.color, self.bg_color)
        displayed.append(rendered_line)
        _, line_height = self.font.size(lines[i])
        total_height += line_height

    text_box_surface = pygame.Surface((self.font.size(lines[0])[0]+200, total_height))
    text_box_surface.fill(self.bg_color)

    for t in range(len(displayed)):
        text_box_surface.blit(displayed[t], (0, t * line_height))

    # Blit the whole text box onto the screen
    surface.blit(text_box_surface, (x, y))
    return surface #surface var is now type Rect, if surface != SCREEN, we'll have to blit this onto the SCREEN later
