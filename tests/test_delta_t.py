import os
import shutil
import unittest

import numpy as np

from LinoSPAD2.functions.delta_t import (
    calculate_and_save_timestamp_differences,
    collect_and_plot_timestamp_differences,
)
from LinoSPAD2.functions.fits import fit_with_gaussian


class TestDeltasFull(unittest.TestCase):
    def setUp(self):
        # Set up test variables
        self.path = "tests/test_data"
        self.pixels = [
            [x for x in range(66, 70)],
            [x for x in range(170, 178)],
        ]
        self.daughterboard_number = "NL11"
        self.motherboard_number = "#33"
        self.firmware_version = "2212b"
        self.timestamps = 300
        self.delta_window = 20e3
        self.rewrite = True
        self.range_left = -20e3
        self.range_right = 20e3
        self.same_y = False
        self.app_mask = True
        self.include_offset = False

    def test_a_deltas_save_positive(self):
        # Test positive case for deltas_save function
        work_dir = r"{}".format(os.path.realpath(__file__) + "../../..")
        os.chdir(work_dir)
        calculate_and_save_timestamp_differences(
            self.path,
            self.pixels,
            self.rewrite,
            self.daughterboard_number,
            self.motherboard_number,
            self.firmware_version,
            self.timestamps,
            self.delta_window,
            self.app_mask,
            self.include_offset,
        )

        # Check if the csv file is created
        self.assertTrue(
            os.path.isfile(
                "delta_ts_data/test_data_2212b-test_data_2212b.feather"
            )
        )

    # Negative test case
    # Invalid firmware version
    def test_b_deltas_save_negative(self):
        work_dir = r"{}".format(os.path.realpath(__file__) + "../../..")
        os.chdir(work_dir)
        # Test negative case for deltas_save function
        with self.assertRaises(TypeError):
            calculate_and_save_timestamp_differences(
                self.path,
                self.pixels,
                "2212",
                self.daughterboard_number,
                self.motherboard_number,
                self.firmware_version,
                self.timestamps,
                self.delta_window,
            )

    def test_c_delta_cp(self):
        # Test case for delta_cp function
        # Positive test case
        os.chdir(r"{}".format(os.path.realpath(__file__) + "/../.."))
        collect_and_plot_timestamp_differences(
            path=self.path,
            pixels=[x for x in range(67, 69)] + [x for x in range(173, 175)],
            rewrite=self.rewrite,
            range_left=self.range_left,
            range_right=self.range_right,
            same_y=self.same_y,
        )

        # Check if the plot file is created
        self.assertTrue(
            os.path.isfile(
                "results/delta_t/test_data_2212b-test_data_2212b_delta_t_grid.png"
            )
        )

    # TODO: need larger data set to get more delta ts
    def test_d_fit_wg_positive(self):
        # Test with valid input
        os.chdir(r"{}".format(os.path.realpath(__file__) + "/../.."))
        pix_pair = [67, 174]
        window = 20e3
        step = 5

        # Call the function
        fit_with_gaussian(self.path, pix_pair, window, step)

        # Assert that the function runs without raising any exceptions
        self.assertTrue(
            os.path.isfile(
                "results/fits/test_data_2212b-test_data_2212b_pixels_{},{}_fit.png".format(
                    pix_pair[0], pix_pair[1]
                )
            )
        )

    def tearDownClass():
        # Clean up after tests
        os.chdir(r"{}".format(os.path.realpath(__file__) + "/.."))
        shutil.rmtree("test_data/delta_ts_data")
        shutil.rmtree("test_data/results")


if __name__ == "__main__":
    unittest.main()
