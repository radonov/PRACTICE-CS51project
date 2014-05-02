from threading import Thread
from time import time
from connectfour import ConnectFourBoard
import tree_searcher


class inc_depth_thread(Thread):
    #A thread that keeps increasing depth until a
    #certain time elapsed.
    
    def __init__(self, limit_time=5, target=None, group=None, name=None, args=(), kwargs={}):
        """
        Store the various values that we use from the constructor args,
        then let the superclass's constructor do its thing
        """
        self._limit_time = limit_time
        self._target = target
        self._args = args
        self._kwargs = kwargs
        Thread.__init__(self, args=args, kwargs=kwargs, group=group, target=target, name=name)

    def run(self):
        """ Run until the specified time limit has been exceeded """
        depth = 1

        limit_time = self._limit_time**(1/2.0)  # Times grow exponentially, and we don't want to
                                          # start a new depth search when we won't have
                                          # enough time to finish it

        end_time = time() + limit_time
        
        while time() < end_time:
            self._kwargs['depth'] = depth
            self._most_recent_val = self._target(*self._args, **self._kwargs)
            depth += 1

    def get_most_recent_val(self):
        """ Return the most-recent return value of the thread function """
        try:
            return self._most_recent_val
        except AttributeError:
            print "Error: You ran the search function for so short a time that it couldn't even come up with any answer at all!  Returning a random column choice..."
            import random
            return random.randint(0, 6)
    
def run_search_function(board, search_fn, eval_fn, limit_time = 5):
    """
    Run the specified search function "search_fn" to increasing depths
    until "time" has expired; then return the most recent available return value

    "search_fn" must take the following arguments:
    board -- the ConnectFourBoard to search
    depth -- the depth to estimate to
    eval_fn -- the evaluation function to use to rank nodes

    "eval_fn" must take the following arguments:
    board -- the ConnectFourBoard to rank
    """

    eval_t = inc_depth_thread(limit_time=limit_time, target=search_fn, kwargs={ 'board': board,
                                                                          'eval_fn': eval_fn })

    eval_t.setDaemon(True)
    eval_t.start()
    
    eval_t.join(limit_time)

    # Note that the thread may not actually be done eating CPU cycles yet;
    # Python doesn't allow threads to be killed meaningfully...
    return int(eval_t.get_most_recent_val())


class use_memoizer(object):
    """
    'Memoize' decorator.

    Caches a function's return values,
    so that it needn't compute output for the same input twice.

    Use as follows:
    @memoize
    def my_fn(stuff):
        # Do stuff
    """
    def __init__(self, function):
        self.function = function
        self.memocache = {}

    def __call__(self, *args, **kwargs):
        memokey = ( args, tuple( sorted(kwargs.items()) ) )
        if memokey in self.memocache:
            return self.memocache[memokey]
        else:
            val = self.function(*args, **kwargs)
            self.memocache[memokey] = val
            return val







