import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def set_image_metadata(image_path, description, artist):
    with Image.open(image_path) as img:
        exif_data = img.info.get("exif")
        if not exif_data:
            exif_data = img.getexif()

        exif_dict = {TAGS.get(tag, tag): value for tag, value in exif_data.items() if tag in TAGS}

        # Update metadata
        exif_dict["ImageDescription"] = description
        exif_dict["Artist"] = artist

        # Save updated metadata
        exif_bytes = img.getexif()
        exif_bytes[270] = description  # 270 is ImageDescription
        exif_bytes[315] = artist  # 315 is Artist

        img.save(image_path, exif=exif_bytes)

def edit_metadata(directory):
    for file in os.listdir(directory):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(directory, file)
            with Image.open(image_path) as img:
                exif_data = img.getexif()
                description = exif_data.get(270, "No description available")
                artist = exif_data.get(315, "Unknown")

            print(f"Editing {file}")
            print(f"Current Description: {description}")
            new_description = input("Enter new description (leave blank to keep current): ")
            if not new_description:
                new_description = description

            print(f"Current Artist: {artist}")
            new_artist = input("Enter new artist (leave blank to keep current): ")
            if not new_artist:
                new_artist = artist

            set_image_metadata(image_path, new_description, new_artist)
            print("Metadata updated successfully!\n")

edit_metadata("images")
