"""The expyriment randomise module.

This module contains various functions for randomising data

Modified shuffle_list function (Experimental Approach)
path: .venv/lib/python3.11/site-packages/expyriment/design/randomise/_randomise.py
"""

__author__ = 'Florian Krause <florian@expyriment.org>,\
              Oliver Lindemann <oliver@expyriment.org>'


import random as _random
from copy import copy as _copy
from collections import defaultdict

_random.seed()


def rand_int_sequence(first_elem, last_elem):
    """Return a randomised sequence of integers in given range.

    Parameters
    ----------
    first_elem : int
        first element of the range
    last_elem : int
        last element of the range

    Returns
    -------
    rnd_seq : list
        randomised sequence of integers in given range

    """

    list_ = list(range(first_elem, last_elem + 1))
    _random.shuffle(list_)
    return list_


def rand_int(a, b):
    """Return random integer in given range.

    Parameters
    ----------
    a : int
        first element of range
    b : int
        last element of range

    Returns
    -------
    rnd : int

    """

    return _random.randint(a, b)


def rand_element(list_):
    """Return a random element from a list

    Parameters
    ----------
    list_ : list

    Returns
    -------
    elem : a random element from the list

    """

    list_ = list(list_)
    return list_[_random.randint(0, len(list_) - 1)]


def coin_flip(head_bias=0.5):
    """Return randomly True (head) or False (tail).

    Parameters
    ----------
    head_bias : numeric, optional
        bias in favor of head (default=0.5, fair coin)

    Returns
    -------
    rnd : bool

    """

    if head_bias < 0 or head_bias > 1:
        raise RuntimeError("Head bias must be between 0 and 1!")

    return _random.random() <= head_bias


def rand_norm(a, b, mu=None, sigma=None):
    """Normally distributed random number in given range.

    Parameters
    ----------
    a : numeric
        lowest number in range
    b : numeric
        highest number in range
    mu : numeric, optional
        distribution mean, default: mid point of the interval [a, b]
    sigma : numeric, optional
        distribution standard deviation, default: (b-a)/6.0

    Returns
    -------
    rnd : numeric

    """

    if mu is None:
        mu = a + (b-a) / 2.0
    if sigma is None:
        sigma = (b-a) / 6.0

    r = _random.normalvariate(mu=mu, sigma=sigma)
    if r < a or r > b:
        return rand_norm(a=a, b=b)

    return r


def _get_grouping_key(item):
    """
    Helper to get a hashable key for grouping items.
    """
    from expyriment.design._structure import (
        Block,
        Trial,
    )
    if isinstance(item, (Trial, Block)):
        return frozenset(item.factor_dict.items())
        
    # Handle unhashable types that have hashable "==" equivalents

    if type(item) is dict:
        try:
            return frozenset(item.items())
        except TypeError: # if the dict has unhashable types as values ex. set, dict, list 
            return repr(sorted(item.items())) # items are sorted so that their order in the dict doesn't matter
    
    if type(item) is list:
        return tuple(item)

    if type(item) is set:
        return frozenset(item)

    # For all other types, return the item itself. Relies on them being hashable and having a correct __eq__ method.
    return item

def _shuffle_list_helper(list_seqs, max_repetitions, _retries=975):
    """
    Constructs a list of sequences with at most `max_repetitions` of the same condition consecutively.
    Returns a new list on success, or None on failure.
    """
    
    if not list_seqs:
        return []
        
    # If no repetition constraint, just do a standard shuffle and return
    if max_repetitions < 0:
        shuffled_list = _copy(list_seqs) 
        _random.shuffle(shuffled_list)  
        return shuffled_list

    if _retries <= 0:
        # Could not find a valid shuffle after multiple attempts
        return None

    items_by_cond = defaultdict(list)
    try:
        for item in list_seqs:
            items_by_cond[_get_grouping_key(item)].append(item)
    except TypeError:
        return None 

    # Shuffle each group internally
    for cond in items_by_cond:
        _random.shuffle(items_by_cond[cond])

    res = []
    last_key = None
    streak = 0
    
    while len(res) < len(list_seqs):
        choices = []
        for key in items_by_cond:
            if items_by_cond[key]:
                if key != last_key or streak < max_repetitions:
                    choices.append(key)

        if not choices:
            return _shuffle_list_helper(list_seqs, max_repetitions, _retries - 1)

        choice_key = _random.choice(choices)

        res.append(items_by_cond[choice_key].pop())

        if choice_key == last_key:
            streak += 1
        else:
            streak = 1
        last_key = choice_key

    return res

def shuffle_list(list_, max_repetitions=-1, n_segments=0):
    
    if not isinstance(list_, list):
        raise TypeError("The parameter 'list_' is a {0}, but has to be list. ".format(type(list_).__name__))

    if n_segments is None:
        n_segments = 0
    if max_repetitions is None:
        max_repetitions = -1

    if n_segments > 1:
        success = True
        l = 1 + (len(list_) - 1) // int(n_segments)
        for x in range(n_segments):
            t = (x + 1) * l
            if t > len(list_):
                t = len(list_)

            #slice and try to shuffle without constraint
            segment = list_[l * x:t]

            shuffled_segment = _shuffle_list_helper(
                segment, max_repetitions, _retries=975
            ) 
            
            if shuffled_segment is None:
                success = False #If one segment failed, shuffle it standardly and global success is False
                _random.shuffle(segment)
                list_[l * x:t] = segment
            else:
                list_[l * x:t] = shuffled_segment
        return success
    
    else:
        shuffled_list = _shuffle_list_helper(
            list_, max_repetitions, _retries=975
        )
        
        if shuffled_list is None:
            # standard shuffle as fallback
            _random.shuffle(list_) 
            return False
        else:
            list_[:] = shuffled_list 
            return True


def make_multiplied_shuffled_list(list_, xtimes):
    """Return the multiplied and shuffled (sectionwise) list.

    The function manifolds the list 'x times' and shuffles each
    and concatenates to the return new lists.

    Parameters
    ----------
    list_ : list
        list to be shuffled
    xtimes : int
        how often the list will be multiplied. If xtimes==0, an
        empty list will be returned.

    """

    newlist = []
    tmp = _copy(list(list_))
    for _i in range(0, xtimes):
        _random.shuffle(tmp)
        newlist.extend(tmp)
    return newlist

