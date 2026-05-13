# Resistance Companion App

A real-time, local-network web application for the board game "The Resistance". This app allows players to use their smartphones as controllers, automating role distribution, voting, and mission tracking while eliminating the need for physical cards.

## 🚀 Usage & Installation

1. **Navigate to the project directory:**
   ```bash
   cd resistancecompanionapp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python app.py
   ```

4. **Join the game:**
   - The server will display a QR code and a local IP address (e.g., `http://192.168.1.50:5000`) in the terminal.
   - All players must be on the **same Wi-Fi network**.
   - Scan the QR code or enter the URL into your mobile browser to join the lobby.

## 🎮 How to Play

1. **Lobby:** Players join by entering their names. Once at least 5 players are ready, the game starts and roles are secretly assigned.
2. **Role Reveal:** Use the "Press and Hold" button on your screen to see if you are **Resistance** or a **Spy**.
3. **Team Building:** The designated Leader selects a team for the current mission based on the required size shown on the screen.
4. **Voting:** All players vote "Approve" or "Reject" on the proposed team. If the majority rejects (or it's a tie), the Leader title passes to the next player.
5. **Missions:** If a team is approved, members secretly vote "Success" or "Fail".
   - **Resistance** MUST vote Success.
   - **Spies** can choose to sabotage by voting Fail.
6. **Winning:** The Resistance wins by succeeding in 3 missions. The Spies win if 3 missions fail or if 5 teams are rejected in a single round.

## ✨ Features

- **Local Network Play:** Optimized for LAN environments, accessible via QR code.
- **Real-time Sync:** Uses WebSockets for instant updates across all devices.
- **Secure Role Reveal:** "Press and hold" mechanic to prevent screen peeking.
- **Automated Rules:** Handles role distribution and mission sizes for 5-10 players.
- **Mission History:** Tracks results, team composition, and vote counts for every round.
- **Special Rule Support:** Automatically enforces the "2 fails required" rule for Mission 4 in large games.
- **Session Persistence:** Allows players to reconnect with the same name if their browser refreshes.

## 🛠️ Technical Details

- **Backend:** Python (Flask), Flask-SocketIO for real-time state synchronization.
- **Frontend:** Vanilla JavaScript and CSS (Single Page Application).
- **Network:** Binds to `0.0.0.0:5000` to allow LAN access.
- **Features:**
  - Automated rule matrix for 5-10 players.
  - "Press and hold" secure role reveal mechanic.
  - Mission history and vote tracking.
  - Special "2 fails required" logic for Mission 4 in 7+ player games.
- **Design:** Serves as the visual baseline for the workspace with a mobile-first, high-contrast dark theme.
