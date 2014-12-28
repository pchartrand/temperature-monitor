import datetime
from nose.tools import istest
from unittest import TestCase

from temperature_monitor.lib.tempseries import TempDataset


class TemDatasetTests(TestCase):
    @istest
    def can_split_coordinate_series_in_distinct_series(self):
        dataset = dataset = TempDataset([
            [datetime.datetime(2014, 12, 26, 15, 6, 18), 1.1],
            [datetime.datetime(2014, 12, 26, 15, 6, 19), 1.2],
            [datetime.datetime(2014, 12, 26, 15, 6, 20), 1.3]
        ])

        self.assertEqual(
            [
                datetime.datetime(2014, 12, 26, 15, 6, 18),
                datetime.datetime(2014, 12, 26, 15, 6, 19),
                datetime.datetime(2014, 12, 26, 15, 6, 20)
            ],
            dataset.timestamps
        )
        self.assertEqual([1.1, 1.2, 1.3], dataset.temperatures)

    istest
    def len_property_keeps_track_of_number_of_measureements(self):
        dataset = TempDataset([[1,1.1], [2, 1.2], [3, 1.3]])
        self.assertEqual(3, dataset.len)

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

    @istest
    def can_get_temperature_variation_and_time_variation(self):
        dataset = TempDataset([
            [datetime.datetime(2014, 12, 26, 15, 6, 18), 12.1],
            [datetime.datetime(2014, 12, 26, 15, 6, 19), 11.2],
            [datetime.datetime(2014, 12, 26, 15, 6, 20), 11.1]
        ])
        self.assertEqual(2L, dataset.time_variation_in_seconds)
        self.assertEqual(-1.0, dataset.temperature_variation)
