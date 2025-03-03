import csv
import os

import dotenv

dotenv.load_dotenv()

FILE_PATH = os.getenv("FILE_PATH")


def write_to_file(data: dict[str, int], file_path: str | None = FILE_PATH) -> None:
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["artist", "scrobbles"])

        for artist, scrobbles in data.items():
            writer.writerow([artist, scrobbles])


def read_data(file_path: str | None = FILE_PATH) -> dict[str, int]:
    artist_data = {}

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            artist_data[row["artist"]] = int(row["scrobbles"])

    return artist_data


def show_percentages() -> None:
    artist_scrobbles = read_data()
    total_scrobbles = sum(artist_scrobbles.values())
    artist_share = {
        artist: (count / total_scrobbles) * 100
        for artist, count in artist_scrobbles.items()
    }
    print(f"Total scrobbles: {total_scrobbles}\n")

    for artist, share in artist_share.items():
        print(f"{artist}: {artist_scrobbles.get(artist)} scrobbles ({share:.2f}%)")
