import unittest

from unittest.mock import MagicMock
from app.services.services import ExtractionService
from app.ocr_modules.modules import ExtractionModuleFactory, BaseExtractionModule
from app.llm_integration.llm import QwenFieldMapper
from app.dto.models import Detection, ExtractionResponse
from PIL import Image

# Example PHOCR output to test
phocr_outputs = [
    [('5', 0.7510972338414347), ('女F', 0.9102697548677771), ('Z683365', 0.8136179417209157), ('***AZ', 0.9162871027748309), ('樂永晴', 0.9210272296431473), ('(96-90)', 0.905446693390135), ('SAMPLE', 0.9094322867069041), ('SAMPLE', 0.9112895413583832), ('special(*chars)', 0.95)],
    [('26-11-18', 0.9073199903932333), ('03-06-1985', 0.9065046042868535), ('Z683365(5)', 0.8552984408642076), ('簽發日期 Date of Issue', 0.8980808507605915), ('出生日期 Date of Birth', 0.9094325203446194), ('LOK, Wing Ching', 0.9047981550914954), ('2867 3057 2532', 0.9059406701911946), ('SAMPLE SAMPLE', 0.9099177744401039)],
    [('香港永久性居民身份證', 0.9219284235308426), ('HONG KONG PERMANENT IDENTITY CARD', 0.9111978062662717)]
]

class TestPHOCROutput(unittest.TestCase):
    def test_phocr_output_format(self):
        for output in phocr_outputs:
            for item in output:
                with self.subTest(item=item):
                    self.assertIsInstance(item, tuple)
                    self.assertEqual(len(item), 2)
                    text, score = item
                    self.assertIsInstance(text, str)
                    self.assertIsInstance(score, float)
                    self.assertGreaterEqual(score, 0.0)
                    self.assertLessEqual(score, 1.0)

    def test_phocr_output_content(self):
        # Example: check that certain expected values are present
        flat = [text for output in phocr_outputs for text, _ in output]
        self.assertIn('香港永久性居民身份證', flat)
        self.assertIn('SAMPLE', flat)
        self.assertIn('Z683365', flat)



class TestPHOCROutput(unittest.TestCase):
    def test_phocr_output_format(self):
        for output in phocr_outputs:
            for item in output:
                self.assertIsInstance(item, tuple)
                self.assertEqual(len(item), 2)
                text, score = item
                self.assertIsInstance(text, str)
                self.assertIsInstance(score, float)
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)

    def test_phocr_output_content(self):
        flat = [text for output in phocr_outputs for text, _ in output]
        self.assertIn('香港永久性居民身份證', flat)
        self.assertIn('女F', flat)

    def setUp(self):
        self.mock_module = MagicMock(spec=BaseExtractionModule)
        # Always return two detections for any extract call
        self.mock_module.extract.return_value = {
            "txts": ["A", "B"],
            "scores": [0.9, 0.8],
            "boxes": [[0,0,1,1],[1,1,2,2]],
            "lang_type": "en",
            "elapse": 0.1
        }
        factory = ExtractionModuleFactory({'en': self.mock_module})
        # Patch get_module to always return the mock module
        factory.get_module = lambda lang: self.mock_module
        preproc = MagicMock()
        preproc.preprocess.side_effect = lambda img: img
        quality = MagicMock()
        field_mapper = MagicMock()
        field_mapper.map_fields.return_value = {"field1": "A", "field2": "B"}
        self.service = ExtractionService(factory, preproc, quality, field_mapper)
        self._orig_image_open = Image.open
        Image.open = lambda *a, **kw: Image.new('RGB', (10, 10))

    def tearDown(self):
        self.mock_module.reset_mock()
        Image.open = self._orig_image_open

    def test_extract_single_page_basic(self):
        img = Image.new('RGB', (10, 10))
        img_path = 'test_img.png'
        img.save(img_path)
        try:
            resp = self.service.extract_single_page(img_path, 'en', 1, ["field1", "field2"])
            self.assertIsInstance(resp, ExtractionResponse)
            self.assertEqual(resp.total_detections, 2)
        finally:
            import os
            if os.path.exists(img_path):
                os.remove(img_path)

    def test_extract_single_page_empty_fields(self):
        img = Image.new('RGB', (10, 10))
        img_path = 'test_img2.png'
        img.save(img_path)
        try:
            resp = self.service.extract_single_page(img_path, 'en', 1, [])
            self.assertIsInstance(resp, ExtractionResponse)
            self.assertEqual(resp.total_detections, 2)
        finally:
            import os
            if os.path.exists(img_path):
                os.remove(img_path)

    def test_extract_single_page_empty_ocr(self):
        self.mock_module.extract.return_value = {
            "txts": [], "scores": [], "boxes": [], "lang_type": "en", "elapse": 0.1
        }
        img = Image.new('RGB', (10, 10))
        img_path = 'test_img6.png'
        img.save(img_path)
        try:
            resp = self.service.extract_single_page(img_path, 'en', 1, ["field1"])
            self.assertEqual(resp.total_detections, 0)
        finally:
            import os
            if os.path.exists(img_path):
                os.remove(img_path)

    def test_extract_single_page_invalid_boxes(self):
        self.mock_module.extract.return_value = {
            "txts": ["A"], "scores": [0.9], "boxes": [None], "lang_type": "en", "elapse": 0.1
        }
        img = Image.new('RGB', (10, 10))
        img_path = 'test_img7.png'
        img.save(img_path)
        try:
            resp = self.service.extract_single_page(img_path, 'en', 1, ["field1"])
            # The service may not skip None boxes, so expect 1 detection
            self.assertEqual(len(resp.detections), 1)
        finally:
            import os
            if os.path.exists(img_path):
                os.remove(img_path)

    def test_phocr_output_empty(self):
        # Test with empty PHOCR output
        empty_output = []
        for output in empty_output:
            for item in output:
                self.assertIsInstance(item, tuple)
        self.assertEqual(len(empty_output), 0)

    def test_phocr_output_score_bounds(self):
        # Test edge cases for score bounds
        outputs = [[('test', 0.0)], [('test', 1.0)]]
        for output in outputs:
            for item in output:
                _, score = item
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)

    def test_phocr_output_types(self):
        # Test that wrong types are caught
        bad_outputs = [[(123, 0.5)], [('text', 'not_a_float')]]
        for output in bad_outputs:
            for item in output:
                with self.assertRaises(AssertionError):
                    self.assertIsInstance(item[0], str)
                    self.assertIsInstance(item[1], float)

    def test_phocr_output_duplicates(self):
        # Test that duplicate values are present as expected
        flat = [text for output in phocr_outputs for text, _ in output]
        self.assertGreater(flat.count('SAMPLE'), 1)

    def test_phocr_output_special_characters(self):
        # Test for special characters in output
        flat = [text for output in phocr_outputs for text, _ in output]
        self.assertTrue(any('*' in t for t in flat))
        self.assertTrue(any('(' in t and ')' in t for t in flat))

    def test_phocr_output_date_formats(self):
        # Test for date-like strings
        flat = [text for output in phocr_outputs for text, _ in output]
        self.assertTrue(any('-' in t for t in flat))
        self.assertTrue(any('/' not in t for t in flat))

    def test_phocr_output_unicode(self):
        # Test for presence of unicode (Chinese) characters
        flat = [text for output in phocr_outputs for text, _ in output]
        self.assertTrue(any(ord(c) > 127 for t in flat for c in t))

if __name__ == "__main__":
    unittest.main()
