import argparse
import logging

from configs import Config
from watermark import WaterMarker

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_dir', default="config",
                        metavar='configuration_directory', type=str,
                        help='Configuration directory to use; if not specified, '
                             'default config directory will be used')
    # Configuration file
    parser.add_argument('-f', '--config_file', default="application.ini",
                        metavar='configuration_file', type=str,
                        help='Configuration file to use; if not specified, '
                             'default configs will be used')
    parser.add_argument('--path',
                        help='Absolute path to the folder with the images to be watermarked.',
                        required=True)
    parser.add_argument('--watermark_path',
                        help='Absolute path to the watermark file.',
                        required=True)
    parser.add_argument('--save_path',
                        help='Absolute path to save the watermarked images, default is the same folder of the images',
                        required=False)
    parser.add_argument('--show', help='If true will show the image after applying the watermark, default false',
                        default=False,
                        required=False)
    args = parser.parse_args()
    config_dir = args.config_dir
    config_file = args.config_file
    Config.init(config_dir, config_file)

    path = args.path
    watermark_path = args.watermark_path
    show = args.show

    if args.save_path:
        save_path = args.save_path
    else:
        save_path = f'{path}/watermarked'

    watermarker = WaterMarker(
        path=path,
        watermark_path=watermark_path,
        save_path=save_path,
        show=show
    )

    watermarker.create_watermarked_image()
