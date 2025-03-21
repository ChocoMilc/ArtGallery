import os
import json
from PIL import Image
from PIL.ExifTags import TAGS

def get_image_metadata(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif() or {}
        metadata = {TAGS.get(tag, tag): value for tag, value in exif_data.items() if tag in TAGS}
        return {
            "name": os.path.basename(image_path),
            "path": image_path.replace("\\", "/"),
            "description": metadata.get("ImageDescription", "No description available"),
            "author": metadata.get("Artist", "Unknown")
        }

def generate_html(images_metadata, output_file="gallery.html"):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Art Gallery</title>
        <style>
            body { background-color: #121212; color: white; font-family: 'Georgia', serif; text-align: center; margin: 0; padding: 0; }
            h1 { font-size: 3rem; margin: 20px 0; }
            .gallery { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 40px; }
            .image-container {
                position: relative;
                width: 340px;
                border: 8px solid #666;
                border-radius: 12px;
                overflow: hidden;
                background: #1e1e1e;
                padding: 15px;
                transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
                box-shadow: 0 10px 30px rgba(255, 255, 255, 0.1);
            }
            .image-container:hover {
                transform: scale(1.08);
                box-shadow: 0 15px 40px rgba(255, 255, 255, 0.2);
                border-color: #888;
            }
            img {
                width: 100%;
                border-radius: 8px;
                border: 5px solid #777;
                transition: transform 0.3s ease-in-out, border-color 0.3s ease-in-out;
            }
            img:hover { transform: scale(1.02); border-color: #aaa; }
            .image-title { font-size: 22px; margin-top: 10px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
            .image-description { font-size: 16px; margin-top: 8px; opacity: 0.9; font-style: italic; }
            .author {
                position: absolute;
                bottom: 15px;
                right: 15px;
                opacity: 0;
                font-size: 14px;
                font-weight: bold;
                transition: opacity 0.3s ease-in-out;
                color: #ddd;
            }
            .image-container:hover .author { opacity: 1; transition-delay: 1.5s; }
        </style>
    </head>
    <body>
        <h1>Art Gallery</h1>
        <div class="gallery">
    """

    for image in images_metadata:
        html_content += f"""
        <div class="image-container">
            <div class="image-title">{image['name'].replace(".png","").replace('_best','')}</div>
            <img src="{image['path']}" alt="{image['name']}" title="{image['author']}">
            <div class="image-description">{image['description']}</div>
            <div class="author">By: {image['author']}</div>
        </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

def main(directory):
    images_metadata = [get_image_metadata(os.path.join(directory, file)) for file in os.listdir(directory) if file.lower().endswith((".jpg", ".jpeg", ".png"))]
    generate_html(images_metadata)

if __name__ == "__main__":
    main("images")  # Change to your image directory
