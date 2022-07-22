import logging
import os
from PIL import Image, UnidentifiedImageError

from config import config

LOGGER = logging.getLogger(__name__)


class WaterMarker:

    def __init__(self, path, watermark_path, save_path, show):
        self._path = path
        self._watermark_path = watermark_path
        self._save_path = save_path
        self._show = show
        self._images = eval(config.IMAGES.get())
        self._dirs = eval(config.DIRS.get())
        self._skip_list = eval(config.SKIP_LIST.get())

    def create_watermarked_image(self):
        """
        Create a watermarked image with the parameters found in the configuration file
        :return:
        :rtype:
        """
        filenames = next(os.walk(self._path), (None, None, []))[2]
        for root, dirs, files in os.walk(os.path.normpath(self._path)):
            print(root, "consumes", end="")

            print("bytes in", len(files), "non-directory files")
            self._images.extend(files)
            self._dirs.extend(dirs)
        LOGGER.debug(f'Images: {self._images}, Directories: {self._dirs}, {filenames}')

        for image in self._images:
            try:
                im = Image.open(f'{self._path}/{image}')
                if 'logo' in image:
                    # TODO: add custom text to the image
                    """
                    width, height = im.size
    
                    draw = ImageDraw.Draw(im)
                    """
                    pass
                else:
                    if image not in self._skip_list:
                        watermark = Image.open(self._watermark_path).convert('RGBA')
                        mask = watermark.convert('L').point(lambda x: min(x, 8))
                        watermark.putalpha(mask)

                        watermark_width, watermark_height = watermark.size
                        main_width, main_height = im.size
                        aspect_ratio = watermark_width / watermark_height
                        new_watermark_width = main_width * 0.25
                        watermark.thumbnail((new_watermark_width, new_watermark_width / aspect_ratio), Image.ANTIALIAS)
                        if not os.path.exists(self._save_path):
                            os.makedirs(self._save_path)
                        tmp_img = Image.new('RGB', im.size)
                        for i in range(0, tmp_img.size[0], watermark.size[0]):
                            for j in range(0, tmp_img.size[1], watermark.size[1]):
                                im.paste(watermark, (i, j), watermark)
                                im.thumbnail((8000, 8000), Image.ANTIALIAS)
                                im.save(f'{self._save_path}/{image}', quality=100)
                        # add watermark to your image
                        if self._show:
                            im.show()
                    else:
                        LOGGER.warning(f'Image {image} in skip list, moving to the next one')
                        pass
            except UnidentifiedImageError:
                LOGGER.error(f'Cannot open image {image}: invalid format')
            except Exception as e:
                LOGGER.error(f'Error while watermarking the image {image}: {e}')

        LOGGER.info(f'All watermarked images saved to {self._save_path}')
