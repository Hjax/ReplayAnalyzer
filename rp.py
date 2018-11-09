import mpyq, math
import matplotlib.pyplot as plt
from s2protocol import versions


archive = mpyq.MPQArchive('test.SC2Replay')

contents = archive.header['user_data_header']['content']

header = versions.latest().decode_replay_header(contents)
baseBuild = header['m_version']['m_baseBuild']
protocol = versions.build(baseBuild)

contents = archive.read_file('replay.game.events')
gameEvents = protocol.decode_replay_game_events(contents)


last = {0:(0,0), 1:(0,0)}
last_frame = {0:0, 1:0}
times = {0:[], 1:[]}
get_next = {0:True, 1:True}

def distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

FPS = 22.4

count = 0
for event in gameEvents:
    user = event['_userid']['m_userId']
    if event['_event'] == 'NNet.Game.SCmdEvent':
        count += 1
        if get_next[user]:
            get_next[user] = False
            times[user].append(int(((event['_gameloop'] - last_frame[user]) / FPS) * 1000))
        
    elif event['_event'] == 'NNet.Game.SCameraUpdateEvent':
        count += 1
        target = (event['m_target']['x'], event['m_target']['y'])
        if distance(last[user], target) > 5000:
            get_next[user] = True
            last[user] = target
            last_frame[user] = event['_gameloop']


