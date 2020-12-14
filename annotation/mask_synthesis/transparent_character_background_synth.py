import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

home_dir = 'C:\\Users\\Jisu\\Desktop\\annotation\\mask_synthesis'
background_dir = os.path.join(home_dir, 'background\\factory1.jpg')
character_dir = os.path.join(home_dir, 'character\\yellow-real.png')
#character_layer_dir = os.path.join(home_dir, 'character\\green_layer.png')
output_dir = os.path.join(home_dir, 'output')

character = cv2.imread(character_dir, cv2.IMREAD_UNCHANGED)
character_resize = cv2.resize(character,dsize = (200,400)) # 캐릭터 사이즈
#character_layer = cv2.imread(character_layer_dir)
background = cv2.imread(background_dir)

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

output = overlay_transparent(background, character_resize, 200, 200)
cv2.imwrite('output.png',output)