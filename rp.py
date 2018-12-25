import mpyq, math
import matplotlib.pyplot as plt
from s2protocol import versions


archive = mpyq.MPQArchive('test.SC2Replay')

contents = archive.header['user_data_header']['content']

header = versions.latest().decode_replay_header(contents)
baseBuild = header['m_version']['m_baseBuild']
protocol = versions.build(baseBuild)

details = archive.read_file('replay.details')
details = protocol.decode_replay_details(details)
print details

quit()

details = archive.read_file('replay.details')
details = protocol.decode_replay_details(details)
print details

contents = archive.read_file('replay.game.events')
gameEvents = protocol.decode_replay_game_events(contents)


last = {}
last_frame = {}
times = {}
get_next = {}

for i in range(10):
    last[i] = (0,0)
    last_frame[i] = 0
    times[i] = []
    get_next[i] = True

def distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

FPS = 22.4

count = 0
for event in gameEvents:
    user = event['_userid']['m_userId']
    print event
    if event['_event'] == 'NNet.Game.SCmdEvent':
        count += 1
        if get_next[user]:
            get_next[user] = False
            times[user].append(int(((event['_gameloop'] - last_frame[user]) / FPS) * 1000))
        
    elif event['_event'] == 'NNet.Game.SCameraUpdateEvent':
        count += 1
        if not (event['m_target'] == None):
            target = (event['m_target']['x'], event['m_target']['y'])
            if distance(last[user], target) > 5000:
                get_next[user] = True
                last[user] = target
                last_frame[user] = event['_gameloop']

check_id = -1
while check_id == -1:
    print "Enter a players name"
    name = raw_input(">>> ")
    for player in details['m_playerList']:
        if name.lower() in player['m_name'].lower():
            check_id = player['m_teamId']

print check_id

print(sum(times[check_id]) / len(times[check_id]))
