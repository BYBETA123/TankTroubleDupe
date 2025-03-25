import shutil
import os
import glob

NAME_OF_FILE = "Flanki"



def clean_build_folders():
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("Removed the 'build' folder.")
    
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("Removed the 'dist' folder.")
    
    spec_files = glob.glob('*.spec')
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"Removed the '{spec_file}' file.")
    
# Run the cleanup
clean_build_folders()

# Run the build command
data_to_add = ["Sounds", "Assets", "Sprites", "fonts"]

# Generate the string for the command
pyinstallerCommand = 'pyinstaller'

pyinstallerCommand += ' --onefile' # One file
pyinstallerCommand += ' --noconfirm' # No confirmation
pyinstallerCommand += ' --name \"' + NAME_OF_FILE # Name of the executable
pyinstallerCommandWin = pyinstallerCommand + 'Windows\"' # Windows
pyinstallerCommandMac = pyinstallerCommand + 'MacOS\"' # Mac and Linux
pyinstallerCommandLinux = pyinstallerCommand + 'Linux\"' # Mac and Linux

for data in data_to_add:
    pyinstallerCommandWin += ' --add-data \"' + data + ';' + data + '\"' # Add data for windows
    pyinstallerCommandMac += ' --add-data \"' + data + ':' + data + '\"' # Add data for mac and linux
    pyinstallerCommandLinux += ' --add-data \"' + data + ':' + data + '\"' # Add data for mac and linux

pyinstallerCommandWin += ' main.py' # Add the main file
pyinstallerCommandMac += ' main.py' # Add the main file
pyinstallerCommandLinux += ' main.py' # Add the main file

# Run the command
os.system(pyinstallerCommandWin)
os.system(pyinstallerCommandMac)
os.system(pyinstallerCommandLinux)