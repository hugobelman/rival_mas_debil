# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 11:20:24 2021

@author: hugob
"""

import shutil
from pynput import keyboard
from PIL import Image, ImageFont, ImageDraw 

def change_question():
    global q_user, no_q, names
    
    if q_user == 1:
        q_user = 2
    else:
        q_user = 1
        if no_q < 5:
            no_q += 1
        else:
            no_q = 0

def render_bank():
    image = Image.open(bank_graphic)
    edit = ImageDraw.Draw(image)
    
    if bank > 99:
        x = 86
    elif bank > -1 and bank < 10:
        x = 118
    else:
        x = 100
        
    edit.text((x,73), f"${bank}", (255, 255, 255), font=font)
    image.save("bank.png")

MAX_LEVEL = 9
prizes = [0,2,4,8,10,20,40,80,100]

graphics_folder = "graphics"
prize_level_grahpic = "level.png"
bank_graphic = graphics_folder+"/bank.png"
font = ImageFont.truetype('font.ttf', 60)
questions_folder = "questions_g"
                         
prize_level = 1
bank = 0
final_prize = 0
q_user = 1
no_q = 1
names = ['P1', 'P2']

shutil.copyfile(f"{graphics_folder}/HUD_1.png", prize_level_grahpic)
render_bank()

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    
    global prize_level, bank, final_prize, q_user, no_q, names
    
    if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.shift_r, keyboard.Key.page_down, keyboard.Key.pause]:
        current_prize_level = prize_level
        current_bank = bank
        
        if key == keyboard.Key.up:
            if (prize_level < MAX_LEVEL):
                prize_level += 1
            else:
                prize_level = 1
        elif key == keyboard.Key.down:
            if (prize_level > 1):
                prize_level -= 1
            else:
                prize_level = MAX_LEVEL
        elif key == keyboard.Key.shift_r:
            to_add = prizes[prize_level-1]
            
            if bank + to_add > 100:
                bank = 100
            else:
                bank += to_add
                
            prize_level = 1       
            print(f"+{to_add}")
        elif key == keyboard.Key.page_down:
            prize_level = 1
            print("lose")
        elif key == keyboard.Key.pause:
            prize_level = 1
            print("=======================================")
            print("ROUND ENDED")
            print("round bank =",bank)
            final_prize += bank
            bank = 0
            print("final_prize =",final_prize)
            print("\n")
            
        print(f"level={prize_level}, bank={bank}")
        
        if prize_level != current_prize_level:
            shutil.copyfile(f"{graphics_folder}/HUD_{prize_level}.png", prize_level_grahpic)
        
        if bank != current_bank:
            render_bank()
    elif key in [keyboard.Key.f10, keyboard.Key.end, keyboard.Key.home]:      
        if key == keyboard.Key.f10:
            with open("names.txt", 'r', encoding = 'utf-8') as f:
                names = f.read().split(",")
                
            q_user = 1
            no_q = 1
            
            for i in range(1,6):
                shutil.copyfile(f"{graphics_folder}/std.png", f"{questions_folder}/u1_q{i}.png")
                shutil.copyfile(f"{graphics_folder}/std.png", f"{questions_folder}/u2_q{i}.png")
        elif key == keyboard.Key.end:
            shutil.copyfile(f"{graphics_folder}/incorrect.png", f"{questions_folder}/u{q_user}_q{no_q}.png")
            
            change_question()
            
        elif key == keyboard.Key.home:
            shutil.copyfile(f"{graphics_folder}/correct.png", f"{questions_folder}/u{q_user}_q{no_q}.png")
            
            change_question()
        
        print(f"{names[q_user-1]} Q{no_q}: Correcto: [Inicio] y Incorrecto [Fin]")
    #else:
    #    pass
    #    print(key)

print("Welcome to 'El rival más salsa'")

listener = keyboard.Listener(on_release=on_release)
listener.start()
listener.join() 


