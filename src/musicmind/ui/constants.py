"""Display constants for the MusicMind AI interface."""

GENRE_DISPLAY = {
    "blues": "Blues",
    "classical": "Classical",
    "country": "Country",
    "disco": "Disco",
    "hiphop": "Hip-Hop",
    "jazz": "Jazz",
    "metal": "Metal",
    "pop": "Pop",
    "reggae": "Reggae",
    "rock": "Rock",
}

GITHUB_URL = "https://github.com/AbdelrhmanAkl/MusicMind-AI"


def display_name(genre: str) -> str:
    """Human-readable genre name for a model class label."""
    return GENRE_DISPLAY.get(genre, genre.replace("_", " ").title())
