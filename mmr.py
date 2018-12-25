import mpyq, math
import matplotlib.pyplot as plt
from s2protocol import versions


archive = mpyq.MPQArchive('test.SC2Replay')

contents = archive.header['user_data_header']['content']

header = versions.latest().decode_replay_header(contents)
baseBuild = header['m_version']['m_baseBuild']
protocol = versions.build(baseBuild)

details = archive.read_file('replay.load.info')
details = protocol.decode_replay_details(details)

print archive.files
