# Import necessary libraries and modules
import sys
import pygame
from pygame.locals import QUIT
import tkinter as tk
import threading
from PIL import Image
from random import randint

# Import the program modules and classes
import main_class
import os
from text_process_module import text_process
import program_module
from program_module import program

# Declaring folders, templates, and dictionaries for the modules
bg_folder = 'images/bg_cloud'
txt_folders = "original_txt"
csv_folder = "csv"
info_template = {
    'title': 'title',
    'author_sur': 'author\'s surname',
    'author_init': 'author initials (w/o surname)',
    'vol': 'volume',
    'publ_year': 'publication year',
    'publ': 'publisher',
    'editn': 'edition',
    'start_section': 'start_section',
    'end_section': 'end_section',
    'filename': 'filename'
}

output_folder = 'output'
rule_dict = {
    "defined": 1,
    "definition": 1,
    " refers ": 2,
    " refer ": 2,
    " means ": 2,
    " mean ": 2,
    " imply ": 3,
    " implies ": 3,
    " implied ": 3,
    " can be ": 4
}
output_dir = {
    "all_books": "output/all_books.csv",
    "sent_def": "output/sent_def.csv",
    "sent_other": "output/sent_other.csv",
    "keyword": "output/keyword.csv"
}
text_process = text_process()
program_module = program(bg_folder=bg_folder,
                         txt_folders=txt_folders,
                         info_template=info_template,
                         rule_dict=rule_dict,
                         output_folder=output_folder,
                         output_dir=output_dir,
                         text_process=text_process)

# Ask the user if they need to preprocess before starting
if program_module.is_preprocess():
  program_module.preprocess()

# Initialize Pygame session and its global variables
pygame.init()
SCREEN = pygame.display.set_mode((1200, 800))
# The clock serves to assign the program's frame refresh rate, instead of freely updating whenever possible
CLOCK = pygame.time.Clock()
BG_SCREEN = pygame.image.load('images/bg_screen/3065.jpg')
FONT_SIZE = round(SCREEN.get_height() / 30)
input_font = pygame.font.Font(None, FONT_SIZE)

# Set up window caption and the font
pygame.display.set_caption('GPDS - Greek Philosophy Definition Search')
pygame.font.init()

#Behaviour for each button


#Function for the Definition Search button
def ds_btn_func(input_text, output_textbox):
  output_textbox.fill((255, 255, 255))
  program_output_txt = program_module.get_definition(str(input_text))
  displayed_output = main_class.Text(str(program_output_txt), 1,
                                     (255, 255, 255), (0, 0, 0), FONT_SIZE)
  show = displayed_output.display_text_wrapped(10, 5, True, True,
                                               output_textbox)
  is_cloud = True

  return program_output_txt, show, is_cloud  # show is a type Rect variable


#Function for the Word Cloud button
def wc_btn_func(input_text):

  bg_folder = 'images/bg_cloud'
  bg_dir = [
      os.path.join(bg_folder, t) for t in os.listdir(bg_folder)
      if t.endswith(".jpg")
  ]
  bg = (bg_dir[randint(0, 2)])  #click again to change the cloud background
  contains_keyword = program_module.get_wordcloud(str(input_text), bg)

  if contains_keyword == False:
    print('No occurrences of the keyword ' + str(input_text) + ' found.')
    is_cloud = False
    return is_cloud

  else:
    #Create plot image and save file into output folder
    cloud_result_files = [
        f'{output_folder}/{t}' for t in os.listdir(output_folder)
        if t.endswith(".png")
    ]
    program_output_pic = cloud_result_files[-1]
    #Open image with PIL, then convert into pygame surface
    image = Image.open(program_output_pic)
    #Maintain the size and color/res modes by convert()
    show = pygame.image.fromstring(image.tobytes(), image.size,
                                   image.mode).convert()
    is_cloud = True

  return program_output_pic, show, is_cloud


#Function for the Save button
def save_btn_func(is_cloud, program_output_txt):

  def save_pic():
    # Open tkinter window to select files, then close the window
    root = tk.Tk()
    root.withdraw()
    root.file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files",
                                                                 "*.txt"),
                                                                ("All files",
                                                                 "*.*")])
    if root.file_path:
      with open(root.file_path, 'w') as file:
        file.write(program_output_txt)
      print(f"File saved at: {root.file_path}")

  if is_cloud == False:
    thread = threading.Thread(target=save_pic)
    thread.start()
  else:
    print("Image saved to the output folder.")


# Define the placement and image source of buttons
button_images = main_class.load_images("images/buttons")
save_btn = main_class.Button(button_images['btn_3'], 700, 100, 1)
ds_btn = main_class.Button(button_images['btn_5'], 300, 80, 1)
wc_btn = main_class.Button(button_images['btn_6'], 300, 155, 1)


# Main event loop
def main():

  running = True
  input_text = ''
  show = ''
  program_output_pic = ''

  while running:
    SCREEN.blit(BG_SCREEN, (0, 0))
    save_btn.draw(SCREEN)
    ds_btn.draw(SCREEN)
    wc_btn.draw(SCREEN)

    pygame.mouse.set_visible(True)
    #Draw the input textbox: a small space for text input
    input_textbox = pygame.Surface((200, 100))
    input_textbox.fill((0, 0, 0))
    SCREEN.blit(input_textbox, (50, 80))
    #Draw the output textbox: a white box for both text and image output
    output_textbox = pygame.Surface((1000, 500))
    output_textbox.fill((255, 255, 255))
    SCREEN.blit(output_textbox, (100, 225))

    #Display instruction texts on the screen
    instruct_text_1 = main_class.Text(
        "Enter your keyword, then click on DEFINITION or WORD CLOUD to try out!",
        1, (255, 255, 255), (22, 22, 22), FONT_SIZE)
    instruct_text_1.display_text_wrapped(50, 27, False, False, SCREEN)

    instruct_text_2 = main_class.Text(
        "Press a button above to clear the screen and try a new output.", 1,
        (255, 255, 255), (22, 22, 22), FONT_SIZE)
    instruct_text_2.display_text_wrapped(300, 760, False, False, SCREEN)

    # Pygame event handler, including mouse, keyboard and button presses
    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
        pygame.quit()
        sys.exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          input_text = ''  # Clear input when press Esc
        elif event.key == pygame.K_BACKSPACE and input_text != '':
          input_text = input_text[:
                                  -1]  # Remove the last character on Backspace
        else:
          input_text += event.unicode

      if ds_btn.click():
        program_output_txt = ''  #clear txt before running
        program_output_txt, show, is_cloud = ds_btn_func(
            input_text, output_textbox)
      elif wc_btn.click():
        program_output_txt = ''  #clear txt again
        program_output_pic, show, is_cloud = wc_btn_func(input_text)
      elif save_btn.click():
        save_btn_func(is_cloud, program_output_txt)
    '''The text surface and output image display must be handled in the main event loop, 
        or else they would make the program loop unnecessarily'''
    text_surface = input_font.render(input_text, True, (0, 255, 255),
                                     (0, 0, 0))
    SCREEN.blit(text_surface, (55, 85))
    if type(program_output_pic) != str:
      print('Image saved in the output folder.')
    if type(show) == pygame.surface.Surface:
      SCREEN.blit(show, (100, 225))

    CLOCK.tick(60)  #Program runs at 60 fps

    #Update the screen
    pygame.display.update()


if __name__ == '__main__':
  main()
