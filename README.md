# py trojan tool
Library for creating GDI-malwares in python
Fork of [Python-gdi-repo](https://github.com/Leo-Aqua/Python-gdi-repo/) with many new features!  
idea - [Rewrite as module](https://github.com/Leo-Aqua/Python-gdi-repo/discussions/5)  
Some of code wrote by chatgpt (like custom message box) and may not work (this is AI, lol)

## run gdi
```
from pytrojantool import run_gdi, GDIeffect, clean, get_size, get_user32
from pytrojantool.collection import tunnel

try:
    run_gdi([GDIeffect(tunnel, 0, -1, 0.1)]) #0 - start time, -1 - end time (-1 for infinity), 0.1 - delay
except KeyboardInterrupt:
    clean(get_size(get_user32())) #clean screen
```

## Functions
- Message boxes 
- Python-GDI-repo as library (collection.py)  
- New GDI effects from c++ trojans source code
- MBR overwriting
- Add files to startup
- Icon effects (work in progress)  
- Image effects (soon)  
- Text effects (soon)  
- extra features (like shutdown, bluescreen, custom gdi runner, etc)

## Soon
- Complete icon enums
- Add image support
- Add text support
- Add wallpaper changer
- More gdi effects
- Rewrite get_gdi_data function
- Payload creating (Payload class, inside gdi effetcs (custom of from collection), can edit start and stop time on every payload)
You can ask to add new feature creaint issue!

 > [!IMPORTANT]
> ## DISCLAIMER
> Don't be a skid. Do not use any of the code in this repo for harm.
> I do not take responsibility for any damages.
