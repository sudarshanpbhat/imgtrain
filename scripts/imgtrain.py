import argparse
from PIL import Image, ImageDraw, ImageFont
import os

DEFAULT_BORDER_SIZE = 30
DEFAULT_SPACE_BETWEEN_IMAGES = 30
DEFAULT_BACKGROUND_COLOR = "#eeeeee"
DEFAULT_OUTPUT_FILE = "output.jpeg"
DEFAULT_FONT = "../fonts/Roboto-Medium.ttf"
DEFAULT_CAPTION_FONT_SIZE = 60
DEFAULT_CAPTION_FONT_COLOR = "#000000"

class ImageData: 
  def __init__(self, filename, configuration): 
    self.filename = filename
    self.configuration = configuration

    with (Image.open(self.filename, 'r')) as image: 
      self.width, self.height = image.size
    self.text_width, self.text_height = self.configuration.font.getsize(self.get_filename())

  def get_filename(self): 
    filename, _ = os.path.splitext(os.path.basename(self.filename))
    return filename


class Configuration: 
  def __init__(self, args): 
    self.bg_color = args.bg_color
    self.border_size = args.border_size
    self.space_between_images = args.space_between_images
    self.caption_filenames = args.caption_filenames
    self.caption_fontcolor = args.caption_fontcolor
    self.caption_fontsize = args.caption_fontsize
    self.font = ImageFont.truetype(DEFAULT_FONT, self.caption_fontsize)

  @staticmethod
  def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('image_files', nargs='+', type=argparse.FileType('r'))
    parser.add_argument('--bg-color', default=DEFAULT_BACKGROUND_COLOR, help="Set the background image color")
    parser.add_argument('--border-size', default=DEFAULT_BORDER_SIZE, help="Set the border size.", type=int)
    parser.add_argument('--caption-filenames', help="Set to show filenames as captions in the output image", action='store_true')
    parser.add_argument('--caption-fontcolor', default=DEFAULT_CAPTION_FONT_COLOR, help="Set caption text color. Applicable only when --caption_filenames is set.")
    parser.add_argument('--caption-fontsize', default=DEFAULT_CAPTION_FONT_SIZE, help="Set caption text size. Applicable only when --caption_filenames is set.", type=int)
    parser.add_argument('--space-between-images', default=DEFAULT_SPACE_BETWEEN_IMAGES, help="Set space between images.", type=int)
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT_FILE, help="Set output file name.", type=argparse.FileType('w'))
    return parser.parse_args()


class CollageBuilder: 
  def __init__(self, images, configuration): 
    self.images = images
    self.configuration = configuration
    self.output_image_width, self.output_image_height = self.get_output_image_size()

  def get_output_image_size(self): 
    # Add image sizes considering they're horizontally placed
    output_image_width = 0
    output_image_height = 0
    max_text_height = 0
    for image in self.images: 
      output_image_width += image.width
      output_image_height = image.height if image.height > output_image_height else output_image_height
      max_text_height = image.text_height if image.text_height > max_text_height else max_text_height


    # Adjust for borders and space between images
    output_image_width += 2 * self.configuration.border_size + (len(self.images) - 1) * self.configuration.space_between_images
    output_image_height += 2 * self.configuration.border_size

    # Adjust for text height. Add extra border when text is enabled
    if self.configuration.caption_filenames: 
      output_image_height += max_text_height + self.configuration.border_size

    return output_image_width, output_image_height

  def build(self): 
    output_image = Image.new('RGB', (self.output_image_width, self.output_image_height), self.configuration.bg_color)
    width_offset = self.configuration.border_size
    height_offset = self.configuration.border_size
    for item in self.images:
      with (Image.open(item.filename, 'r')) as image: 
        # Draw screenshot
        width, height = image.size 
        output_image.paste(image, (width_offset, height_offset))

        # Draw text
        if self.configuration.caption_filenames:
          text_draw = ImageDraw.Draw(output_image)
          text_width_offset = width_offset + ((width - item.text_width) / 2)
          text_height_offset = self.output_image_height - item.text_height - self.configuration.border_size
          text_draw.text((text_width_offset, text_height_offset), item.get_filename(), font=self.configuration.font, fill=self.configuration.caption_fontcolor)

        # Update offset for next image
        width_offset += width + self.configuration.space_between_images
    return output_image


# Entry point. Main function. 
def main():
  # Configuration
  args = Configuration.parse_args()
  config = Configuration(args)

  # Image list
  image_list = []
  for image_file in args.image_files: 
    image_list.append(ImageData(image_file.name, config))

  # Create aggregate image
  imgTrain = CollageBuilder(image_list, config)
  output_image = imgTrain.build()

  # Save output
  output_file_name = args.output.name 
  output_image.save(output_file_name)


if (__name__ == "__main__"):
  main()