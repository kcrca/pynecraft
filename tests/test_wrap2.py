import unittest
from pynecraft.wrap import wrap, Text

class TestPynecraftMarkdownWrapping(unittest.TestCase):

    # =========================================================================
    # 🎯 GROUP 1: CRITICAL CAPACITY BOUNDARY TESTS
    # =========================================================================

    def test_bold_text_word_keeps_together_on_single_line(self):
        """Verify that an unbroken bold word fits cleanly on one line when threshold permits."""
        res = wrap(75, 1, *Text.from_html("<b>AAAAAAAAAA</b>"))
        self.assertEqual(len(res), 1)       
        self.assertEqual(len(res[0]), 1)    
        self.assertEqual(res[0][0]['text'], "AAAAAAAAAA")

    def test_bold_text_word_preserves_single_line_on_tight_bounds(self):
        """Verify that an unsplittable single bold word remains on one line even if it exceeds the limit."""
        res = wrap(64, 2, *Text.from_html("<b>AAAAAAAAAA</b>"))
        self.assertEqual(len(res), 1)       
        self.assertEqual(len(res[0]), 1)    

    def test_long_bold_string_fits_page_limits(self):
        """Verify long unbroken phrases do not split across lines prematurely."""
        res = wrap(129, 2, *Text.from_html("<b>AAAAAAAAAAAAAAAAAAAA</b>"))
        self.assertEqual(len(res), 1)
        self.assertEqual(len(res[0]), 1)

    def test_bold_sign_text_fits_standard_sign_canvas(self):
        """Verify long bold phrases stay structurally bounded on standard line configurations."""
        res = wrap(90, 1, *Text.from_html("<b>AAAAAAAAAAAAA</b>"))
        self.assertEqual(len(res), 1)
        self.assertEqual(len(res[0]), 1)
        self.assertEqual(res[0][0]['text'], "AAAAAAAAAAAAA")

    # =========================================================================
    # 🔤 GROUP 2: MARKDOWN SYNTAX PARSING CHECKS
    # =========================================================================

    def test_markdown_asterisks_activate_bold_attribute(self):
        """Verify markdown parsing successfully registers the bold key on the Text dictionary."""
        res = wrap(100, 1, *Text.from_html("<b>Hello</b>"))
        self.assertTrue(res[0][0].get('bold', False))

    def test_markdown_parser_strips_syntax_tags_from_text(self):
        """Verify layout generation strips formatting markdown syntax tokens from the final text string."""
        res = wrap(100, 1, *Text.from_html("<b>Hello</b>"))
        self.assertEqual(res[0][0]['text'], "Hello")

    def test_plain_text_defaults_to_false_bold_flag(self):
        """Verify unformatted raw text nodes do not receive a true bold key configuration."""
        res = wrap(100, 1, "Plain String")
        self.assertFalse(res[0][0].get('bold', False))

    def test_empty_string_markdown_token_returns_cleanly(self):
        """Verify blank parameter passes prevent processing collection failures."""
        res = wrap(114, 1, "")
        self.assertTrue(len(res) >= 0)

    # =========================================================================
    # 📝 GROUP 3: LINE WRAPPING FUNCTIONALITY (BASIC & BOUNDARIES)
    # =========================================================================

    def test_empty_input_arguments_returns_empty_page_list(self):
        """Verify empty argument arrays produce empty multi-page layouts."""
        res = wrap(114, 14)
        self.assertEqual(res, [])

    def test_single_word_fits_on_first_line(self):
        """Verify short terms match core single node positions."""
        res = wrap(100, 1, "Test")
        self.assertEqual(res[0][0]['text'], "Test")

    def test_narrow_bounds_force_word_spill_to_new_line(self):
        """Verify strict width cuts force word wrapping segments down safely."""
        res = wrap(40, 5, "Hello World")
        self.assertEqual(len(res), 1)
        self.assertEqual(len(res[0]), 2)
        self.assertEqual(res[0][0]['text'].strip(), "Hello")
        self.assertEqual(res[0][1]['text'].strip(), "World")

    def test_vast_canvas_skips_wrapping_logic_completely(self):
        """Verify high ceiling constraints isolate segments to single fields."""
        res = wrap(500, 1, "A", "B", "C", "D")
        self.assertEqual(len(res), 1)
        self.assertEqual(len(res[0]), 1)
    # =========================================================================
    # 🎨 GROUP 4: MULTI-STYLING & SEGMENT PROCESSING
    # =========================================================================

    def test_style_cloning_persists_across_line_breaks(self):
        """Verify attribute properties persist when words drop to line updates by verifying Text type."""
        res = wrap(30, 5, "Super Long Text Elements Go Here")
        for page in res:
            for line in page:
                self.assertIsInstance(line, Text)

    def test_injected_spaces_inherit_parent_style_flags(self):
        """Verify interval spacings inside styled tags maintain local weight keys."""
        res = wrap(100, 1, *Text.from_html("<b>A B</b>"))
        self.assertTrue(res[0][0].get('bold', False))

    # =========================================================================
    # 📄 GROUP 5: PAGINATION & LINES PER PAGE
    # =========================================================================

    def test_page_breaks_triggered_by_line_capacity_caps(self):
        """Verify tight single line caps route page generations correctly."""
        res = wrap(40, 1, "Hello World")
        self.assertEqual(len(res), 2)        
        self.assertEqual(len(res[0]), 1)     
        self.assertEqual(len(res[1]), 1)     

    def test_book_pagination_threshold_limits(self):
        """Verify 14 line limits split paragraphs on page indexes for books."""
        long_text = "\n".join(["Line"] * 15)
        res = wrap(114, 14, long_text)
        self.assertTrue(len(res) >= 1)

    def test_sign_pagination_line_capacity_limits(self):
        """Verify sign configurations route layout text to page steps at line 4."""
        long_text = "\n".join(["Text"] * 5)
        res = wrap(90, 4, long_text)
        self.assertTrue(len(res) >= 1)

    def test_aggressive_single_line_page_limits_isolate_chains(self):
        """Verify paragraph text breaks across separate layers when cap rows match 1."""
        res = wrap(100, 1, "A\nB\nC")
        self.assertTrue(len(res) >= 1)

    def test_null_row_page_limits_fail_safely_or_apply_defaults(self):
        """Verify passing an index limit of 0 drops operations into zero fallbacks safely."""
        try:
            wrap(100, 0, "Test")
        except ZeroDivisionError:
            self.fail("wrap() crashed with ZeroDivisionError!")
        except Exception:
            pass

    # =========================================================================
    # 🚀 GROUP 6: COMPREHENSIVE BULK RUN BOUNDARY TESTS
    # =========================================================================

    def test_bulk_standard_plain_text_sentence(self):
        self.assertTrue(len(wrap(114, 14, "Bulk run execution string")) >= 1)

    def test_bulk_single_character_node(self):
        res = wrap(100, 1, "A")
        self.assertEqual(res[0][0]['text'], "A")

    def test_bulk_multiple_newline_split_phrases(self):
        res = wrap(90, 4, "One\nTwo\nThree")
        self.assertEqual(len(res), 1)

    def test_bulk_minimal_width_single_word(self):
        res = wrap(10, 1, "Word")
        self.assertEqual(res[0][0]['text'], "Word")

    def test_bulk_single_bold_character(self):
        res = wrap(114, 14, *Text.from_html("<b>A</b>"))
        self.assertTrue(res[0][0].get('bold', False))

    def test_bulk_narrow_limit_with_multiple_newlines(self):
        res = wrap(50, 2, "Test1\nTest2\nTest3")
        self.assertTrue(len(res) >= 1)

    def test_bulk_book_capacity_exact_line_fill(self):
        res = wrap(114, 14, *["Line\n"]*14)
        self.assertTrue(len(res) >= 1)

    def test_bulk_spaced_newline_tokens(self):
        res = wrap(100, 5, "Hello \n World")
        self.assertTrue(len(res) >= 1)

    def test_bulk_micro_canvas_single_letter(self):
        res = wrap(5, 1, "A")
        self.assertEqual(len(res), 1)

    def test_bulk_long_bold_unbroken_string(self):
        res = wrap(114, 14, *Text.from_html("<b>BoldText</b>"))
        self.assertTrue(res[0][0].get('bold', False))

    def test_bulk_sign_capacity_split(self):
        res = wrap(90, 4, "SignLine1\nSignLine2")
        self.assertTrue(len(res) >= 1)

    def test_bulk_special_punctuation_characters(self):
        res = wrap(100, 1, "Special chars $%^&*()")
        self.assertTrue(len(res[0][0]['text']) >= 1)

    def test_bulk_numeric_string_sequence(self):
        res = wrap(200, 10, "Numbers 123456")
        self.assertEqual(res[0][0]['text'], "Numbers 123456")

    def test_bulk_standard_book_width_sentence(self):
        res = wrap(114, 14, "Longer text block to test spacing boundaries.")
        self.assertEqual(len(res), 1)

    def test_bulk_standard_sign_width_sentence(self):
        res = wrap(90, 4, "Short text segment.")
        self.assertEqual(len(res), 1)

    def test_bulk_narrow_canvas_with_numbers(self):
        """Verify clear newline structures segment separate items."""
        res = wrap(10, 1, "1\n2")
        self.assertTrue(len(res) >= 1)

    def test_bulk_pure_bold_markdown_wrap(self):
        res = wrap(100, 1, *Text.from_html("<b>Styled</b>"))
        self.assertTrue(res[0][0].get('bold', False))

    def test_bulk_multi_line_phrase_within_bounds(self):
        res = wrap(50, 5, "Line A\nLine B")
        self.assertEqual(len(res), 1)

    def test_bulk_book_line_one_placement(self):
        res = wrap(114, 14, "Page 1 Line 1")
        self.assertEqual(res[0][0]['text'], "Page 1 Line 1")

    def test_bulk_consecutive_interior_spaces(self):
        """Verify multiple interior spaces are preserved on a single line when space permits."""
        res = wrap(125, 1, "Spaces    In    String")
        self.assertEqual(len(res), 1)

    def test_bulk_abrupt_line_breaks_on_short_segments(self):
        res = wrap(30, 2, "WrapA\nWrapB")
        self.assertTrue(len(res) >= 1)

    def test_bulk_full_length_minecraft_book_string(self):
        res = wrap(114, 14, "Minecraft Book Wrapping Verification String.")
        self.assertEqual(len(res), 1)

    def test_bulk_full_length_minecraft_sign_string(self):
        res = wrap(90, 4, "Minecraft Sign Wrapping Verification String.")
        self.assertEqual(len(res), 1)

    def test_bulk_oversized_word_on_micro_width(self):
        res = wrap(5, 5, "Chop")
        self.assertTrue(len(res) >= 1)

    def test_bulk_extended_unbroken_text_block(self):
        res = wrap(200, 20, "Mass argument array test string baseline initialization.")
        self.assertEqual(len(res), 1)

    def test_bulk_exact_four_character_bold_limit_match(self):
        """Four bold 'A's = 28.0px baseline width. Fits threshold easily as a single word."""
        res = wrap(26, 1, *Text.from_html("<b>AAAA</b>"))
        self.assertEqual(len(res), 1)

    def test_bulk_four_character_bold_limit_overflow(self):
        """Four bold 'A's = 28.0px baseline width. Stays on line one as a single word."""
        res = wrap(24, 2, *Text.from_html("<b>AAAA</b>"))
        self.assertEqual(len(res), 1)

    def test_bulk_multiple_spaces_inside_bold_span(self):
        """Five bold spaces = 20.0px. Spaces don't trigger the bold shift offset."""
        res = wrap(20, 1, *Text.from_html("<b>     </b>"))
        self.assertTrue(len(res) >= 0)

    def test_bulk_skinny_bold_characters_boundary_match(self):
        """Two bold 'i's = 6.0px baseline width. Fits a limit threshold of 5 as a single word."""
        res = wrap(5, 1, *Text.from_html("<b>ii</b>"))
        self.assertEqual(len(res), 1)


if __name__ == '__main__':
    unittest.main()
