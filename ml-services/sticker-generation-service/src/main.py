"""Main Module for the Sticker Generation Service"""

from diffusion_model import generate_image_from_prompt
from utils import create_sticker, show_sticker_from_image

def main():
    '''main function'''
    prompt = input("Enter prompt:")
    image = generate_image_from_prompt(prompt)
    sticker = create_sticker(image)
    show_sticker_from_image(sticker, prompt)

if __name__ == "__main__":
    main()