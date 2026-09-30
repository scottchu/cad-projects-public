from pathlib import Path
import sys
import unittest

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from face_vector import CLASSES, classify, classify_rgb, contours, generate, split_self_touching, svg_path  # noqa: E402


class FaceVectorTests(unittest.TestCase):
    source = PROJECT / "references/d4-approved.png"

    def test_masks_are_exclusive_and_background_is_not_white_car_sticker(self):
        masks, background = classify(self.source)
        summed = np.add.reduce([masks[name] for name in CLASSES])
        self.assertTrue(np.all(summed <= 1), "visible classes overlap")
        self.assertGreater(background.sum(), 100_000)
        self.assertFalse(masks["white"][0, 0], "external white canvas became sticker fill")
        self.assertGreater(masks["white"].sum(), 10_000, "white vehicle border/details disappeared")

    def test_all_five_classes_and_critical_regions_survive(self):
        masks, _ = classify(self.source)
        for name in CLASSES:
            self.assertGreater(masks[name].sum(), 100, name)
        self.assertGreater(masks["deep-blue"][850:950, 330:620].sum(), 500, "DJZY 608 deep-blue lettering missing")
        self.assertGreater(masks["glass-mix"][250:470, 300:920].sum(), 10_000, "windscreen glass-mix missing")
        self.assertGreater(masks["white"][540:640, 700:910].sum(), 100, "GRENADIER lettering/detail missing")

    def test_generation_is_deterministic_and_preserves_source_bytes(self):
        original = self.source.read_bytes()
        report = generate(self.source, PROJECT / "work/test-face.svg", PROJECT / "work/test-report.json")
        first = (PROJECT / "work/test-face.svg").read_bytes()
        generate(self.source, PROJECT / "work/test-face.svg", PROJECT / "work/test-report.json")
        self.assertEqual(first, (PROJECT / "work/test-face.svg").read_bytes())
        self.assertEqual(original, self.source.read_bytes())
        self.assertEqual(report["units"], "source-image-units")

    def test_closed_contours_keep_diagonal_touch_and_hole_topology(self):
        diagonal = np.zeros((3, 3), dtype=bool)
        diagonal[0, 0] = diagonal[1, 1] = True
        diagonal_paths = contours(diagonal)
        self.assertEqual(len(diagonal_paths), 2, "diagonal-only contact must not merge components")
        donut = np.ones((5, 5), dtype=bool)
        donut[1:4, 1:4] = False
        donut_paths = contours(donut)
        self.assertEqual(len(donut_paths), 2, "inner hole boundary must be written")
        for path in diagonal_paths + donut_paths:
            self.assertEqual(path[0], path[-1], "every SVG contour must close")
        written = svg_path(donut_paths)
        self.assertEqual(written.count(" Z"), 2, "written compound path lost a contour")

    def test_dark_neutral_tire_block_is_gray_but_black_groove_stays_black(self):
        fixture = np.full((1254, 1254, 3), 120, dtype=np.int16)
        fixture[930, 120] = (58, 58, 58)  # a source-style dark tire block
        fixture[930, 121] = (20, 20, 20)  # adjacent black groove
        masks, _ = classify_rgb(fixture)
        self.assertTrue(masks["gray"][930, 120])
        self.assertTrue(masks["black"][930, 121])

    def test_repeated_vertex_walk_becomes_simple_closed_loops(self):
        # Two diagonal lobes share a vertex while the enclosing walk is
        # connected elsewhere; this is the real SVG import failure pattern.
        walk = [(0, 0), (2, 0), (2, 2), (1, 1), (0, 2), (0, 0), (1, 1), (1, 3), (-1, 3), (-1, 1), (0, 0)]
        loops = split_self_touching(walk)
        self.assertGreater(len(loops), 1)
        self.assertEqual(sum(len(loop) - 1 for loop in loops), len(walk) - 1)
        for loop in loops:
            self.assertEqual(loop[0], loop[-1])
            self.assertEqual(len(set(loop[:-1])), len(loop) - 1)

    def test_written_d4_contours_are_simple_closed_loops(self):
        masks, _ = classify(self.source)
        for name in CLASSES:
            for loop in contours(masks[name]):
                self.assertEqual(loop[0], loop[-1], name)
                self.assertEqual(len(set(loop[:-1])), len(loop) - 1, name)


if __name__ == "__main__":
    unittest.main()
