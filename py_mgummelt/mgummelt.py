import os
import sys
import calendar
import cProfile, pstats
from itertools import chain

class profiling:
    def __init__(self,
                 stats_file = 'profile.stats',
                 print_file = 'profile.txt'):
        self.stats_file = stats_file
        self.print_file = print_file
    def __enter__(self):
        self.pr = cProfile.Profile()
        self.pr.enable()
    def __exit__(self, exc, exc_type, exc_msg):
        self.pr.disable()
        with open(self.print_file, 'w') as f:
            ps = pstats.Stats(self.pr, stream=f)
            ps.sort_stats('time')
            ps.print_stats()
            ps.dump_stats(self.stats_file)

def pull_field(attr, ls):
    ls = list(ls)
    if not ls:
        return []
    if isinstance(ls[0], dict):
        return [elem[attr] for elem in ls]
    else:
        return [getattr(elem, attr) for elem in ls]

def set_attrs(obj, dict):
    for k, v in dict.iteritems():
        setattr(obj, k, v)

def flatten(ls):
    return chain(*list(ls))

def subclasses(cls):
    subclasses = set()
    q = [cls]
    while q:
        c = q.pop(0)
        subclasses.add(c)
        for subc in c.__subclasses__():
            q.append(subc)
    return subclasses

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def dt_to_ts(dt):
    return calendar.timegm(dt.utctimetuple())
