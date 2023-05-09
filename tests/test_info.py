import unittest

from pynecraft.info import Fish, block_items, blocks, blocks_by_id, items, items_by_id, mobs, mobs_by_id, \
    must_give_items, must_give_items_by_id
from pynecraft.simpler import Painting


class TestInfo(unittest.TestCase):
    def test_fish(self):
        var1 = Fish.variant('Spotty', 'Blue', 'RED')
        self.assertEqual(0x0e_0b_00_01, var1)
        fish = Fish(var1, 'foo')
        self.assertTrue(fish.is_small())
        self.assertEqual(0, fish.which_body())
        self.assertEqual('Spotty', fish.kind())
        self.assertEqual('blue', fish.body_color())
        self.assertEqual('red', fish.pattern_color())
        self.assertEqual('Blue-Red Spotty', fish.desc())
        var2 = Fish.variant('Glitter', 'GREEN', 'light blue')
        self.assertEqual(0x03_0d_03_00, var2)
        fish = Fish(var2, 'foo')
        self.assertFalse(fish.is_small())
        self.assertEqual(3, fish.which_body())
        self.assertEqual('Glitter', fish.kind())
        self.assertEqual('green', fish.body_color())
        self.assertEqual('light_blue', fish.pattern_color())
        self.assertEqual('Green-Light Blue Glitter', fish.desc())

    def test_full_lists(self):
        self.assertIn('Oak Sign', blocks)
        self.assertIn('oak_sign', blocks_by_id)
        self.assertNotIn('oak_wall_sign', blocks)

        self.assertIn('Book and Quill', items)
        self.assertIn('writable_book', items_by_id)
        self.assertNotIn('Oak Sign', items)

        self.assertIn('Cocoa', block_items)
        self.assertNotIn('Oak Sign', block_items)
        self.assertEqual('oak_sign', block_items['Oak Sign'].id)

        self.assertIn('Zombie', mobs)
        self.assertIn('zombie', mobs_by_id)

        self.maxDiff = None
        self.assertSequenceEqual(list(blocks.values()), sorted(blocks.values()))
        self.assertSequenceEqual(tuple(items.values()), sorted(items.values()))
        self.assertSequenceEqual(tuple(mobs.values()), sorted(mobs.values()))
        self.assertSequenceEqual(tuple(blocks_by_id.values()), sorted(blocks.values(), key=lambda t: t.id))
        self.assertSequenceEqual(tuple(items_by_id.values()), tuple(sorted(items.values(), key=lambda t: t.id)))
        self.assertSequenceEqual(tuple(mobs_by_id.values()), tuple(sorted(mobs.values(), key=lambda t: t.id)))

        for key, value in must_give_items.items():
            self.assertEqual(items[key], value)
        for key, value in must_give_items_by_id.items():
            self.assertEqual(items_by_id[key], value)

    def test_painting(self):
        self.assertEqual('bust', Painting('bust').nbt['variant'])
