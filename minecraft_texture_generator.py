import json
import os
from PIL import Image, ImageDraw, ImageFont


def find_es_json(indexes_json):
    with open(indexes_json, "r") as f:
        data = json.load(f)

        es_entry = data["objects"]["minecraft/lang/es_es.json"]
        es_hash = es_entry["hash"]

        subdir = es_hash[:2]

        minecraft_assets = os.path.expanduser("~/.minecraft/assets/objects")
        es_path = os.path.join(minecraft_assets, subdir, es_hash)

        return es_path


def filter_es_json(es_path):
    with open(es_path, "r") as f:
        data = json.load(f)
        filtered_data = {}

        for key in data.keys():
            key_list = key.split(".")
            if key_list[0] in ["block", "item", "container", "entity"]:
                filtered_data[key] = data[key]

        return filtered_data


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def generate_texture(text):
    texture = Image.new("RGBA", (128, 128), color="white")
    draw = ImageDraw.Draw(texture)

    font = ImageFont.truetype("arial.ttf", 22)

    lines = wrap_text(draw, text, font, 120)

    line_height = draw.textbbox((0, 0), "Ay", font=font)[3]
    total_height = line_height * len(lines)

    y = (128 - total_height) / 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        x = (128 - width) / 2

        draw.text((x, y), line, font=font, fill="black")
        y += line_height

    for key, value in filtered_data.items():
        if value == text:
            key_list = key.split(".")

            if key_list[0] == "block":
                texture.save(
                    os.path.expanduser(f"~/.minecraft/resourcepacks/Spanish Resource Pack/assets/minecraft/textures/block/{key_list[-1]}.png"
                )

            if key_list[0] == "item":
                texture.save(
                    os.path.expanduser(f"~/.minecraft/resourcepacks/Spanish Resource Pack/assets/minecraft/textures/item/{key_list[-1]}.png"
                )


indexes_json = input("Type the file path for the indexes json: ")

es_path = find_es_json(indexes_json)
filtered_data = filter_es_json(es_path)

block_dir = os.path.expanduser("~/.minecraft/resourcepacks/Spanish Resource Pack/assets/minecraft/textures/block")
item_dir = os.path.expanduser("~/.minecraft/resourcepacks/Spanish Resource Pack/assets/minecraft/textures/item")

if not os.path.exists(block_dir):
    os.makedirs(block_dir)

if not os.path.exists(item_dir):
    os.makedirs(item_dir)

for text in filtered_data.values():
    generate_texture(text)
