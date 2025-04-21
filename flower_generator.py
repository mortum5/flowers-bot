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

    # Choose the best available device (CUDA for Windows with NVIDIA GPU).
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load Stable Diffusion model.
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe = pipe.to(device)

    # Generate the image.
    result = pipe(prompt, guidance_scale=7.5, num_inference_steps=50)
    image = result.images[0]

    # Ensure output directory exists.
    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
    image.save(output_path)
    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a realistic flower bouquet image.")
    parser.add_argument('--query', type=str, required=True, help='Description of the bouquet in Russian')
    parser.add_argument('--output', type=str, default="generated_flower_bouquet.png", help='Output image file path')
    args = parser.parse_args()

    start_time = time.time()
    output = generate_image(args.query, args.output)
    print(f"Image saved to {os.path.abspath(output)} in {time.time()-start_time:.2f} seconds")
