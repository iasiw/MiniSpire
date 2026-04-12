import collections

from MiniSpire.src.entities import Targets
from MiniSpire.src.play import Play

repeat_ = collections.defaultdict(int)
message_log = collections.defaultdict(str)
connect_dict = collections.defaultdict()
player = {}
game = collections.defaultdict(lambda: Play(Targets(),Targets()))
room_num = 0
user_num = 0
use_card = False
