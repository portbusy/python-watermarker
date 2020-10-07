# Import required Image library
from PIL import Image, ImageDraw, ImageFont
import argparse
from os import walk


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                        help='Absolute path to the folder with the images to be watermarked.',
                        required=True)
    parser.add_argument('--watermark',
                        help='Absolute path to the watermark file.',
                        required=True)
    parser.add_argument('--save',
                        help='Absolute path to save the watermarked images, default is the same folder of the images',
                        required=False)
    parser.add_argument('--show', help='If true will show the image after applying the watermark, default false',
                        default=False,
                        required=False)
    args = parser.parse_args()
    path = args.path
    if args.save:
        save_path = args.save
    else:
        save_path = f'{path}/watermarked'
    logo_path = args.watermark
    show = args.show
    skipList = ['404.png', 'default.jpg', 'logo45.png', 'logo.jpeg', 'logo45w.png', 'esp-dht.jpg']
    images = []
    dirs = []
    for (dirpath, dirnames, filenames) in walk(path):
        images.extend(filenames)
        dirs.extend(dirnames)
        break

    print(images, dirnames)

    for image in images:
        print(image)
        im = Image.open(f'{path}/{image}')
        width, height = im.size

        draw = ImageDraw.Draw(im)
        if 'logo' in image:
            # print(image)
            # text = "DB"
            # font = ImageFont.truetype('C:\Windows\Fonts\Montserrat-Bold.ttf', 10)
            # textwidth, textheight = draw.textsize(text, font)
            #
            # # calculate the x,y coordinates of the text
            # margin = 5
            # x = width - textwidth - margin
            # y = height - textheight - margin
            # if 'w.png' in image:
            #     color = '#000000'
            # else:
            #     color = '#ffffff'
            # # draw watermark in the bottom right corner
            # draw.text((x, y), text, font=font, fill=color)
            # im.show()
            # im.save(f'C:/Users/bertolottida/Desktop/img/{image}')
            pass

        else:
            try:
                if image not in skipList:
                    watermark = Image.open(logo_path).convert('RGBA');
                    mask = watermark.convert('L').point(lambda x: min(x, 8))
                    watermark.putalpha(mask)

                    watermark_width, watermark_height = watermark.size
                    main_width, main_height = im.size
                    aspect_ratio = watermark_width / watermark_height
                    new_watermark_width = main_width * 0.25
                    watermark.thumbnail((new_watermark_width, new_watermark_width / aspect_ratio), Image.ANTIALIAS)

                    tmp_img = Image.new('RGB', im.size)
                    for i in range(0, tmp_img.size[0], watermark.size[0]):
                        for j in range(0, tmp_img.size[1], watermark.size[1]):
                            im.paste(watermark, (i, j), watermark)
                            im.thumbnail((8000, 8000), Image.ANTIALIAS)
                            im.save(f'{save_path}/{image}', quality=100)
                    # add watermark to your image
                    if show:
                        im.show()
                else:
                    print('passed')
                    pass
            except:
                pass


if __name__ == '__main__':
    main()
