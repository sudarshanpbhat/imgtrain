import argparse
from PIL import Image

DEFAULT_BORDER_SIZE = 20
DEFAULT_SPACE_BETWEEN_IMAGES = 20

# Returns a tuple containg the output image's width and height 
def get_output_image_size(file_list, border_size, space_between_images): 
  output_image_width = 0
  output_image_height = 0
  for filename in file_list: 
    with (Image.open(filename, 'r')) as image: 
      width, height = image.size
      output_image_width += width
      output_image_height = height

  # Adjust for borders and space between images
  output_image_width += 2 * border_size + (len(file_list) - 1) * space_between_images
  output_image_height += 2 * border_size
  return output_image_width, output_image_height

# Merges image into a bigger image of specified size 
def merge_images(output_image_width, output_image_height, file_list, border_size, space_between_images, background_color): 
  output_image = Image.new('RGB', (output_image_width, output_image_height), background_color)
  width_offset = border_size
  height_offset = border_size
  for filename in file_list:
    with (Image.open(filename, 'r')) as image: 
      width, height = image.size 
      output_image.paste(image, (width_offset, height_offset))
      width_offset += width + space_between_images
  return output_image

# Entry point. Main function. 
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('image_files', nargs='+', type=argparse.FileType('r'))
  parser.add_argument('--bg-color', default='#EEEEEE', help="Set the background image color")
  parser.add_argument('--border-size', default=20, help="Set the border size.", type=int)
  parser.add_argument('--space-between-images', default=20, help="Set space between images.", type=int)
  parser.add_argument('-o', '--output', default='output.jpeg', help="Set output file name.", type=argparse.FileType('w'))
  args = parser.parse_args()

  # Get list of files passed as arguments
  file_list = []
  for argument in args.image_files: 
    file_list.append(argument.name)

  # Get border size and space between images
  border_size = args.border_size
  space_between_images = args.space_between_images

  # Get background color
  background_color = args.bg_color

  output_image_width, output_image_height = get_output_image_size(file_list, border_size, space_between_images)
  output_image = merge_images(output_image_width, output_image_height, file_list, border_size, space_between_images, background_color)

  # Get output file name
  output_file_name = args.output.name 
  output_image.save(output_file_name)


if (__name__ == "__main__"):
  main()