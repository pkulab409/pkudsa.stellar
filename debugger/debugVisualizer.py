from debuggerCmd import GameWithModule, ensure_players, json
from server import app, webbrowser

@app.route('/battle.json')
def battledebug():
    g = GameWithModule(*ensure_players(), {})
    g.run()
    return json.dumps(g.get_history())


if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    app.run(port=8080, debug=False)
