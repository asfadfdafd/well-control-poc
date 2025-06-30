import unittest
from src.inference.detector import Detector

class TestDetector(unittest.TestCase):
    def test_predict_format(self):
        # Тестируем, что метод возвращает пару (float, int)
        sample = {'feature1': 0.0, 'feature2': 0.0}
        det = Detector()
        score, flag = det.predict(sample)
        self.assertIsInstance(score, float)
        self.assertIn(flag, (0, 1))

if __name__ == "__main__":
    unittest.main()
