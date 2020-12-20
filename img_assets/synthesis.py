# %%
import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import random

# home_dir = 'C:\\Users\\Jisu\\Desktop\\Amongus-Bot-main\\Amongus-Bot-main\\img_assets'
home_dir = './'
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

def make_mask(character):
    '''
    character: [H, W, 4]
    '''
    H, W, _ = character.shape
    new_mask = character[..., 3].copy()
    half_H, half_W = H//2, W//2

    # Coordinate
    x = np.linspace(-half_W, half_W, W+1)
    y = np.linspace(-half_H, half_H, H+1)
    xv, yv = np.meshgrid(x[:W], y[:H])
    
    # weight, bias
    w, b = random.randint(-5, 5), random.randint(-15, 15)
    fx = w*x[:W]+b 
    
    # upper? bottom?
    bottom = random.randint(0,1)
    for idx in range(len(fx)):
        if bottom:
            new_mask[:, idx][yv[:, idx]<=fx[idx]] = 128
        else:
            new_mask[:, idx][yv[:, idx]>=fx[idx]] = 128

    return new_mask

def paste_transparency(background, character, x, y, w, h):
    bg_copy = background.copy()
    
    character_image = character[..., :3]
    chracter_mask = np.equal(character[..., 3:], 255, dtype=np.uint8)
    transparency_mask = np.equal(character[..., 3:], 128, dtype=np.uint8)
    
    paste_bg = (1.0 - chracter_mask) * (1.0 - transparency_mask) * bg_copy[y:y+h, x:x+w]
    paste_ch = chracter_mask * character_image
    paste_transparency = (transparency_mask * np.maximum(0, np.int16(bg_copy[y:y+h, x:x+w])-75))
    
    # Paste character
    bg_copy[y:y+h, x:x+w] = paste_bg + paste_ch + paste_transparency

    return bg_copy

def overlay_transparent(background, overlay, x, y):
    '''
    background: Main Image
    overlay: Character
    x, y: Coordinate
    '''
    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    # 벗어나는 부분 잘라내기
    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    # RGB일 경우 Alpha 채널 추가
    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    mode = random.randint(0, 2)

    if mode==0:
        # Basic Paste    
        overlay_image = overlay[..., :3]
        mask = overlay[..., 3:] / 255.0

        background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image
    
    elif mode==1:
        overlay[..., -1] = make_mask(overlay)
        background = paste_transparency(background, overlay, x, y, w, h)
    
    elif mode==2:
        # Apply Image Blending
        overlay_image = overlay[..., :3]
        mask = overlay[..., 3:] / 255.0
        overlay_image[mask[..., 0] == 0] = 0
        result = cv2.addWeighted(background[y:y+h, x:x+w], 0.5, (mask * overlay_image).astype(np.uint8),0.5, 0)
        background[y:y+h, x:x+w, :3] = result

    else:
        return background

    return background


background_id, background = choose_background()

# Paste Character
n_clones = 30
for i in range(n_clones):
    if i == 0:
        output = background.copy()
    ch = choose_character()
    x = random.randint(0, 1280)
    y = random.randint(0, 798)
    output = overlay_transparent(output, ch, x, y)
    cv2.imwrite(os.path.join(output_dir, str(background_id) + '_' + str(i) + '.png'), output)
# %%
