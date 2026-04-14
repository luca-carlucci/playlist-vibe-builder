# Playlist Vibe Builder - Merge Sort Visualizer

**CISC 121 - Introduction to Computing Science, Final Project**
**By:** Luca Carlucci | 20530705

**Chosen Problem:** 

The problem I have chosen is Problem (2) Playlist Vibe Builder. Given a playlist of songs, each with a title, artist and energy score (0-100), and duration (secs), the user picks a sorting key (energy or duration) and the app will sort the playlist using Merge Sort. The sorting process is animated step-by-step, that way the user can follow along.

**Algorithm and why it fits chosen problem and dataset:** 

I chose **Merge Sort** for this problem for a couple of reasons. Fist off, it is a stable sort method. Merge Sort will keep the relative order of songs that have the same energy/duration. This is nice for playlists, since if two songs are tied they will stay in the original order that the user decided. In addition, Merge Sort has predictable performance, considering it always runs in O(n log n) time, regardless of the input. This will make things less complicated as the code won't have to account for the worst case complexity O(n^2). This complexity happens with sorted, or nearly sorted data, which can be common for playlists if users add songs roughly in order.

**Preconditions:** 

None, Merge Sort does not require the data to be pre-sorted, the app accepts any order.

**What user will see during simulation:**

1) **Split steps (blue):** The list being divided into two different halves.

2) **Compare steps (amber):** Two songs being compared, with the winner being added to the merged result.

3) **Remaining steps (purple):** Leftover songs appended after one half is completed.

4) **Merge-completed steps (green):** A sub-merge is complete, showing the merged result.

5) **Bar charts:** A before and after bar chart to visually see the reordering.


## Demo video/gif/screenshot of test

## Problem Breakdown & Computational Thinking

**Decomposition:**

The task breaks down into these smaller tasks:

- Read user's song list from a text box. Validate format, energy range, duration.

- Divide the song list into two halves (recursive base case: list of size <= 1).

- Compare front elements of two sorted halves, pick the smaller, repeat.

- At each split, compare, and merge, save a snapshot for visualization.

- Display results, rendering the step by step trace and before/after bar charts.

**Pattern Recognition:**

The core repeating pattern in Merge Sort is as follows:

- **Split** the list in **half**
- Recursively **sort** each half, with same pattern applied to smaller lists
- **Merge** by repeatedly comparing the front of each half and taking the smaller element.

This split, sort, merge cycle repeats at every level of recursion until we reach single-element lists (base case), then merges build back up to the full sorted list.

**Abstraction:**

Certain things will be shown to the users, and others hidden. The things **shown** to the user will include:

**1)** Each split, comparison and merge labelled card with a plain-English description. **2)** Which song "won" each comparison and why (its value was smaller). **3)** The final merged result at each level. **4)** Before/after bar charts for visual summary.

Others will **not** be shown:

**1)** Recursion depth / call stack details. **2)** Array index management (i,j pointers). **3)** Internal list copying.

## Algorithm Design - Input -> Processing -> Output + Flowchart

**Input:** 

-Text Box: Songs

-Radio: Sort Key

**Processing:**

-Check Format
-Check Ranges
-Build Song List 

Merge Sort:
-Split
-Recurse
-Merge
-Record Steps

**Output:**
-Step-by-step HTML
-Bar chart HTML
-Sorted playlist

**Flowchart (See HTML, there's an error with Preview):**


START
  ↓
Read Song Text + Key
  ↓
Valid Input?
  ├── No → Display Error Message → END
  └── Yes
         ↓
   Break Down Into Dicts
         ↓
   merge_sort():
      if len <= 1 → return
      else:
         - Split in half
         - Sort left
         - Sort right
         - Merge halves
         ↓
   Build HTML step cards + bar charts
         ↓
        END

		
**Data types:**

- Input: Each song is a Python "dict" with keys "title" (str), "artist" (str), "energy" (int, 0-100), "duration" (int, seconds > 0). The full playlist is a "list" of these dicts. 
- Steps list: A "list" of "dict" objects, each describing one algorithm action (split, compare, remaining, or merge_done).

## Steps to Run

1. Clone to the Repository:

2. Install Dependencies:

pip install -r requirements.txt

3. Run the App:

python app.py

git clone 

4. Open URL shown in terminal

## Testing

Test 1 - Default playlist (8 songs, sort by Energy) ***Screenshot** submitted with OnQ submission due to error uploading on Markdown File

- **Input**: The 8 pre-loaded songs
- **Expected**: Songs ordered from lowest to highest energy (Someone Like You --> Uptown Funk).
- **Result**: Correct Ordering ! 

Test 2 - Sort by Duration *Screenshot submitted on OnQ for same reason

- **Input**: Same 8 songs, sort key = Duration
- **Expected**: Shortest song first (Blinding Lights, 3:21) to longest (Stairway to Heaven, 8:02).
- **Result**: Correct Ordering ! 

Test 3 - One song (edge case) *Screenshot submitted on OnQ for same reason

- **Input**: "Only Song, Solo Artist, 50, 200"
- **Expected**: No sorting needed, list gets returned as-is with no compare steps.
- **Result**: Correct ! Output shows "0 comparisons" and the single song. 

Test 4 - Already sorted input

- **Input**: Songs entered in ascending energy order.
- **Expected**: Merge Sort still runs the same number of splits (it always divides), but comparisons may be slightly fewer since one half is always done first during merges.
- **Result**: Correct, output is in the same order as input ! 

Test 5 - Empty input

- **Input**: (blank text box)
- **Expected**: Error: "Please enter at least one song."
- **Result**: Correct ! 

## Hugging Face Link

## Author & AI Acknowledgment

Resources: 
- Gradio documentation:
- Merge Sort Explanation: CISC 121 course notes
- Hugging Face Spaces guide: https://huggingface.co/docs/hub/spaces

