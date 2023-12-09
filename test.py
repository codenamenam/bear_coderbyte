import unittest
from unittest.mock import patch
from io import StringIO
from main import ATMController

class TestATMController(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def assert_output(self, expected_output, mock_stdout):
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output.strip())

    @patch('builtins.input', side_effect=['1234567890123456', '123'])
    def test_insert_card(self, mock_input):
        atm = ATMController()
        atm.insert_card()
        self.assertTrue(atm.isCardInserted)
        self.assertTrue(atm.isPinVerified)

    @patch('builtins.input', side_effect=['1234567890123456', '1234'])
    def test_enter_pin(self, mock_input):
        atm = ATMController()
        atm.insert_card()
        atm.enter_pin()
        self.assertTrue(atm.isPinVerified)

    @patch('builtins.input', side_effect=['1'])
    def test_select_account(self, mock_input):
        atm = ATMController()
        atm.insert_card()
        atm.enter_pin()
        atm.select_account()
        self.assertEqual(atm.accountType, '1')

    @patch('builtins.input', side_effect=['1'])
    def test_show_options(self, mock_input):
        atm = ATMController()
        atm.insert_card()
        atm.enter_pin()
        atm.select_account()
        atm.show_options()
        expected_output = "옵션을 선택해주세요.\n1. 잔고 확인\n2. 예금\n3. 인출"
        self.assert_output(expected_output)

    @patch('builtins.input', side_effect=['1'])
    def test_perform_transaction_check_balance(self, mock_input):
        atm = ATMController()
        atm.insert_card()
        atm.enter_pin()
        atm.select_account()
        atm.option = '1'
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            atm.perform_transaction()
            self.assertIn("잔고:", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['2', '1000'])
    def test_perform_transaction_deposit(self, mock_input):
        atm = ATMController()
        atm.insert_card()
        atm.enter_pin()
        atm.select_account()
        atm.option = '2'
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            atm.perform_transaction()
            self.assertIn("입금이 완료되었습니다.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['3', '300000'])
    def test_perform_transaction_withdraw(self, mock_input):
        atm = ATMController()
        atm.insert_card()
        atm.enter_pin()
        atm.select_account()
        atm.option = '3'
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            atm.perform_transaction()
            self.assertIn("인출이 완료되었습니다.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()

