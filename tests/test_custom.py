# pylint: skip-file
import unittest
from testing_imports import *
from HTMLTestRunner import HTMLTestRunner


class CustomTestsEx2(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", [2016])

    def test_custom_1(self):
        # Check if potential and short_name are correct
        filtered_df = find_max_col(self.data, "potential", ["short_name", "potential"])
        expected = pd.DataFrame({"short_name": ['L. Messi'], "potential": [95]})
        # Comparing dataframes is a bit complex, you can use this if you are sure that there are no NaNs
        self.assertTrue(
            (filtered_df.reset_index(drop=True) == expected.reset_index(drop=True)).all().all())

    def test_custom_2(self):
        # Check if potential and short_name are correct
        filtered_df = find_max_col(self.data, "weight_kg", ["short_name", "weight_kg"])
        expected = pd.DataFrame({"short_name": ['T. Wiese', 'K. Van Hout', 'A. Akinfenwa'],
                                 "weight_kg": [110, 110, 110]})
        # Comparing dataframes is a bit complex, you can use this if you are sure that there are no NaNs
        self.assertTrue(
            (filtered_df.reset_index(drop=True) == expected.reset_index(drop=True)).all().all())


class CustomTestsEx3(unittest.TestCase):

    @classmethod
    def setUp(cls):
        # Create some fake data
        cls.data = pd.DataFrame({"short_name": ["L. Messi", "A. Putellas", "A. Hegerberg"],
                                 "gender": ["M", "F", "F"],
                                 "year": [2021, 2021, 2022],
                                 "height_cm": [169, 171, 177],
                                 "weight_kg": [67, 66, 70]})

    def test_custom_3(self):
        male_bmi = calculate_bmi(self.data, "F", 2021, ["short_name"])
        self.assertEqual(male_bmi["short_name"].iloc[0], "A. Putellas")
        self.assertEqual(male_bmi["BMI"].iloc[0], 66 / (1.71 * 1.71))


class CustomTestsEx4(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", [2016, 2017, 2018])

    def test_custom_4(self):
        ids = [176580, 168542]
        columns_of_interest = ["overall", "player_positions"]
        data_dict = players_dict(self.data, ids, columns_of_interest)
        data_dict = clean_up_players_dict(data_dict, [("player_positions", "one")])
        # Check a couple of values
        self.assertCountEqual(data_dict[176580]["overall"], [90, 92, 92])
        self.assertCountEqual(data_dict[168542]["player_positions"], 'CAM, LM')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CustomTestsEx2))
    suite.addTest(unittest.makeSuite(CustomTestsEx3))
    suite.addTest(unittest.makeSuite(CustomTestsEx4))
    runner = HTMLTestRunner(log=True, verbosity=2, output='reports_custom',
                            title='PAC4', description='PAC4 custom tests',
                            report_name='Custom tests')
    runner.run(suite)