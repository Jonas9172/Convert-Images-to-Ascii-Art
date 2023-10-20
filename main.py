from PIL import Image, ImageDraw, ImageFont


# Define a function to get a character based on the RGB values of a pixel
def getchar(r, g, b, a=256):
    if a == 0:
        return " "
    char_list = list("@B%8&WMZOQLCJUYXwmoahkbdpqzcvunxrjft?I|;:'`")
    gray = 0.2126 * r + 0.7152 * g + 0.0722 * b   # Calculate grayscale value
    index = int(gray / 256 * len(char_list))    # Map grayscale to a character
    return char_list[index]


if __name__ == '__main__':
    image = Image.open("input.png")   # Open the input image
    WIDTH = int(image.width*0.5)
    HEIGHT = int(image.height*0.5)

    # Create a new image for the text representation with a gray background
    imageText = Image.new("RGB", (image.width*4, image.height*4), (231, 223, 223))

    # Resize the original image using the nearest-neighbor algorithm for pixelation
    image = image.resize((WIDTH, HEIGHT), Image.NEAREST)
    text = ""
    colors = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel = image.getpixel((x, y))  # Get the pixel color at (x, y)
            colors.append((pixel[0], pixel[1], pixel[2]))
            if len(pixel) == 4:
                text += getchar(pixel[0], pixel[1], pixel[2], pixel[3])
            else:
                text += getchar(pixel[0], pixel[1], pixel[2])
        text += "\n"
        colors.append((0, 0, 0))
    dr = ImageDraw.Draw(imageText)
    font_size = ImageFont.load_default().font.getsize(text[0])
    font_w, font_h = font_size[0]
    x = y = 0
    font_w *= 1.15  # Adjust font width for spacing
    font_h *= 1  # Adjust font height for spacing
    for i in range(len(text)):
        if text[i] == '\n':   # Move to the next row
            x += font_h
            y = - font_w
        dr.text([y, x], text[i], colors[i])  # Draw each character with its corresponding color
        y += font_w  # Move to the next character's position
    imageText.save("output.png", encoding='utf-8')
