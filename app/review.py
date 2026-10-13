import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGE_PATH = PROJECT_ROOT / "data/generated/may_madness_promo.png"
REVIEW_PATH = PROJECT_ROOT / "data/generated/may_madness_review.json"

st.set_page_config(page_title="CreativeOps AI", layout="wide")
st.title("CreativeOps AI")
st.subheader("May Madness | Creative Approval")

if not IMAGE_PATH.exists():
    st.error("No promotional graphic found. Run composition first.")
    st.stop()

image_bytes = IMAGE_PATH.read_bytes()
image_hash = hashlib.sha256(image_bytes).hexdigest()

st.image(image_bytes, caption="Generated campaign graphic", use_container_width=True)
st.caption(f"Artifact SHA-256: {image_hash}")

reviewer = st.text_input("Reviewer name")
comments = st.text_area("Review comments")

col1, col2 = st.columns(2)

def save_review(decision):
    if not reviewer.strip():
        st.error("Enter a reviewer name before submitting.")
        return

    review = {
        "campaign": "May Madness",
        "artifact": IMAGE_PATH.name,
        "artifact_sha256": image_hash,
        "decision": decision,
        "reviewer": reviewer.strip(),
        "comments": comments.strip(),
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }

    REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PATH.write_text(json.dumps(review, indent=2))
    st.success(f"Review saved: {decision}")

with col1:
    if st.button("Approve", type="primary"):
        save_review("approved")

with col2:
    if st.button("Reject"):
        save_review("rejected")