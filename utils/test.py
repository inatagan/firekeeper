import re

title = 'PS3 help'

ps = re.search('ps(x|5|4|3)?', title)
print(ps.groups())
