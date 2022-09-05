# Tkinter-Notesy
This is a notetaking app made using tkinter.

## Manual
![Untitled](https://user-images.githubusercontent.com/97748294/188282962-101705aa-09e6-4aca-9be4-45a4d3af6aa8.png)

## Key Bindings

`OPT-BackSpace` : There is no official support for OPT-BackSpace for tkinter.text. This keybinding adds it.

`CMD-=`/`CMD--` : This keybinding allows font increase and decrease. The default fontsize gets restored every session. (If you wish to change the default size, edit `self.font=13` in 'tkinter notetakingapp.py' *BEFORE* using pyinstaller) 

## Installing the app

To install this program as an executable use pyinstaller inside of the cloned repo. As of now only targeted for MacOs:

`pyinstaller --noconfirm --windowed --icon=icons/icon.png -n Notesy  --clean --distpath . --add-data Icons/:Icons tkinter\ notetakingapp.py'`

Afterwards delete `Build`, `Notesy.spec` or simply everything else that *ISN'T* Notesy.app.
