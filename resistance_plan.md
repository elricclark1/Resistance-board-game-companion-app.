# Implementation Plan: The Resistance Local-Network App

## Objective
Build a real-time, local-network web application for the board game "The Resistance" using Python (Flask/SocketIO) for the backend and Vanilla JS/CSS for the frontend.

## Architecture & Technical Decisions
*   **Backend:** Flask serving the initial HTML, with Flask-SocketIO handling all subsequent game state synchronizations. Eventlet will be used as the async mode for optimal performance.
*   **Frontend:** A Single Page Application (SPA) contained entirely within `templates/index.html`. It will use vanilla JavaScript to handle SocketIO events and toggle DOM visibility based on the game state.
*   **Styling:** I will use clean, custom CSS embedded in the HTML. This ensures the app works perfectly on a local network even if the router does not have an active internet connection (avoiding CDN dependencies).
*   **Reconnection:** The server will track players by their chosen name. If a socket disconnects, the player can enter their name again in the lobby to "re-bind" their new socket ID to their existing player state.

## Implementation Steps

### 1. Server Setup & Utilities (`app.py`)
*   Configure Flask and SocketIO.
*   Implement local IP detection and terminal QR code generation upon startup.
*   Define the Game State data structure (Players, Mission History, Current State, Leader, Vote Track).

### 2. Game Logic Engine (`app.py`)
*   **Rule Matrix:** Hardcode the configuration for 5 to 10 players (number of spies, mission sizes, and the special "2 fails required" rule for mission 4 in 7+ player games).
*   **State Machine Phases:**
    *   `LOBBY`: Accepting players.
    *   `TEAM_BUILDING`: Current leader selects a team.
    *   `VOTING`: All players approve/reject the team. Tied votes reject. 5 rejections in a round = Spies win.
    *   `MISSION`: Approved team votes Success/Fail. Resistance constrained to Success. Result shuffled.
    *   `GAME_OVER`: 3 successful missions (Resistance wins) or 3 failed missions (Spies win).

### 3. Security & Data Sanitization
*   Implement a state-sanitization function that runs before emitting state to a specific client.
*   Ensure Resistance players only receive their own role. Spies receive the list of all spies.
*   Ensure secret votes (during the Mission phase) are not broadcasted until the phase resolves.

### 4. Frontend UI & Socket Integration (`templates/index.html`)
*   **Views:** Create hidden-by-default `div` sections for: Lobby, Role Reveal, Team Selection, Voting, Mission Action, and Game Over.
*   **Role Reveal:** Implement `mousedown`/`touchstart` and `mouseup`/`touchend` listeners to implement the "press and hold to reveal" mechanic safely.
*   **Client Logic:** Listen for `game_state_update` events from the server and render the appropriate view based on the player's role and the current game phase.

## Verification
*   Ensure the QR code generates correctly in the terminal.
*   Verify that players can join, disconnect, and rejoin using the same name.
*   Validate the role distribution and visibility (Spies see spies, Resistance sees nothing).
*   Run through a simulated game to ensure mission progression, the vote track, and win conditions trigger correctly.