# AI GENERATED TESTS - ChatGPT is better than me at writing tests
#NOTE: this code uses the _randomise.py in this folder not the one from the env
# the only diff is: 

# def _get_grouping_key(item):
#     """
#     Helper to get a hashable key for grouping items.
#     """
#     from expyriment.design._structure import ( <--- HERE
#         Block,
#         Trial,
#     )

# instead of 
#     from .._structure import ( 

# To avoid import errors. but the first code also works if put in the expyriment lib


import unittest
from unittest import mock
import sys
import random
from collections import Counter, defaultdict


class MockTrial:
    def __init__(self, factors):
        self.factor_dict = factors
    def __repr__(self):
        return f"Trial({self.factor_dict})"

class MockBlock:
    def __init__(self, factors):
        self.factor_dict = factors
    def __repr__(self):
        return f"Block({self.factor_dict})"

mock_structure = mock.MagicMock()
mock_structure.Trial = MockTrial
mock_structure.Block = MockBlock

# Inject into sys.modules
sys.modules['expyriment.design._structure'] = mock_structure
# Also inject the parent if necessary, though the specific file imports from .._structure
sys.modules['expyriment._structure'] = mock_structure 

# ----------------------------------------------------------------------
# 2. IMPORT MODULE UNDER TEST
# ----------------------------------------------------------------------

try:
    import _randomise as rd
except ImportError:
    print("CRITICAL: Ensure '_randomise.py' is in the same directory as this test file.")
    sys.exit(1)

# ----------------------------------------------------------------------
# 3. TEST CLASSES
# ----------------------------------------------------------------------

class TestGroupingKey(unittest.TestCase):
    """Tests specifically for _get_grouping_key logic."""

    def test_basic_hashables(self):
        """Test ints, strings, tuples."""
        self.assertEqual(rd._get_grouping_key(1), 1)
        self.assertEqual(rd._get_grouping_key("A"), "A")
        self.assertEqual(rd._get_grouping_key((1, 2)), (1, 2))

    def test_expyriment_objects(self):
        """Test MockTrial and MockBlock using factor_dict."""
        t1 = MockTrial({'color': 'red', 'size': 1})
        t2 = MockTrial({'color': 'red', 'size': 1}) # Identical content
        t3 = MockTrial({'color': 'blue'})

        k1 = rd._get_grouping_key(t1)
        k2 = rd._get_grouping_key(t2)
        k3 = rd._get_grouping_key(t3)

        # Keys should be frozensets of items
        self.assertIsInstance(k1, frozenset)
        self.assertEqual(k1, k2, "Identical trials should have identical keys")
        self.assertNotEqual(k1, k3, "Different trials should have different keys")

    def test_lists(self):
        """Test list conversion to tuple."""
        l1 = [1, 2, 3]
        key = rd._get_grouping_key(l1)
        self.assertEqual(key, (1, 2, 3))
        self.assertIsInstance(key, tuple)

    def test_sets(self):
        """Test set conversion to frozenset."""
        s1 = {1, 2, 3}
        key = rd._get_grouping_key(s1)
        self.assertEqual(key, frozenset({1, 2, 3}))
        self.assertIsInstance(key, frozenset)

    def test_simple_dicts(self):
        """Test dicts with hashable values."""
        d1 = {'a': 1, 'b': 2}
        key = rd._get_grouping_key(d1)
        self.assertEqual(key, frozenset({('a', 1), ('b', 2)}))

    def test_complex_dicts_unhashable(self):
        """
        Test dicts with unhashable values (e.g. lists).
        The code uses repr(sorted(item.items())).
        """
        # Dict with a list as value
        d1 = {'a': [1, 2], 'b': 1} 
        
        key = rd._get_grouping_key(d1)
        
        # Expected logic: sorted items, then repr
        # Items: [('a', [1, 2]), ('b', 1)] -> sorted by key
        # verify it returns a string representation
        self.assertIsInstance(key, str)
        self.assertIn("'a', [1, 2]", key) 
        
        # Ensure order invariance of the dict keys in the repr
        d2 = {'b': 1, 'a': [1, 2]}
        key2 = rd._get_grouping_key(d2)
        self.assertEqual(key, key2, "Dict grouping should be independent of key insertion order")


class TestShuffleList(unittest.TestCase):
    """Tests for the main shuffle_list function."""

    def check_constraints(self, lst, max_reps, key_func=lambda x: x):
        """Helper to verify max repetitions are respected."""
        if not lst: return True
        current_streak = 1
        last_val = key_func(lst[0])
        
        for item in lst[1:]:
            val = key_func(item)
            if val == last_val:
                current_streak += 1
            else:
                current_streak = 1
                last_val = val
            
            if current_streak > max_reps:
                return False, f"Streak of {current_streak} for {val} exceeds {max_reps}"
        return True, ""

    def test_basic_integers_success(self):
        """Test shuffling a simple list of integers."""
        lst = [1, 1, 1, 2, 2, 2]
        success = rd.shuffle_list(lst, max_repetitions=2)
        self.assertTrue(success)
        self.assertEqual(len(lst), 6)
        self.assertEqual(sorted(lst), [1, 1, 1, 2, 2, 2])
        
        ok, msg = self.check_constraints(lst, 2)
        self.assertTrue(ok, msg)

    def test_impossible_constraint(self):
        """Test that impossible constraints return False (fallback)."""
        # 10 'A's and 1 'B', max_reps=2. Impossible to solve.
        lst = ["A"] * 10 + ["B"]
        orig_counts = Counter(lst)
        
        success = rd.shuffle_list(lst, max_repetitions=2)
        
        self.assertFalse(success, "Should return False for impossible shuffle")
        self.assertEqual(Counter(lst), orig_counts, "Should conserve elements")
        # It should still be randomly shuffled (fallback)
        # Note: In rare cases, fallback might match original, but unlikely for larger lists.

    def test_complex_types_list_of_lists(self):
        """Test shuffling a list of lists (uses tuple conversion logic)."""
        # Three [1,2] and Three [3,4]
        lst = [[1, 2]] * 3 + [[3, 4]] * 3
        # We need deep copies to ensure they are distinct objects for the test logic if needed,
        # though the function handles same-reference objects fine.
        lst = [[1, 2] for _ in range(3)] + [[3, 4] for _ in range(3)]
        
        success = rd.shuffle_list(lst, max_repetitions=1)
        self.assertTrue(success)
        
        # Check constraint using the tuple logic manually
        ok, msg = self.check_constraints(lst, 1, key_func=lambda x: tuple(x))
        self.assertTrue(ok, msg)

    def test_complex_types_trials(self):
        """Test shuffling MockTrial objects."""
        t1 = MockTrial({'cond': 'A'})
        t2 = MockTrial({'cond': 'B'})
        lst = [t1] * 4 + [t2] * 4
        
        success = rd.shuffle_list(lst, max_repetitions=1)
        self.assertTrue(success)
        
        # Check constraints
        ok, msg = self.check_constraints(lst, 1, key_func=lambda x: frozenset(x.factor_dict.items()))
        self.assertTrue(ok, msg)

    def test_n_segments_logic(self):
        """Test segmentation logic."""
        # Create list 0..19. 
        # n_segments=2. 
        # Logic: 0-9 should be shuffled within 0-9 indices, 10-19 within 10-19.
        lst = list(range(20))
        orig_first_half = set(range(10))
        orig_second_half = set(range(10, 20))
        
        success = rd.shuffle_list(lst, max_repetitions=-1, n_segments=2)
        self.assertTrue(success)
        
        res_first_half = set(lst[:10])
        res_second_half = set(lst[10:])
        
        self.assertEqual(orig_first_half, res_first_half, "Segments should not mix")
        self.assertEqual(orig_second_half, res_second_half, "Segments should not mix")

    def test_segments_with_constraint_failure(self):
        """
        Test n_segments=2 where one segment is impossible and one is possible.
        The function should return False overall, but shuffle the impossible one via fallback.
        """
        # Seg 1: Impossible (AAAAAB, max=2)
        # Seg 2: Possible (CCDD, max=2)
        lst = ["A"]*5 + ["B"] + ["C"]*2 + ["D"]*2
        
        # n_segments=2 -> Seg1 size 6, Seg2 size 4.
        success = rd.shuffle_list(lst, max_repetitions=2, n_segments=2)
        
        self.assertFalse(success, "Should fail because first segment is impossible")
        
        # Verify segment 2 obeyed constraints even though result is False?
        # The current implementation modifies in place.
        # Check second segment (indices 6 to 10)
        seg2 = lst[6:]
        ok, msg = self.check_constraints(seg2, 2)
        self.assertTrue(ok, f"Possible segment should still be shuffled validly: {msg}")

    def test_no_constraints(self):
        """Test max_repetitions = -1."""
        lst = [1]*10 + [2]*10
        success = rd.shuffle_list(lst, max_repetitions=-1)
        self.assertTrue(success)
        self.assertEqual(Counter(lst), Counter([1]*10 + [2]*10))


class TestHelpers(unittest.TestCase):
    """Tests for the smaller helper functions."""

    def test_rand_int_sequence(self):
        res = rd.rand_int_sequence(1, 10)
        self.assertEqual(len(res), 10)
        self.assertEqual(set(res), set(range(1, 11)))
        self.assertNotEqual(res, list(range(1, 11))) # Probabilistic, but likely true

    def test_rand_int(self):
        for _ in range(100):
            r = rd.rand_int(1, 5)
            self.assertTrue(1 <= r <= 5)

    def test_rand_element(self):
        lst = ['a', 'b', 'c']
        for _ in range(20):
            el = rd.rand_element(lst)
            self.assertIn(el, lst)

    def test_coin_flip(self):
        # Statistical test (approximate)
        heads = sum(rd.coin_flip(0.5) for _ in range(1000))
        self.assertTrue(400 < heads < 600, f"Coin flip heavily biased? heads={heads}")
        
        # Biased tests
        self.assertTrue(all(rd.coin_flip(1.0) for _ in range(10)))
        self.assertFalse(any(rd.coin_flip(0.0) for _ in range(10)))
        
        with self.assertRaises(RuntimeError):
            rd.coin_flip(1.5)

    def test_rand_norm(self):
        # Ensure it returns a number and stays within bounds (resampling)
        for _ in range(100):
            # Narrow range to force resampling logic
            r = rd.rand_norm(10, 12, mu=11, sigma=5) 
            self.assertTrue(10 <= r <= 12)

    def test_make_multiplied_shuffled_list(self):
        lst = [1, 2]
        res = rd.make_multiplied_shuffled_list(lst, 3)
        self.assertEqual(len(res), 6)
        self.assertEqual(Counter(res), Counter([1, 1, 1, 2, 2, 2]))


if __name__ == '__main__':
    unittest.main()