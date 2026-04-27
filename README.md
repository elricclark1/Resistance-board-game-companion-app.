# Resistance Board Game Companion App

A real-time, local-network web application for the board game "The Resistance". This app allows players to play the game using their smartphones as controllers, eliminating the need for the physical board and cards.

## 🚀 Features

- **Local Network Play:** Designed to run on a LAN, allowing anyone on the same Wi-Fi to join via a QR code or local URL.
- **Real-time Synchronization:** Uses WebSockets (Socket.io) for instant state updates across all connected devices.
- **Role Reveal:** Secure "press and hold" mechanic for secret role identification.
- **Game Logic Automation:**
  - Automated role distribution (Spies vs. Resistance).
  - Mission size management based on player count (5-10 players).
  - Automated voting tracking and mission resolution.
  - Support for special rules (e.g., 2 fails required for Mission 4 in 7+ player games).
- **History Tracking:** Detailed mission history showing success/fail counts and team compositions.

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-SocketIO
- **Frontend:** Vanilla JavaScript, CSS (embedded for zero-dependency LAN support)
- **Utilities:** `qrcode` for easy joining.

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/elricclark1/Resistance-board-game-companion-app..git
   cd Resistance-board-game-companion-app.
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
   - The server will display a QR code and a local IP address in the terminal.
   - Players on the same network can scan the QR code or enter the URL into their mobile browser.

## 🎮 How to Play

1. **Lobby:** Players join by entering their names.
2. **Ready Up:** Once at least 5 players are ready, roles are assigned.
3. **Team Building:** The designated Leader selects a team for the current mission.
4. **Voting:** All players vote to approve or reject the proposed team.
5. **Missions:** Approved teams secretly vote "Success" or "Fail".
6. **Winning:** The Resistance wins by succeeding in 3 missions. The Spies win if 3 missions fail or if 5 teams are rejected in a single round.

## 📝 License

This project is for personal use and education. Check the repository for specific licensing details.
