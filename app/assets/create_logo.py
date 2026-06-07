from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


ASSETS_DIR = Path(__file__).parent
PNG_PATH = ASSETS_DIR / "vaultix_logo.png"
ICO_PATH = ASSETS_DIR / "vaultix.ico"


def create_logo():
    size = 512
    img = Image.new("RGBA", (size, size), (2, 6, 23, 0))
    draw = ImageDraw.Draw(img)

    # Shield shape
    shield = [
        (256, 40),
        (420, 105),
        (390, 330),
        (256, 470),
        (122, 330),
        (92, 105),
    ]

    draw.polygon(shield, fill=(14, 165, 233, 255), outline=(56, 189, 248, 255))

    # Inner shield
    inner = [
        (256, 82),
        (370, 128),
        (348, 310),
        (256, 412),
        (164, 310),
        (142, 128),
    ]

    draw.polygon(inner, fill=(15, 23, 42, 255), outline=(125, 211, 252, 255))

    # Lock body
    draw.rounded_rectangle(
        (178, 220, 334, 340),
        radius=20,
        fill=(56, 189, 248, 255),
    )

    # Lock shackle
    draw.arc(
        (190, 130, 322, 270),
        start=180,
        end=360,
        fill=(56, 189, 248, 255),
        width=26,
    )

    # Letter V
    try:
        font = ImageFont.truetype("arialbd.ttf", 96)
    except Exception:
        font = ImageFont.load_default()

    draw.text(
        (256, 275),
        "V",
        anchor="mm",
        font=font,
        fill=(2, 6, 23, 255),
    )

    img.save(PNG_PATH)

    img.save(
        ICO_PATH,
        sizes=[
            (16, 16),
            (32, 32),
            (48, 48),
            (64, 64),
            (128, 128),
            (256, 256),
        ],
    )

    print(f"Created: {PNG_PATH}")
    print(f"Created: {ICO_PATH}")


if __name__ == "__main__":
    create_logo()