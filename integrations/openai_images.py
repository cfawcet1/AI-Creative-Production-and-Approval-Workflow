import base64
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


def generate_campaign_background(brief, output_path):
    """
    Generate a promotional background from a structured creative brief.

    Brand logos and campaign typography are deliberately excluded.
    They will be added later by deterministic composition.
    """

    client = OpenAI()

    prompt = f"""
Create a premium sports-broadcast promotional background.

Campaign: {brief['campaign']}
Creative direction: {brief['creative_direction']}
Visual mood: {brief['visual_mood']}
Primary colors: {', '.join(brief['colors'])}

Requirements:
- Cinematic professional sports-broadcast aesthetic.
- Basketball championship atmosphere.
- Dynamic lighting and strong visual depth.
- Leave clear negative space in the center for a campaign logo.
- No words, letters, numbers, watermarks, or logos.
- No recognizable real-world sports teams or athletes.
- Compose as a wide promotional background.
"""

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024",
        quality="medium",
    )

    image_bytes = base64.b64decode(result.data[0].b64_json)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)

    return output_path


if __name__ == "__main__":
    brief = {
        "campaign": "May Madness",
        "creative_direction": (
            "A dramatic basketball championship arena illuminated "
            "by electric orange and blue lights, with atmospheric "
            "spotlights and a premium national sports broadcast feel."
        ),
        "visual_mood": "Energetic, cinematic, prestigious, competitive",
        "colors": ["#101D35", "#FF5A1F", "#2389FF"],
    }

    output = generate_campaign_background(
        brief,
        PROJECT_ROOT / "data" / "generated" / "may_madness_background.png",
    )

    print(f"\nGenerated campaign background:\n{output}")