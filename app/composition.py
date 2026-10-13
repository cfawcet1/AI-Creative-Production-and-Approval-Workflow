import hashlib
import io
import json
from pathlib import Path

import cairosvg
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    PROJECT_ROOT / "data" / "may_madness_campaign_manifest.json"
)

LOGO_PATH = (
    PROJECT_ROOT / "data" / "assets" / "may_madness_logo.svg"
)

BACKGROUND_PATH = (
    PROJECT_ROOT / "data" / "generated" / "may_madness_background.png"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "generated" / "may_madness_promo.png"
)


def verify_approved_logo(manifest, logo_path):
    """Verify that the logo matches the approved campaign asset."""

    logo = manifest["identity"]["primary_logo"]

    if logo["status"] != "approved":
        raise ValueError("Campaign logo is not approved.")

    if logo["filename"] != logo_path.name:
        raise ValueError("Logo filename does not match campaign manifest.")

    expected_hash = logo["sha256"]

    if not expected_hash:
        raise ValueError("Approved logo has no SHA-256 fingerprint.")

    actual_hash = hashlib.sha256(logo_path.read_bytes()).hexdigest()

    if actual_hash != expected_hash:
        raise ValueError(
            "Logo integrity verification failed. "
            "The file does not match the approved asset."
        )

    print("✓ Approved logo verified")


def crop_to_16x9(image):
    """Center-crop an image to a 16:9 aspect ratio."""

    width, height = image.size
    target_ratio = 16 / 9
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        return image.crop((left, 0, left + new_width, height))

    new_height = int(width / target_ratio)
    top = (height - new_height) // 2

    return image.crop((0, top, width, top + new_height))


def compose_campaign_graphic():
    """Create a branded promotional graphic from approved inputs."""

    manifest = json.loads(MANIFEST_PATH.read_text())

    verify_approved_logo(manifest, LOGO_PATH)

    background = Image.open(BACKGROUND_PATH).convert("RGBA")
    background = crop_to_16x9(background)

    output_width, output_height = background.size

    logo_width = int(output_width * 0.42)

    logo_png = cairosvg.svg2png(
        url=str(LOGO_PATH),
        output_width=logo_width,
    )

    logo = Image.open(io.BytesIO(logo_png)).convert("RGBA")

    x = (output_width - logo.width) // 2
    y = int(output_height * 0.18)

    background.alpha_composite(logo, (x, y))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    background.convert("RGB").save(OUTPUT_PATH, "PNG")

    print("✓ Composition completed")
    print(f"✓ Output saved to: {OUTPUT_PATH}")

    return OUTPUT_PATH


if __name__ == "__main__":
    compose_campaign_graphic()