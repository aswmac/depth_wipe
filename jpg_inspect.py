from PIL import Image, ExifTags

def inspect_jpg(filepath):
    try:
        img = Image.open(filepath)
        print(f"Format: {img.format}")
        print(f"Size: {img.size}")
        print(f"Mode: {img.mode}")
        print("nBasic Info:")
        print(f"Filename: {filepath}")
        print(f"Width: {img.width}, Height: {img.height}")
        
        # Extract EXIF metadata
        exif_data = img._getexif()
        if exif_data:
            print("nEXIF Metadata:")
            for tag_id, value in exif_data.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                # Skip binary data
                if isinstance(value, bytes):
                    continue
                print(f"{tag}: {value}")
        else:
            print("nNo EXIF metadata found.")
            
        # Additional info (if available)
        print("nAdditional Info:")
        for key, value in img.info.items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Error: {e}")

# Usage
inspect_jpg("your_image.jpg")

