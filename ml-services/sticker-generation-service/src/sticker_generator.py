"""Mock sticker generator for testing caching system"""

import time
import random
import io
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont


class StickerGenerator:
    """Mock sticker generator for testing cache implementation"""
    
    def __init__(self, width: int = 512, height: int = 512):
        """Initialize sticker generator
        
        Args:
            width: Width of generated stickers
            height: Height of generated stickers
        """
        self.width = width
        self.height = height
        print(f"Initialized mock sticker generator ({width}x{height})")
    
    def generate(self, prompt: str, **kwargs) -> bytes:
        """Generate a sticker based on the provided prompt
        
        Args:
            prompt: Text prompt for sticker generation
            **kwargs: Additional generation parameters
            
        Returns:
            Generated sticker as bytes
        """
        # Simulate processing time that would be required for real generation
        # Real diffusion models would take much longer
        processing_time = random.uniform(1.0, 3.0)
        print(f"Generating sticker for prompt: '{prompt}'")
        print(f"Using parameters: {kwargs}")
        print(f"Simulating diffusion model processing...")
        time.sleep(processing_time)  # Simulate processing time
        
        # Create a simple colored image with the prompt text
        # In a real implementation, this would call the diffusion model
        image = Image.new('RGB', (self.width, self.height), color=self._get_color_from_prompt(prompt))
        
        # Add text to the image
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("Arial.ttf", 24)
        except IOError:
            # Fallback to default
            font = ImageFont.load_default()
            
        # Draw prompt text
        text_position = (20, 20)
        draw.text(text_position, f"Prompt: {prompt}", fill=(255, 255, 255), font=font)
        
        # Add some random shapes to make each image unique
        for _ in range(10):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            fill = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw.ellipse((x1, y1, x2, y2), fill=fill)
            
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        print(f"Generated sticker: {len(img_bytes)} bytes")
        
        return img_bytes
    
    def _get_color_from_prompt(self, prompt: str) -> Tuple[int, int, int]:
        """Generate a background color based on the prompt"""
        # Simple hashing of the prompt to get consistent colors for the same prompt
        hash_value = hash(prompt)
        r = (hash_value & 0xFF0000) >> 16
        g = (hash_value & 0x00FF00) >> 8
        b = hash_value & 0x0000FF
        return (abs(r), abs(g), abs(b))