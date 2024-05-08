from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

class VisitorIDCardGenerator:
    @staticmethod
    def generate(visitor_name, visitor_image_path):
        # Download the image from the URL
        response = requests.get(visitor_image_path)
        if response.status_code != 200:
            raise Exception("Failed to download image")
        
        # Open the image from the downloaded content
        visitor_image = Image.open(BytesIO(response.content))

        id_card = Image.new('RGB', (856, 539), color='white')
        id_card.paste(visitor_image, (100, 100))

        draw = ImageDraw.Draw(id_card)

        # Use default font
        font = ImageFont.load_default()

        draw.text((100, 20), f"visitor_name: {visitor_name}", fill='black', font=font)
        draw.text((400, 20), f"TEMPORARY VISITOR PASS", fill='black', font=font)

        id_card_buffer = BytesIO()
        id_card.save(id_card_buffer, format='PNG')

        id_card_buffer.seek(0)  # Move the buffer cursor to the beginning

        return id_card_buffer


# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

# class VisitorIDCardGenerator:
#     @staticmethod
#     def generate(visitor_name, visitor_image_path):
#         visitor_image = Image.open(visitor_image_path)

#         id_card = Image.new('RGB', (856, 539), color='white')
#         id_card.paste(visitor_image, (100, 100))

#         draw = ImageDraw.Draw(id_card)

#         # Use default font
#         font = ImageFont.load_default()

#         draw.text((100, 20), f"visitor_name: {visitor_name}", fill='black', font=font)
#         draw.text((400, 20), f"TEMPORARY VISITOR PASS", fill='black', font=font)

#         id_card_buffer = BytesIO()
#         id_card.save(id_card_buffer, format='PNG')

#         id_card_buffer.seek(0)  # Move the buffer cursor to the beginning

#         return id_card_buffer


# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

# class VisitorIDCardGenerator:
#     @staticmethod
#     def generate(visitor_name, visitor_image_path):
#         visitor_image = Image.open(visitor_image_path)

#         id_card = Image.new('RGB', (856, 539), color='white')
#         id_card.paste(visitor_image, (100, 100))

#         draw = ImageDraw.Draw(id_card)

#         # Use default font
#         font = ImageFont.load_default()

#         draw.text((100, 20), f"visitor_name: {visitor_name}", fill='black', font=font)
#         draw.text((400, 20), f"TEMPORARY VISITOR PASS", fill='black', font=font)

#         id_card_buffer = BytesIO()
#         id_card.save(id_card_buffer, format='PNG')

#         return id_card_buffer


# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

# class VisitorIDCardGenerator:
#     @staticmethod

#     def generate (visitor_name, visitor_image_path):

#         visitor_image = Image.open(visitor_image_path)

#         id_card = Image.new('RGB', (856, 539), color = 'white')

#         id_card.paste(visitor_image, (100, 100))

#         draw = ImageDraw.Draw(id_card)

#         font = ImageFont.truetype('arial.ttf', 20)

#         draw.text((100, 20), f"visitor_name: {visitor_name}", fill='black', font=font)
#         draw.text((400, 20), f"TEMPORARY VISITOR PASS", fill='black', font=font)

        

#         Id_card_buffer = BytesIO()

#         id_card.save(Id_card_buffer, format='PNG')

#         return Id_card_buffer