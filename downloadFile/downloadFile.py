#!/usr/bin/env python3

import requests
import argparse
import os

# python3 downloadFile "https://en.wikipedia.org/static/images/icons/wikipedia.png"

def get_filename_from_url(url):
    """Extracts the filename from a URL."""
    return url.split("/")[-1] or "downloaded_file"


def download_file(url):
    """
    Downloads a file from the given URL and saves it with the extracted filename.

    Args:
        url (str): The URL of the file to download.
    """
    try:
        print(f"Starting download from: {url}")

        # Send a GET request to fetch the content
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        filename = get_filename_from_url(url)

        # Check if file already exists to prevent overwriting
        if os.path.exists(filename):
            print(f"Warning: {filename} already exists. It will be overwritten.")

        # Save the content to a file
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Download completed: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to download the file. {e}")
    except OSError as e:
        print(f"Error: Unable to save the file. {e}")


def main():
    """
    Main function to handle argument parsing and initiate the file download.
    """
    parser = argparse.ArgumentParser(description="Download a file from a given URL.")
    parser.add_argument("-u", "--url", required=True, help="URL of the file to be downloaded")

    args = parser.parse_args()

    # Start the download process
    download_file(args.url)


if __name__ == "__main__":
    main()

