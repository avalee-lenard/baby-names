import io
import urllib.request
import zipfile
from pathlib import Path

URL = "https://www.ssa.gov/oact/babynames/names.zip"
OUTPUT_CSV = Path("ssa-baby-names.csv")

# Browser-like headers required by www.ssa.gov
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
}


def main() -> None:
    req = urllib.request.Request(URL, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
        zip_bytes = io.BytesIO(response.read())

    # Combine all yobYYYY.txt files into a single CSV with a year column
    with zipfile.ZipFile(zip_bytes) as zf, OUTPUT_CSV.open("w", encoding="utf-8") as out:
        out.write("year,name,sex,count\n")
        for filename in sorted(zf.namelist()):
            if filename.startswith("yob") and filename.endswith(".txt"):
                year = filename[3:7]
                text = zf.read(filename).decode("utf-8")
                for line in text.splitlines():
                    if line.strip():
                        out.write(f"{year},{line}\n")

    print(f"Wrote {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
