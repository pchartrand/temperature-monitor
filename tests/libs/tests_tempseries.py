from nose.tools import istest

from unittest import TestCase

from templibs.tempseries import TempDataset


class TemDatasetTests(TestCase):
    @istest
    def can_split_coordinate_series_in_distinct_series(self):
        dataset = TempDataset([[1,1.1], [2, 1.2], [3, 1.3]])

        self.assertEqual([1, 2, 3], dataset.timestamps)
        self.assertEqual([1.1, 1.2, 1.3], dataset.temperatures)

    @istest
    def can_calculate_average_temperature(self):
        dataset = TempDataset([[1,1.1], [2, 1.2], [3, 1.3]])

        self.assertEqual(1.2, dataset.get_average_temperature())

    @istest
    def constructor_calculates_average_temperature(self):
        dataset = TempDataset([[1,1.1], [2, 1.2], [3, 1.3]])

        self.assertEqual(1.2, dataset.average_temperature)

    @istest
    def dataset_behaves_well_when_no_serie_is_given(self):
        dataset = TempDataset([])

        self.assertEqual([], dataset.timestamps)
        self.assertEqual([], dataset.temperatures)
        self.assertIsNone(dataset.average_temperature)
