"""
Playlist Vibe Builder — CISC 121 Project (W26)
================================================
A Gradio app that sorts a playlist of songs using the Merge Sort algorithm.
Users can choose to sort by energy score or duration and watch
the algorithm work step-by-step through an animated HTML visualization.

Author: [Your Name]
Course: CISC 121 — Introduction to Computing Science
"""

import gradio as gr
import random
import time
import json

# ============================================================
# SAMPLE DATA — a small default playlist the user can modify
# ============================================================

DEFAULT_SONGS = [
    {"title": "Blinding Lights", "artist": "The Weeknd", "energy": 75, "duration": 201},
    {"title": "Bohemian Rhapsody", "artist": "Queen", "energy": 60, "duration": 354},
    {"title": "Lose Yourself", "artist": "Eminem", "energy": 90, "duration": 326},
    {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "energy": 45, "duration": 482},
    {"title": "Uptown Funk", "artist": "Bruno Mars", "energy": 95, "duration": 270},
    {"title": "Someone Like You", "artist": "Adele", "energy": 30, "duration": 285},
    {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "energy": 88, "duration": 301},
    {"title": "Shape of You", "artist": "Ed Sheeran", "energy": 65, "duration": 234},
]


# ============================================================
# MERGE SORT — implemented from scratch (no built-in sorting)
# ============================================================

def merge_sort(songs, key, steps):
    """
    Recursively splits the list in half, sorts each half,
    then merges them back together in order.

    Parameters
    ----------
    songs : list of dict
        Each dict has keys: title, artist, energy, duration.
    key : str
        The field to sort by ("energy" or "duration").
    steps : list
        Accumulator — each merge operation appends a snapshot
        so we can replay the animation later.

    Returns
    -------
    list of dict
        The sorted list of songs.
    """
    # Base case: a list of 0 or 1 elements is already sorted
    if len(songs) <= 1:
        return songs

    # SPLIT — divide the list into two halves
    mid = len(songs) // 2
    left_half = songs[:mid]
    right_half = songs[mid:]

    # Record the split step for visualization
    steps.append({
        "type": "split",
        "description": f"Split into two halves: left has {len(left_half)} song(s), right has {len(right_half)} song(s)",
        "left": [s["title"] for s in left_half],
        "right": [s["title"] for s in right_half],
    })

    # RECURSE — sort each half
    sorted_left = merge_sort(left_half, key, steps)
    sorted_right = merge_sort(right_half, key, steps)

    # MERGE — combine the two sorted halves into one sorted list
    merged = merge(sorted_left, sorted_right, key, steps)
    return merged


def merge(left, right, key, steps):
    """
    Merge two sorted lists into one sorted list by comparing
    the front elements one at a time.

    Parameters
    ----------
    left : list of dict
        Sorted left half.
    right : list of dict
        Sorted right half.
    key : str
        The field to compare ("energy" or "duration").
    steps : list
        Accumulator for animation snapshots.

    Returns
    -------
    list of dict
        A single merged and sorted list.
    """
    result = []       # the merged output
    i = 0             # pointer for the left list
    j = 0             # pointer for the right list

    # Compare elements from left and right, pick the smaller one
    while i < len(left) and j < len(right):
        left_val = left[i][key]
        right_val = right[j][key]

        if left_val <= right_val:
            # Left element is smaller (or equal) — take it
            result.append(left[i])
            steps.append({
                "type": "compare",
                "description": (
                    f"Compare: \"{left[i]['title']}\" ({key}={left_val}) "
                    f"≤ \"{right[j]['title']}\" ({key}={right_val}) → take left"
                ),
                "chosen": left[i]["title"],
                "compared_with": right[j]["title"],
                "result_so_far": [s["title"] for s in result],
            })
            i += 1
        else:
            # Right element is smaller — take it
            result.append(right[j])
            steps.append({
                "type": "compare",
                "description": (
                    f"Compare: \"{left[i]['title']}\" ({key}={left_val}) "
                    f"> \"{right[j]['title']}\" ({key}={right_val}) → take right"
                ),
                "chosen": right[j]["title"],
                "compared_with": left[i]["title"],
                "result_so_far": [s["title"] for s in result],
            })
            j += 1

    # Append any remaining elements (one of the halves may not be empty)
    while i < len(left):
        result.append(left[i])
        steps.append({
            "type": "remaining",
            "description": f"Append remaining from left: \"{left[i]['title']}\"",
            "chosen": left[i]["title"],
            "result_so_far": [s["title"] for s in result],
        })
        i += 1

    while j < len(right):
        result.append(right[j])
        steps.append({
            "type": "remaining",
            "description": f"Append remaining from right: \"{right[j]['title']}\"",
            "chosen": right[j]["title"],
            "result_so_far": [s["title"] for s in result],
        })
        j += 1

    # Record the completed merge
    steps.append({
        "type": "merge_done",
        "description": f"Merge complete → [{', '.join(s['title'] for s in result)}]",
        "merged": [s["title"] for s in result],
    })

    return result


# ============================================================
# HELPER — parse user-entered songs from a text box
# ============================================================

def parse_songs(text):
    """
    Parse a multi-line string where each line is:
        title, artist, energy, duration
    Returns a list of song dicts or raises ValueError.
    """
    songs = []
    lines = text.strip().split("\n")
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue  # skip blank lines
        parts = line.split(",")
        if len(parts) != 4:
            raise ValueError(
                f"Line {line_num}: expected 4 comma-separated values "
                f"(title, artist, energy, duration), got {len(parts)}."
            )
        title = parts[0].strip()
        artist = parts[1].strip()

        # Validate energy (must be integer 0-100)
        try:
            energy = int(parts[2].strip())
        except ValueError:
            raise ValueError(
                f"Line {line_num}: energy must be a whole number, "
                f"got \"{parts[2].strip()}\"."
            )
        if energy < 0 or energy > 100:
            raise ValueError(
                f"Line {line_num}: energy must be between 0 and 100, "
                f"got {energy}."
            )

        # Validate duration (must be a positive integer, in seconds)
        try:
            duration = int(parts[3].strip())
        except ValueError:
            raise ValueError(
                f"Line {line_num}: duration (seconds) must be a whole number, "
                f"got \"{parts[3].strip()}\"."
            )
        if duration <= 0:
            raise ValueError(
                f"Line {line_num}: duration must be positive, got {duration}."
            )

        songs.append({
            "title": title,
            "artist": artist,
            "energy": energy,
            "duration": duration,
        })

    if len(songs) == 0:
        raise ValueError("Please enter at least one song.")

    return songs


def format_duration(seconds):
    """Convert seconds (int) to a m:ss string."""
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02d}"


# ============================================================
# BUILD HTML — create the step-by-step animation as HTML
# ============================================================

def build_step_html(steps, sorted_songs, key):
    """
    Turn the list of algorithm steps into a single HTML string
    that the user can scroll through. Each step is a card.
    """
    # Colour coding for step types
    colours = {
        "split": "#3b82f6",       # blue
        "compare": "#f59e0b",     # amber
        "remaining": "#8b5cf6",   # purple
        "merge_done": "#10b981",  # green
    }
    icons = {
        "split": "✂️",
        "compare": "⚖️",
        "remaining": "📥",
        "merge_done": "✅",
    }

    html_parts = []
    html_parts.append("""
    <style>
        .step-container { font-family: 'Segoe UI', sans-serif; max-width: 700px; }
        .step-card {
            border-left: 4px solid #ccc;
            padding: 10px 14px;
            margin: 8px 0;
            border-radius: 6px;
            background: #f9fafb;
        }
        .step-num { font-weight: bold; font-size: 0.85em; color: #6b7280; }
        .step-desc { margin-top: 4px; font-size: 0.95em; }
        .final-list {
            margin-top: 16px; padding: 12px;
            background: #ecfdf5; border-radius: 8px;
            border: 2px solid #10b981;
        }
        .final-list h3 { margin: 0 0 8px 0; color: #065f46; }
        .song-row {
            display: flex; justify-content: space-between;
            padding: 6px 0; border-bottom: 1px solid #d1fae5;
            font-size: 0.93em;
        }
        .song-row:last-child { border-bottom: none; }
        .song-rank { font-weight: bold; color: #065f46; width: 28px; }
        .song-title { flex: 1; font-weight: 600; }
        .song-artist { color: #6b7280; flex: 0.7; }
        .song-stat { width: 80px; text-align: right; font-weight: 500; }
        .summary-box {
            background: #eff6ff; border: 2px solid #3b82f6;
            border-radius: 8px; padding: 12px; margin-bottom: 12px;
        }
        .summary-box h3 { margin: 0 0 4px 0; color: #1e40af; }
    </style>
    """)

    # Summary
    total_comparisons = sum(1 for s in steps if s["type"] == "compare")
    total_splits = sum(1 for s in steps if s["type"] == "split")
    total_merges = sum(1 for s in steps if s["type"] == "merge_done")
    html_parts.append(f"""
    <div class="summary-box">
        <h3>📊 Merge Sort Summary</h3>
        <p>Sorted <strong>{len(sorted_songs)}</strong> songs by <strong>{key}</strong>
        in <strong>{len(steps)}</strong> total steps:
        {total_splits} splits, {total_comparisons} comparisons, {total_merges} merges.</p>
    </div>
    """)

    # Steps
    html_parts.append('<div class="step-container">')
    for idx, step in enumerate(steps, start=1):
        colour = colours.get(step["type"], "#9ca3af")
        icon = icons.get(step["type"], "🔹")
        html_parts.append(
            f'<div class="step-card" style="border-left-color:{colour};">'
            f'<span class="step-num">Step {idx} {icon}</span>'
            f'<div class="step-desc">{step["description"]}</div>'
            f'</div>'
        )
    html_parts.append('</div>')

    # Final sorted playlist
    html_parts.append('<div class="final-list">')
    html_parts.append("<h3>🎵 Sorted Playlist</h3>")
    for rank, song in enumerate(sorted_songs, start=1):
        stat = song[key]
        stat_label = f"Energy: {stat}" if key == "energy" else f"Duration: {format_duration(stat)}"
        html_parts.append(
            f'<div class="song-row">'
            f'<span class="song-rank">#{rank}</span>'
            f'<span class="song-title">{song["title"]}</span>'
            f'<span class="song-artist">{song["artist"]}</span>'
            f'<span class="song-stat">{stat_label}</span>'
            f'</div>'
        )
    html_parts.append('</div>')

    return "\n".join(html_parts)


# ============================================================
# BUILD BAR CHART HTML — before & after visual comparison
# ============================================================

def build_bar_chart(songs_before, sorted_songs, key):
    """
    Create a simple HTML/CSS bar chart showing the playlist
    before and after sorting, so the user can visually compare.
    """
    max_val = max(s[key] for s in songs_before) if songs_before else 1

    def bar_row(song, max_v, key_name):
        val = song[key_name]
        pct = int((val / max_v) * 100) if max_v else 0
        label = str(val) if key_name == "energy" else format_duration(val)
        return (
            f'<div style="display:flex;align-items:center;margin:3px 0;">'
            f'<span style="width:160px;font-size:0.85em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{song["title"]}</span>'
            f'<div style="background:#3b82f6;height:20px;width:{pct}%;border-radius:4px;min-width:2px;"></div>'
            f'<span style="margin-left:6px;font-size:0.8em;color:#374151;">{label}</span>'
            f'</div>'
        )

    html = '<div style="font-family:Segoe UI,sans-serif;">'
    html += '<h4 style="margin:8px 0 4px;">Before Sorting</h4>'
    for s in songs_before:
        html += bar_row(s, max_val, key)
    html += '<h4 style="margin:12px 0 4px;">After Sorting (Merge Sort)</h4>'
    for s in sorted_songs:
        html += bar_row(s, max_val, key)
    html += '</div>'
    return html


# ============================================================
# MAIN CALLBACK — runs when the user clicks "Sort Playlist"
# ============================================================

def sort_playlist(song_text, sort_key):
    """
    1. Parse the user's song list.
    2. Run merge sort, collecting step snapshots.
    3. Return the step-by-step HTML and the bar chart HTML.
    """
    # --- input validation ---
    if not song_text or not song_text.strip():
        return (
            '<p style="color:red;">⚠️ Please enter at least one song in the text box above.</p>',
            ""
        )

    try:
        songs = parse_songs(song_text)
    except ValueError as e:
        return (
            f'<p style="color:red;">⚠️ Input error: {e}</p>',
            ""
        )

    # Map user-friendly label to dict key
    key = "energy" if sort_key == "Energy Score" else "duration"

    # Keep a copy of the original order for the bar chart
    songs_before = [s.copy() for s in songs]

    # Run merge sort
    steps = []
    sorted_songs = merge_sort(songs, key, steps)

    # Build outputs
    step_html = build_step_html(steps, sorted_songs, key)
    chart_html = build_bar_chart(songs_before, sorted_songs, key)

    return step_html, chart_html


# ============================================================
# HELPER — generate random songs for the "Randomize" button
# ============================================================

SAMPLE_TITLES = [
    ("Neon Lights", "Synthwave Sam"),
    ("Rainy Monday", "Jazz Cat"),
    ("Thunder Road", "Rock Rita"),
    ("Chill Breeze", "Lo-Fi Lou"),
    ("Fire Dance", "EDM Ella"),
    ("Sunset Walk", "Indie Ian"),
    ("Midnight Run", "Pop Priya"),
    ("Ocean Waves", "Ambient Amy"),
    ("Electric Slide", "Funk Fred"),
    ("Mountain High", "Folk Fiona"),
    ("City Lights", "Hip-Hop Hank"),
    ("Quiet Storm", "R&B Rosa"),
]

def generate_random():
    """Return a string of 6-10 random songs in CSV format."""
    count = random.randint(6, 10)
    chosen = random.sample(SAMPLE_TITLES, min(count, len(SAMPLE_TITLES)))
    lines = []
    for title, artist in chosen:
        energy = random.randint(5, 100)
        duration = random.randint(120, 420)
        lines.append(f"{title}, {artist}, {energy}, {duration}")
    return "\n".join(lines)


def load_defaults():
    """Return the default playlist as a CSV-like string."""
    lines = []
    for s in DEFAULT_SONGS:
        lines.append(f"{s['title']}, {s['artist']}, {s['energy']}, {s['duration']}")
    return "\n".join(lines)


# ============================================================
# GRADIO UI
# ============================================================

with gr.Blocks(
    title="🎵 Playlist Vibe Builder — Merge Sort Visualizer",
) as demo:

    gr.Markdown(
        """
        # 🎵 Playlist Vibe Builder
        ### Sort your playlist using **Merge Sort** and watch every step!

        **How to use:**
        1. Enter songs below (one per line): `title, artist, energy (0-100), duration (seconds)`
        2. Pick a sorting key — **Energy Score** or **Duration**.
        3. Click **Sort Playlist** to see the Merge Sort algorithm in action!
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            song_input = gr.Textbox(
                label="🎶 Song List (title, artist, energy, duration in seconds)",
                placeholder="e.g.  Blinding Lights, The Weeknd, 75, 201",
                lines=10,
                value=load_defaults(),
            )
            with gr.Row():
                sort_key = gr.Radio(
                    choices=["Energy Score", "Duration"],
                    value="Energy Score",
                    label="Sort by",
                )
            with gr.Row():
                sort_btn = gr.Button("🔀 Sort Playlist", variant="primary")
                random_btn = gr.Button("🎲 Randomize Songs")
                default_btn = gr.Button("📋 Load Defaults")

        with gr.Column(scale=2):
            chart_output = gr.HTML(label="Before & After")

    gr.Markdown("---")
    gr.Markdown("### 📝 Step-by-Step Merge Sort Trace")
    step_output = gr.HTML(label="Algorithm Steps")

    # Wire up buttons
    sort_btn.click(
        fn=sort_playlist,
        inputs=[song_input, sort_key],
        outputs=[step_output, chart_output],
    )
    random_btn.click(fn=generate_random, outputs=[song_input])
    default_btn.click(fn=load_defaults, outputs=[song_input])

# Launch the app (works locally and on Hugging Face Spaces)
if __name__ == "__main__":
    demo.launch()
