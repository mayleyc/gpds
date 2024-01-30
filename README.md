# Welcome to GPDS - Greek Philosophy Definition Search!
GPDS - Greek Philosophy Definition Search program

by Nguyen Hoa Quynh Nhung and Tran Nguyen Anh Thu (CiMEC)

Course: Introduction to Computer Programming (Python) - Sep 2023

1. REQUIREMENTS:

- Computer with 8GB RAM and above (The program works on a 4GB machine; however, the Save function is not guaranteed with low RAM, due to running a tkinter thread in parallel.)

NB: Server computers will most likely not work, since this program requires a computer with a display window for pygame.

- A code editor + a Python >=3.9 interpreter to avoid incompatibility.
  
- It is recommended to create a new virtual environment (either with conda or venv) and install the packages in the requirements_pip.txt file.

2. INSTALL:
   
- Download the package from Github and unzip as a folder. Open this folder in your code editor.
  
- Open up main.py.
  
- Create a new virtual environment. To install all necessary libraries, type in the terminal:
  
	pip install -r requirements.txt (either pip or pip3), then press Enter.

3. RUNNING MAIN.PY:
   
- BEFORE RUNNING: The program allows for customization by replacing asset images and .txt files of your choice.
  
	+ All ebooks for use must be .txt files and placed in the original_txt folder.

	  It is advisable to use .txt ebooks from Gutenberg. For non-Gutenberg books, the user may also manually append a false Gutenberg-style header at the beginning with the correct book title, author name and publication year before preprocessing, since the program can auto-detect these mandatory data.
  
	+ New images should use the original name, size (they do not auto-scale), and the same file type.

- Run the program by typing in the terminal:
	python main.py (either python or python3)
  
- When prompted, press Y (in caps) to preprocess the texts first, or Enter to run the program as is.

	+ PREPROCESS: Press Y again to confirm.

		- After locating the .txt files, the program will prompt the user to enter some information. Firstly, each file must be confirmed whether it is a Gutenberg-style ebook or not. If so, the user should select Y (yes) for this book. If not, select N (no) and enter mandatory details manually. The mandatory data must not be skipped, since they are used to generate the data structure.
  
		- Optional data (after the program has auto-detected mandatory data) can be skipped by pressing Enter. After gathering book information, the program will preprocess the text into 4 .csv files, and then open the program window.

	+ MAIN PROGRAM:

		- Press either Definition or Word Cloud to initiate a process. Pressing either button afterwards, or pressing the same button again will clear the existing output. However, word clouds are still saved in the output folder for every new cloud output.
  
		- To make outputs more interesting, results after each time will be randomized in some way. For text, the program may pick some new sentences (if available). For word clouds, the color and cloud shape might be different.
  
		- Click Save to export your text result into a .txt file to the location of choice. The program opens up a tkinter window where you can save the file as any file name or file type (default .txt). This does not apply to images, since they are already saved in the output folder. There will be a message in the terminal to confirm whenever your outputs have been saved.
  
		- Close the program by clicking the top-right X button.

4. Data used, with links:
   
* List of books used from Gutenberg:
  
WARNING: Project Gutenberg is not accessible from Italy. The .txt files used for processing are available in the txt_original folder.

- A Short History of Greek Philosophy (Marshall J., 1891) - https://www.gutenberg.org/files/20500
  
- A Critical History of Greek Philosophy (Stace W.T., 1920) - https://www.gutenberg.org/files/33411
  
- Early Greek Philosophy & Other Essays (Nietzsche F.W., 1911; Levy O. ed.; Mügge M.A. tr.) - https://www.gutenberg.org/files/51548
  
- The Greek Philosophers, Vol. 1 (Benn A.W., 1882) - https://www.gutenberg.org/files/57126
  
- The Greek Philosophers, Vol. 2 (Benn A.W., 1882) - https://www.gutenberg.org/files/58224
