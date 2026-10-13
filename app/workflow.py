from composition import compose_campaign_graphic


def run_workflow():
    print("Starting CreativeOps AI workflow...")

    # Step 1: Validate the approved logo and compose the graphic.
    # compose_campaign_graphic() stops execution if validation fails.
    output_path = compose_campaign_graphic()

    # Step 2: Hand the artifact off for human review.
    print(f"✓ Artifact ready for human review: {output_path}")
    print("Next: Run 'streamlit run app/review.py' to approve or reject.")


if __name__ == "__main__":
    run_workflow()