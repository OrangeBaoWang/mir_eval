"""
"""

import unittest

from mir_eval import chord


class ChordTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pitch_class_to_semitone(self):
        self.assertEqual(chord.pitch_class_to_semitone('Gbb'), 5)
        self.assertEqual(chord.pitch_class_to_semitone('G'), 7)
        self.assertEqual(chord.pitch_class_to_semitone('G#'), 8)
        self.assertEqual(chord.pitch_class_to_semitone('Cb'), 11)
        self.assertEqual(chord.pitch_class_to_semitone('B#'), 0)

        self.assertRaises(
            chord.InvalidChordException,
            chord.pitch_class_to_semitone, "Cab")

        self.assertRaises(
            chord.InvalidChordException,
            chord.pitch_class_to_semitone, "#C")

        self.assertRaises(
            chord.InvalidChordException,
            chord.pitch_class_to_semitone, "bG")

    def test_scale_degree_to_semitone(self):
        self.assertEqual(chord.scale_degree_to_semitone('b7'), 10)
        self.assertEqual(chord.scale_degree_to_semitone('#3'), 5)
        self.assertEqual(chord.scale_degree_to_semitone('1'), 0)
        self.assertEqual(chord.scale_degree_to_semitone('b1'), 11)
        self.assertEqual(chord.scale_degree_to_semitone('#7'), 0)
        self.assertEqual(chord.scale_degree_to_semitone('bb5'), 5)

        self.assertRaises(
            chord.InvalidChordException,
            chord.scale_degree_to_semitone, "7b")

        self.assertRaises(
            chord.InvalidChordException,
            chord.scale_degree_to_semitone, "4#")

        self.assertRaises(
            chord.InvalidChordException,
            chord.scale_degree_to_semitone, "77")

    def test_well_formedness(self):
        # Good chords should pass.
        for chord_label in ['C', 'Eb:min/5', 'A#:dim7',
                            'B:maj(*1,*5)/3', 'A#:sus4']:
            chord._validate(chord_label)

        # Bad chords should fail.
        self.assertRaises(
            chord.InvalidChordException, chord._validate, "C::maj")
        self.assertRaises(
            chord.InvalidChordException, chord._validate, "C//5")
        self.assertRaises(
            chord.InvalidChordException, chord._validate, "C((4)")
        self.assertRaises(
            chord.InvalidChordException, chord._validate, "C5))")
        self.assertRaises(
            chord.InvalidChordException, chord._validate, "C:maj(*3/3")
        self.assertRaises(
            chord.InvalidChordException, chord._validate, "Cmaj*3/3)")

    def test_split(self):
        self.assertEqual(chord.split('C'), ['C', 'maj', set(), '1'])
        self.assertEqual(chord.split('B:maj(*1,*3)/5'),
                         ['B', 'maj', set(['*1', '*3']), '5'])
        self.assertEqual(chord.split('Ab:min/b3'), ['Ab', 'min', set(), 'b3'])
        self.assertEqual(chord.split('N'), ['N', '', set(), ''])

    def test_join(self):
        self.assertEqual(chord.join('F#'), 'F#')
        self.assertEqual(chord.join('F#', quality='hdim7'), 'F#:hdim7')
        self.assertEqual(
            chord.join('F#', extensions={'*b3', '4'}), 'F#:(*b3,4)')
        self.assertEqual(chord.join('F#', bass='b7'), 'F#/b7')
        self.assertEqual(chord.join('F#', extensions={'*b3', '4'}, bass='b7'),
                         'F#:(*b3,4)/b7')
        self.assertEqual(chord.join('F#', quality='hdim7', bass='b7'),
                         'F#:hdim7/b7')
        self.assertEqual(chord.join('F#', 'hdim7', {'*b3', '4'}, 'b7'),
                         'F#:hdim7(*b3,4)/b7')

if __name__ == "__main__":
    unittest.main()