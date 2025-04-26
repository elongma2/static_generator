import unittest
from blocktype import BlockType, block_to_block_type,is_ordered_list


class TestBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("### This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- This is an unordered list"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is an ordered list" \
        "\n2. This is an ordered list"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is not a valid block"), BlockType.PARAGRAPH)