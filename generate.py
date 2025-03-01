import os
import subprocess
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

def generate_html(input_file, output_file):
    """Generates HTML from Markdown using Pandoc."""
    try:
        subprocess.run(
            ["pandoc", input_file, "-s", "-o", output_file],
            check=True,  # Raise exception on non-zero exit code
            capture_output=True,
            text=True,
        )
        print(f"Successfully generated {output_file} from {input_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating {output_file}: {e.stderr}")

def upload_to_gcs(bucket_name, source_file, destination_name):
    """Uploads a file to Google Cloud Storage."""
    try:
        subprocess.run(
            ["gsutil", "cp", source_file, f"gs://{bucket_name}/{destination_name}"],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Successfully uploaded {source_file} to gs://{bucket_name}/{destination_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error uploading {source_file}: {e.stderr}")

if __name__ == "__main__":
    # Define your bucket name (read from environment variable)
    gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not gcs_bucket_name:
        print("Error: GCS_BUCKET_NAME environment variable not set.")
        exit(1)

    # Generate HTML files for EU, EEA, and Schengen
    generate_html("EU/README.md", "EU.html")
    generate_html("EEA/README.md", "EEA.html")
    generate_html("Schengen/README.md", "Schengen.html")

    # Upload to Google Cloud Storage
    upload_to_gcs(gcs_bucket_name, "EU.html", "EU.html")
    upload_to_gcs(gcs_bucket_name, "EEA.html", "EEA.html")
    upload_to_gcs(gcs_bucket_name, "Schengen.html", "Schengen.html")

    print("Finished generating and uploading files.")