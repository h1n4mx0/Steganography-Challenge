from PIL import Image

def image_to_binary(image_path):
    """Chuyển đổi ảnh thành dữ liệu nhị phân"""
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    binary_data = ""

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_data += f"{r:08b}{g:08b}{b:08b}"  # Mỗi kênh màu thành 8 bit

    return binary_data

def hide_image(target_image, original_image, output_image="stego_image.png"):
    """Nhúng dữ liệu nhị phân của target_image vào original_image"""
    targetBinary = image_to_binary(target_image)
    data_index, binary_length = 0, len(targetBinary)

    img = Image.open(original_image).convert("RGB")
    width, height = img.size
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            if data_index < binary_length:
                r, g, b = pixels[x, y]

                r = (r & 0b11111110) | int(targetBinary[data_index])
                data_index += 1
                if data_index < binary_length:
                    g = (g & 0b11111110) | int(targetBinary[data_index])
                    data_index += 1
                if data_index < binary_length:
                    b = (b & 0b11111110) | int(targetBinary[data_index])
                    data_index += 1
                
                pixels[x, y] = (r, g, b)
    
    img.save(output_image)
    print(f"Ảnh đã nhúng được lưu thành: {output_image}")

def extract_image(stego_image, output_image="extracted_image.png", width=None, height=None):
    """Giải mã ảnh đã ẩn và lưu dưới dạng file ảnh"""
    img = Image.open(stego_image).convert("RGB")
    img_width, img_height = img.size
    extracted_binary = ""

    for y in range(img_height):
        for x in range(img_width):
            r, g, b = img.getpixel((x, y))
            extracted_binary += f"{r & 1}{g & 1}{b & 1}"

    if width is None or height is None:
        total_pixels = len(extracted_binary) // 24  # 24 bit cho mỗi pixel (8 bit mỗi kênh)
        width = int(total_pixels ** 0.5)  # Giả sử ảnh hình vuông
        height = total_pixels // width

    extracted_img = Image.new("RGB", (width, height))
    pixels = extracted_img.load()
    
    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index + 24 <= len(extracted_binary):
                r = int(extracted_binary[data_index:data_index+8], 2)
                g = int(extracted_binary[data_index+8:data_index+16], 2)
                b = int(extracted_binary[data_index+16:data_index+24], 2)
                pixels[x, y] = (r, g, b)
                data_index += 24  # Mỗi pixel có 24 bit

    extracted_img.save(output_image)
    print(f"Ảnh đã giải mã được lưu thành: {output_image}")

hide_image("flag.png", "input.png", "stego_output.png")
extract_image("stego_output.png","extracted_image.png",400,400)
