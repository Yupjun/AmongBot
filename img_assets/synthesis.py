import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import random

home_dir = 'C:\\Users\\Jisu\\Desktop\\Amongus-Bot-main\\Amongus-Bot-main\\img_assets'
output_dir = os.path.join(home_dir, 'output')

def choose_background():
    background_dir = os.path.join(home_dir, 'skeld_map_bg')
    background_random = random.choice(os.listdir(background_dir))
    background = cv2.imread(os.path.join(background_dir, background_random))
    return background_random, background

def choose_character():
    character_dir = os.path.join(home_dir, 'characters')
    character_color_random = random.choice(os.listdir(character_dir))
    character_final_random = random.choice(os.listdir(os.path.join(character_dir, character_color_random)))
    print(os.path.join(character_dir, character_color_random, character_final_random))
    character = cv2.imread(os.path.join(character_dir, character_color_random, character_final_random), cv2.IMREAD_UNCHANGED)

    character_resize = cv2.resize(character, dsize = (100,150)) # 캐릭터 사이즈
    return character_resize

def overlay_transparent(background, overlay, x, y):
    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background


background_id, background = choose_background()

for i in range(30):
    if i == 0:
        output = background
    ch = choose_character()
    x = random.randint(0, 1280)
    y = random.randint(0, 798)
    output = overlay_transparent(output, ch, x, y)
    cv2.imwrite(os.path.join(output_dir, str(background_id) + '_' + str(i) + '.png'), output)