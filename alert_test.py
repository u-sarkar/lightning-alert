"""
#####################################
##           Test Cases            ##
#####################################
Project Name:
  Lightning Alert
Description:
  Printing a lightning strike with the correct asset name and asset owner
Script Parameters:
  | --------------------- | --------- | ---------------------------------------------------------- |
  | Parameter Name        | Type      | Description                                                |
  | --------------------- | --------- | ---------------------------------------------------------- |
  | lightning_file        | Mandatory | Lightning File path, each line is a single json entry      |
  |                       |           | for a strike                                               |
  |                       |           |                                                            |
  |asset_file             | Mandatory | asset File path, list of json object of asset              |
  | --------------------- | --------- | ---------------------------------------------------------- |
Feature:
  In order to: Check lightning alert
  As: a Software Engineer
  I want: To ensure that all the process involved with it should work correctly.
Scenarios:
  Scenario 1:
  Given: Lightning file and asset file is provided
    And: flashType is as 0
    Then: Print a console output as > lightning alert for <assetOwner>:<assetName>
  Scenario 2:
  Given: Lightning file and asset file is provided
    And: flashType is as 1
    Then: Print a console output as > lightning alert for <assetOwner>:<assetName>
  Scenario 3:
  Given: Lightning file and asset file is provided
    And: flashType is as 9
    Then: Print a console output as > heartbeat alert for <assetOwner>:<assetName>
  Scenario 4:
  Given: Lightning file and asset file is provided
    And: flashType is as 0
    And: Repeated lightning strike for the same quad key
    Then: Print only one time console output as > lightning alert for <assetOwner>:<assetName>
"""
import sys
import io
import unittest
import tempfile

import alert


class TestLightningAlert(unittest.TestCase):

    def test_flash_type_0_check(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lightning_file_path = tempfile.mkstemp()[1]
        with open(lightning_file_path, 'w') as lightning_file:
            lightning_file.write('{"flashType":0, '
                                 '"latitude":33.5524951, '
                                 '"longitude":-94.5822016 }')
        asset_file_path = tempfile.mkstemp()[1]
        with open(asset_file_path, 'w') as asset_file:
            asset_file.write('[{"assetName": "Dante Street",'
                             '"quadKey": "023113203031",'
                             '"assetOwner": "6720"}]')
        alert.read_line_from_file(lightning_file_path, asset_file_path)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "lightning alert for 6720:Dante Street\n")

    def test_flash_type_1_check(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lightning_file_path = tempfile.mkstemp()[1]
        with open(lightning_file_path, 'w') as lightning_file:
            lightning_file.write('{"flashType":1, '
                                 '"latitude":33.5524951, '
                                 '"longitude":-94.5822016 }')
        asset_file_path = tempfile.mkstemp()[1]
        with open(asset_file_path, 'w') as asset_file:
            asset_file.write('[{"assetName": "Dante Street",'
                             '"quadKey": "023113203031",'
                             '"assetOwner": "6720"}]')
        alert.read_line_from_file(lightning_file_path, asset_file_path)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "lightning alert for 6720:Dante Street\n")

    def test_flash_type_9_check(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lightning_file_path = tempfile.mkstemp()[1]
        with open(lightning_file_path, 'w') as lightning_file:
            lightning_file.write('{"flashType":9, '
                                 '"latitude":33.5524951, '
                                 '"longitude":-94.5822016 }')
        asset_file_path = tempfile.mkstemp()[1]
        with open(asset_file_path, 'w') as asset_file:
            asset_file.write('[{"assetName": "Dante Street",'
                             '"quadKey": "023113203031",'
                             '"assetOwner": "6720"}]')
        alert.read_line_from_file(lightning_file_path, asset_file_path)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "heartbeat alert for 6720:Dante Street\n")

    def test_repeat_strike_check(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        lightning_file_path = tempfile.mkstemp()[1]
        with open(lightning_file_path, 'w') as lightning_file:
            lightning_file.write('{"flashType":1, '
                                 '"latitude":33.5524951, '
                                 '"longitude":-94.5822016 }\n')
            lightning_file.write('{"flashType":0, '
                                 '"latitude":33.5524951, '
                                 '"longitude":-94.5822016 }\n')
        asset_file_path = tempfile.mkstemp()[1]
        with open(asset_file_path, 'w') as asset_file:
            asset_file.write('[{"assetName": "Dante Street",'
                             '"quadKey": "023113203031",'
                             '"assetOwner": "6720"}]')
        alert.read_line_from_file(lightning_file_path, asset_file_path)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "lightning alert for 6720:Dante Street\n")


if __name__ == '__main__':
    alert.setup_logger()
    unittest.main()
