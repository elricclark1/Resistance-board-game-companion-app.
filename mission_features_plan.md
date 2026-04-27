# Implementation Plan: Mission Results and Size Indicators

## Objective
1. Display the count of "Success" and "Fail" votes after each mission.
2. Add mission size indicators (number of players required) to the mission progress circles.

## Implementation Steps

### 1. Track Mission Vote Counts
*   **Backend (`app.py`)**:
    *   Currently, `game.history` stores the shuffled votes. I will ensure this data is sent to the clients.
    *   Update the `mission_results` structure or `history` to make sure the specific counts of success/fail for the *completed* missions are easily accessible to the frontend.
    *   The `game.mission_results` is a list of booleans. I'll supplement this with a `game.mission_counts` list of strings or dicts (e.g., `{"success": 2, "fail": 1}`).

### 2. Update UI for Mission Circles
*   **Frontend (`templates/index.html`)**:
    *   Update the mission progress dots (the circles) to always display the number of players required for that mission.
    *   Add a secondary indicator (e.g., a tooltip or small text below the circle) showing the success/fail breakdown once the mission is complete.

### 3. Detailed Mission History
*   **Frontend (`templates/index.html`)**:
    *   Add a "History" section or update the mission status bar to show the results of previous missions clearly: "Mission 1: Success (2 Success, 0 Fail)".

## Verification
*   Complete a mission and verify the circles show the correct player count for the next mission.
*   Check that the results of the completed mission show the exact number of Fail cards played.
