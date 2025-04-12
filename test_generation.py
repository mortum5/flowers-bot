import os
from flower_generator import generate_image

def test_generate_image():
    query = "Букет красивых свежих цветов"  # Russian: "Bouquet of beautiful fresh flowers"
    output_path = "test_output.png"
    generated_path = generate_image(query, output_path)
    assert os.path.exists(generated_path), "Image was not generated."
    print("Test passed, image generated at", generated_path)
    
if __name__ == '__main__':
    test_generate_image()
