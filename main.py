import hashlib
from PIL import Image, ImageDraw

def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

defaultSize = 5000
inputSize = input('Size of image? [5000]')

size = defaultSize

if inputSize:
    if int(inputSize) < defaultSize:
        print('The given size cannot be smaller than 5000')
        exit(1)
    elif not int(inputSize) % 2 == 0:
        print('The given size must be an even number')
        exit(1)
    else:
        size = int(inputSize)

print(f'Size has been set to {size}')

key = input('Key? (Entering the same key will give you the same image)')

if not key:
    print('No key was given')
    exit(1)

hash = hashlib.sha512(key.encode('UTF-8')).hexdigest()
data_hash = hashlib.sha512(key[::-1].encode('UTF-8')).hexdigest()

bg_color = hash[:6]
primary_color = hash[6:12]
secondary_color = hash[12:18]
tertiary_color = hash[18:24]
data = hash[24:]

canvas = Image.new('RGB', (size, size), hex_to_rgb(bg_color))
image = ImageDraw.Draw(canvas)

n = 10
data_chunks = [data[i:i+n] for i in range(0, len(data), n)]

multi = size / defaultSize

previous_coord = (0, 0)

def process_chunk(chunk):
    color = chunk[:1]
    pos_x = int(chunk[1:3], 16) * multi * 1.6 * 10
    pos_y = int(chunk[3:5], 16) * multi * 1.6 * 10
    size_w = int(chunk[5:7], 16) / 3 * multi * 10
    size_h = int(chunk[7:9], 16) / 3 * multi * 10

    selected_color = hex_to_rgb(primary_color)
    color_number = int(color, 16)

    global previous_coord

    if color_number > 3:
        if color_number % 3 == 0:
            selected_color = hex_to_rgb(tertiary_color)
        if color_number % 3 == 1:
            selected_color = hex_to_rgb(primary_color)
        if color_number % 3 == 2:
            selected_color = hex_to_rgb(secondary_color)

    if not previous_coord == (0, 0):
        image.line((pos_x + size_w / 2, pos_y + size_h / 2, previous_coord[0], previous_coord[1]), selected_color, int(20 * multi))
    
    previous_coord = (pos_x + size_w / 2, pos_y + size_h / 2)

    image.ellipse((pos_x, pos_y, pos_x + size_w, pos_y + size_h), selected_color)


for chunk in data_chunks:
    if len(chunk) == n:
        process_chunk(chunk)

data_hash_chunks = [data_hash[i:i+n] for i in range(0, len(data_hash), n)]

for chunk in data_hash_chunks:
    if len(chunk) == n:
        process_chunk(chunk)

canvas.save('output.png', 'png')

print('Finished creating image.')
