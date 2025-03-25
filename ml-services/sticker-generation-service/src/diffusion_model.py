""" Diffusion model for generating images from prompts """
import torch
from diffusers import StableDiffusionXLPipeline


def generate_image_from_prompt(prompt):
    """ Generate an image from a prompt using the diffusion model """
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16
    )
    pipe = pipe.to("cuda")
    pipe.batch_size = 1

    image = pipe(prompt).images[0]
    return image