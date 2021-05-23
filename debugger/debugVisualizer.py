from debuggerCmd import GameWithModule, ensure_players, json
from server import app, html, webbrowser

import server
server.html = server.html.replace('battle.json', 'battle_debug.json')


@app.route('/battle_debug.json')
def battledebug():
    g = GameWithModule(*ensure_players(), {})
    g.run()
    return json.dumps(g.get_history())


if __name__ == '__main__':
    webbrowser.open("http://localhost:8080/")
    app.run(port=8080, debug=False)
