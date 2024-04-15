import os
import subprocess
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from common import seconds_to_string
from config import Config


class Renderer:
    def __init__(self, parent):
        self.parent = parent
        self.metadata = parent.metadata
        try:
            self.font = Config.values['font']
        except KeyError:
            self.parent.logger.log('required parameter "font" not provided. Check config.json or use the --font '
                                   'parameter.')
            raise

    def initialize(self):
        args = ['ffmpeg', '-i', self.metadata.fname, 'cover.png']
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
        if not os.path.exists('cover.png'):
            self.parent.logger.log('cover extraction error. Ignoring.')
            return

        cover = Image.open('cover.png')
        cover.thumbnail((200, 200))
        bcover = cover.filter(ImageFilter.GaussianBlur(15))
        bcover = bcover.resize((1920, 1080))
        bcover.save('cover2.png')

        image = Image.open('cover2.png')
        rgba = Image.new('RGBA', image.size, (255, 255, 255, 0))
        rgba.paste(image)
        rgba.save('cover3.png')
        image.close()

        topgradient = Image.new('RGBA', (1, 320), '#919191AE')
        draw = ImageDraw.Draw(topgradient)
        for x in range(18):
            color = int(145 + (255 - 145) / 18 * x)
            alpha = int(174 / 18 * (18 - x))
            draw.point([0, 302 + x], fill=(color, color, color, alpha))
        topgradient = topgradient.resize((1920, 320))

        image = Image.open('cover3.png')
        image.alpha_composite(topgradient)
        image.paste(cover, (60, 60))
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(self.font, size=88)
        draw.text((300, 35), str(self.metadata.title), font=font, fill='#FFFFFF')
        font = ImageFont.truetype(self.font, size=44)
        draw.text((300, 151), self.metadata.artist, font=font, fill='#EDEDED')
        draw.text((300, 208), self.metadata.album, font=font, fill='#EDEDED')

        font = ImageFont.truetype(self.font, size=36)
        text = seconds_to_string(self.metadata.length)
        size = font.getbbox(text)
        draw.text((1880 - size[2] + size[0], 360 - size[3] + size[1]),
                  text,
                  font=font, fill='#DDDDDD')
        image.convert('RGB').save('base.jpg')

    def generate_frame(self, frame_num):
        seconds = frame_num / self.parent.fps
        length = self.metadata.length
        image = Image.open('base.jpg')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font, size=36)
        text = seconds_to_string(seconds, length)
        size = font.getbbox(text)
        draw.text((40, 360 - size[3] + size[1]), text, font=font)
        draw.rectangle((0, 310, (seconds / length) * 1920, 320), fill='#FFFFFF', width=0)
        return image
