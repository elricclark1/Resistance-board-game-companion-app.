import os, socket, qrcode, random, base64, io
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'resistance'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

class ResistanceGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.phase = "LOBBY"
        self.players = {} # name_lower -> {role, sid, display_name, is_ready}
        self.player_order = [] # list of name_lower
        self.leader_idx = 0
        self.mission_idx = 0
        self.vote_track = 0
        self.mission_results = []
        self.current_team = []
        self.votes = {}
        self.mission_votes = []
        self.winner = None
        self.history = []

    def get_rules(self):
        count = len(self.players)
        return {
            5: {"spies": 2, "missions": [2, 3, 2, 3, 3]},
            6: {"spies": 2, "missions": [2, 3, 4, 3, 4]},
            7: {"spies": 3, "missions": [2, 3, 3, 4, 4]},
            8: {"spies": 3, "missions": [3, 4, 4, 5, 5]},
            9: {"spies": 3, "missions": [3, 4, 4, 5, 5]},
            10: {"spies": 4, "missions": [3, 4, 4, 5, 5]},
        }.get(count, {"spies": 2, "missions": [2, 2, 2, 2, 2]})

game = ResistanceGame()

def get_qr_base64(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception: ip = '127.0.0.1'
    finally: s.close()
    return ip

def broadcast_state():
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000"
    qr_code = get_qr_base64(url) if game.phase == "LOBBY" else None
    rules = game.get_rules()

    for name_lower, data in game.players.items():
        # Scrub roles from player list
        sanitized_players = []
        for nl in game.player_order:
            p = game.players[nl]
            sanitized_players.append({
                "name": p['display_name'],
                "is_leader": (game.player_order.index(nl) == game.leader_idx),
                "is_ready": p.get('is_ready', False) if game.phase == "LOBBY" else False
            })

        state = {
            "phase": game.phase,
            "players": sanitized_players,
            "me": {"name": data['display_name'], "role": data['role'], "is_ready": data.get('is_ready', False)},
            "leader": game.players[game.player_order[game.leader_idx]]['display_name'] if game.player_order else "",
            "mission_idx": game.mission_idx,
            "vote_track": game.vote_track,
            "mission_results": game.mission_results,
            "mission_sizes": rules['missions'],
            "current_team": game.current_team,
            "votes": game.votes if (len(game.votes) == len(game.players) or game.phase != "VOTING") else {},
            "num_needed": rules['missions'][game.mission_idx] if game.mission_idx < 5 else 0,
            "winner": game.winner,
            "spies": [game.players[nl]['display_name'] for nl in game.player_order if game.players[nl]['role'] == "Spy"] if data['role'] == "Spy" else [],
            "qr_code": qr_code,
            "join_url": url,
            "history": game.history,
            "total_players": len(game.players)
        }
        socketio.emit('state', state, to=data['sid'])

def broadcast_lobby():
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000"
    socketio.emit('lobby_info', {
        'players': [game.players[nl]['display_name'] for nl in game.player_order],
        'phase': game.phase,
        'join_url': url,
        'qr_code': get_qr_base64(url) if game.phase == "LOBBY" else None
    })

@app.route('/')
def index(): return render_template('index.html')

@socketio.on('connect')
def on_connect():
    broadcast_lobby()

@socketio.on('join')
def on_join(data):
    name = data.get('name', '').strip()
    if not name: return
    nl = name.lower()
    
    if nl in game.players:
        game.players[nl]['sid'] = request.sid
    elif game.phase == "LOBBY" and len(game.players) < 10:
        game.players[nl] = {"role": None, "sid": request.sid, "display_name": name, "is_ready": False}
        game.player_order.append(nl)
    else:
        emit('error', 'Game in progress or full')
        return
    
    join_room('game_room')
    broadcast_state()
    broadcast_lobby()

@socketio.on('toggle_ready')
def on_toggle_ready():
    player_nl = next((nl for nl, d in game.players.items() if d['sid'] == request.sid), None)
    if not player_nl or game.phase != "LOBBY": return
    
    game.players[player_nl]['is_ready'] = not game.players[player_nl].get('is_ready', False)
    
    num_players = len(game.players)
    if num_players >= 5:
        ready_count = sum(1 for p in game.players.values() if p.get('is_ready', False))
        if ready_count / num_players >= 0.9:
            rules = game.get_rules()
            roles = (["Spy"] * rules['spies']) + (["Resistance"] * (num_players - rules['spies']))
            random.shuffle(roles)
            for i, nl in enumerate(game.player_order):
                game.players[nl]['role'] = roles[i]
                game.players[nl]['is_ready'] = False
            game.leader_idx = random.randrange(num_players)
            game.phase = "TEAM_BUILDING"
    broadcast_state()

@socketio.on('propose')
def on_propose(data):
    game.current_team = data.get('team', [])
    game.phase = "VOTING"
    game.votes = {}
    broadcast_state()

@socketio.on('vote')
def on_vote(data):
    player_nl = next((nl for nl, d in game.players.items() if d['sid'] == request.sid), None)
    if not player_nl or game.players[player_nl]['display_name'] in game.votes: return
    game.votes[game.players[player_nl]['display_name']] = data['vote']
    if len(game.votes) == len(game.players):
        if sum(1 for v in game.votes.values() if v) > len(game.players) / 2:
            game.phase = "MISSION"; game.mission_votes = []; game.vote_track = 0
        else:
            game.vote_track += 1
            if game.vote_track >= 5: game.phase = "GAME_OVER"; game.winner = "Spies"
            else: game.leader_idx = (game.leader_idx + 1) % len(game.players); game.phase = "TEAM_BUILDING"
        broadcast_state()

@socketio.on('mission_vote')
def on_mission_vote(data):
    player_nl = next((nl for nl, d in game.players.items() if d['sid'] == request.sid), None)
    if not player_nl or game.players[player_nl]['display_name'] not in game.current_team: return
    if any(v['name'] == game.players[player_nl]['display_name'] for v in game.mission_votes): return
    vote = True if game.players[player_nl]['role'] == "Resistance" else data['vote']
    game.mission_votes.append({"name": game.players[player_nl]['display_name'], "vote": vote})
    if len(game.mission_votes) == len(game.current_team):
        fails = sum(1 for v in game.mission_votes if not v['vote'])
        req = 2 if (game.mission_idx == 3 and len(game.players) >= 7) else 1
        success = fails < req
        game.mission_results.append(success)
        shuffled = [v['vote'] for v in game.mission_votes]
        random.shuffle(shuffled)
        leader_name = game.players[game.player_order[game.leader_idx]]['display_name']
        game.history.append({
            'mission': game.mission_idx + 1,
            'team': game.current_team[:],
            'votes': shuffled,
            'success': success,
            'leader': leader_name
        })
        if sum(1 for r in game.mission_results if r) >= 3: game.phase = "GAME_OVER"; game.winner = "Resistance"
        elif sum(1 for r in game.mission_results if not r) >= 3: game.phase = "GAME_OVER"; game.winner = "Spies"
        else: game.mission_idx += 1; game.leader_idx = (game.leader_idx + 1) % len(game.players); game.phase = "TEAM_BUILDING"
        broadcast_state()

@socketio.on('reset_game')
def on_reset():
    game.reset()
    socketio.emit('reload_all')

if __name__ == '__main__':
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000"
    print(f"\n--- SERVER RUNNING: {url} ---")
    qr = qrcode.QRCode(); qr.add_data(url); qr.make(); qr.print_ascii()
    socketio.run(app, host='0.0.0.0', port=5000)
