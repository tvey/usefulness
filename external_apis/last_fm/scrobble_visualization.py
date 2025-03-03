import matplotlib.pyplot as plt

from last_fm.utils import read_data


def visualize_data(data: dict) -> None:
    total_scrobbles = sum(data.values())
    top_artist_threshold = 0.3
    top_artist_scrobbles = total_scrobbles * top_artist_threshold
    top_artists_data = {}
    other_count = 0

    for artist, scrobbles in data.items():
        if top_artist_scrobbles > 0:
            top_artists_data[artist] = scrobbles
            top_artist_scrobbles -= scrobbles
        else:
            other_count += scrobbles

    if other_count > 0:
        top_artists_data["Other"] = other_count

    labels = list(top_artists_data.keys())
    sizes = list(top_artists_data.values())

    plt.figure()
    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Pastel1.colors,
    )
    plt.axis("equal")
    plt.title("Scrobbles")
    plt.show()


if __name__ == "__main__":
    artist_scrobbles = read_data()
    visualize_data(artist_scrobbles)
