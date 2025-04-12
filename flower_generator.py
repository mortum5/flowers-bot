import os
import time
import argparse
from PIL import Image
from googletrans import Translator
import torch
from diffusers import StableDiffusionPipeline

def generate_image(query: str, output_path: str = "generated_flower_bouquet.png") -> str:
    # Translate the Russian query to English.
    translator = Translator()
    translated_query = translator.translate(query, dest='en').text
    prompt = f"Realistic photo of a flower bouquet, {translated_query}"
    
    # Choose the device: use "mps" if available on your MacBook M1 Pro; otherwise fallback to CPU.
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    
    # Load Stable Diffusion model. Here we use the model optimized for realistic images.
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe = pipe.to(device)
    
    # Generate the image with reasonable settings.
    result = pipe(prompt, guidance_scale=7.5, num_inference_steps=50)
    image = result.images[0]
    image.save(output_path)
    return output_path

# This allows the module to run directly from the command line.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a realistic flower bouquet image.")
    parser.add_argument('--query', type=str, required=True, help='Description of the bouquet in Russian')
    parser.add_argument('--output', type=str, default="generated_flower_bouquet.png", help='Output image file path')
    args = parser.parse_args()
    
    start_time = time.time()
    output = generate_image(args.query, args.output)
    print(f"Image saved to {output} in {time.time()-start_time:.2f} seconds")
