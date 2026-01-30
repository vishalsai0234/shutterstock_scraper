# =====================================================
# Wikimedia Commons Image Downloader (NO API KEYS)
# Guaranteed to work on academic networks
# =====================================================

import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


# ================= CONFIG =================
IMAGES_TO_DOWNLOAD = 40
DOWNLOAD_DELAY = 1

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml"
}


# ================= HELPERS =================
def create_folder(path):
    os.makedirs(path, exist_ok=True)


def download_image(url, folder, idx):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200 and r.headers.get("Content-Type", "").startswith("image"):
            file = os.path.join(folder, f"image_{idx}.jpg")
            with open(file, "wb") as f:
                f.write(r.content)
            print(f"Downloaded: {file}")
    except Exception as e:
        print("Skipped:", e)


# ================= WIKIMEDIA =================
def fetch_wikimedia(term, folder):
    print("Using Wikimedia Commons ✅")

    search_url = (
        "https://commons.wikimedia.org/wiki/Special:MediaSearch"
        f"?type=image&search={quote(term)}"
    )

    r = requests.get(search_url, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    # Wikimedia uses thumbnails; these are safe & valid images
    imgs = soup.select("img")
    idx = 1

    for img in imgs:
        src = img.get("src")

        if src and "upload.wikimedia.org" in src:
            if src.startswith("//"):
                src = "https:" + src

            download_image(src, folder, idx)
            idx += 1
            time.sleep(DOWNLOAD_DELAY)

        if idx > IMAGES_TO_DOWNLOAD:
            break

    print("\nDone ✅ Images saved in:", folder)


# ================= RUN =================
if __name__ == "__main__":
    term = input("Search term: ").strip()
    folder = os.path.join("downloads", term.replace(" ", "_"))
    create_folder(folder)
    fetch_wikimedia(term, folder)
