from PIL import Image

height=int(input('Enter image Height: '))
width=int(input('Enter image length'))
try:
    img=Image.open('abc.png')
    rotated_img=img.resize(size=[height,width])
    rotated_img.save('resized_image.png')
    print('Image resized Successfully.')
except Exception as e:
    print(e)