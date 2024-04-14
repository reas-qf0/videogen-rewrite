import os
import subprocess
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from common import seconds_to_string


class Renderer:
    def __init__(self, parent):
        self.parent = parent
        self.metadata = parent.metadata
        self.top_gradient = '/media/yoo/Новый том/progaming/videogen-rewrite/resources/topgradient.png'
        self.font = '/media/yoo/Новый том/progaming/videogen-rewrite/resources/Arial Unicode MS.ttf'

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

        image = Image.open('cover3.png')
        image.alpha_composite(Image.open(self.top_gradient))
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