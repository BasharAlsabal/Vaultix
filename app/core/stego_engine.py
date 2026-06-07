import struct
from pathlib import Path
from PIL import Image


MAGIC = b"VAULTIX-STEG1"


class StegoError(Exception):
    pass


def _bytes_to_bits(data: bytes):
    for byte in data:
        for i in range(7, -1, -1):
            yield (byte >> i) & 1


def hide_file_in_png(cover_image_path: str, secret_file_path: str, output_image_path: str) -> str:
    cover = Path(cover_image_path)
    secret = Path(secret_file_path)

    if not cover.exists():
        raise StegoError("Cover image does not exist.")

    if not secret.exists():
        raise StegoError("Secret file does not exist.")

    image = Image.open(cover).convert("RGBA")
    pixels = list(image.getdata())

    secret_name = secret.name.encode("utf-8")
    secret_data = secret.read_bytes()

    payload = (
        MAGIC
        + struct.pack(">H", len(secret_name))
        + secret_name
        + struct.pack(">Q", len(secret_data))
        + secret_data
    )

    total_bits = len(payload) * 8
    capacity_bits = len(pixels) * 3

    if total_bits > capacity_bits:
        raise StegoError("Image is too small for this file. Use a larger PNG image.")

    bit_stream = _bytes_to_bits(payload)
    new_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel

        try:
            r = (r & 0xFE) | next(bit_stream)
            g = (g & 0xFE) | next(bit_stream)
            b = (b & 0xFE) | next(bit_stream)
        except StopIteration:
            new_pixels.append((r, g, b, a))
            new_pixels.extend(pixels[len(new_pixels):])
            break

        new_pixels.append((r, g, b, a))

    image.putdata(new_pixels)
    image.save(output_image_path, "PNG")

    return output_image_path


def extract_file_from_png(stego_image_path: str, output_folder: str) -> str:
    image_path = Path(stego_image_path)

    if not image_path.exists():
        raise StegoError("Stego image does not exist.")

    image = Image.open(image_path).convert("RGBA")
    pixels = list(image.getdata())

    bits = []

    for r, g, b, a in pixels:
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    data = bytearray()

    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        if len(byte_bits) < 8:
            break

        value = 0
        for bit in byte_bits:
            value = (value << 1) | bit

        data.append(value)

    raw = bytes(data)

    if not raw.startswith(MAGIC):
        raise StegoError("No Vaultix hidden data found in this image.")

    offset = len(MAGIC)

    name_length = struct.unpack(">H", raw[offset:offset + 2])[0]
    offset += 2

    file_name = raw[offset:offset + name_length].decode("utf-8")
    offset += name_length

    file_size = struct.unpack(">Q", raw[offset:offset + 8])[0]
    offset += 8

    file_data = raw[offset:offset + file_size]

    output_path = Path(output_folder) / file_name
    output_path.write_bytes(file_data)

    return str(output_path)