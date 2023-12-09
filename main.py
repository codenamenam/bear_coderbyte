# 실제 은행 통합, ATM 하드웨어(cash bin 등) 미래에 통합 예정이고 컨트롤러 파트를 현재 테스트 가능해야함

# 네트워크 연결 오류
class ConnectionError(Exception):
    def __str__(self):
        return "네트워크 연결 오류"

# 은행 네트워크 연결
class BankNetwork:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            # 네트워크 연결 구현...
            pass
            #raise ConnectionError
        except:
            # 오류 발생
            raise ConnectionError

# Bank API
# ATM에게 PIN 전송X, PIN이 맞는지 확인만 함
class BankAPI:
    # 카드와 핀번호 유효성 확인
    def verify_pin(self, card_number, pin):
        if card_number is not None and len(pin) == 4:
            return True
        else:
            return False

    def get_account_balance(self, card_number, account_type):
        # 잔고 GET API 구현
        return 300000

    def post_account_deposit(self, card_number, account_type, amount):
        # 입금 POST API 구현
        return 300000 + int(amount)

    def post_account_withdraw(self, card_number, account_type, amount):
        return 300000 - int(amount)


# ATM 컨트롤러
# 카드 삽입, 핀 입력, 계좌 선택, 잔액 확인 입금 인출 등의 흐름 컨트롤
class ATMController:
    def __init__(self):
        print("안녕하세요. OO은행 ATM입니다.")
        try:
            self.network = BankNetwork()
            self.bank = BankAPI()
            self.cardNumber = None
            self.pin = None
            self.accountType = None
            self.option = None
            self.isCardInserted = False
            self.isPinVerified = False
        except ConnectionError:
            print("초기화 중 오류가 발생했습니다.")
            raise ConnectionError

    # 카드 삽입
    def insert_card(self):
        print("카드를 삽입해주세요.")
        card_number = input()
        self.isCardInserted = True

        if len(card_number) == 16:
            self.cardNumber = card_number
            self.enter_pin()
        else:
            print("유효하지 않은 카드입니다.")
            self.isCardInserted = False
        return

    # 핀 입력
    def enter_pin(self):
        print("핀 번호를 입력해주세요.")
        pin = input()
        self.isPinVerified = self.bank.verify_pin(self.cardNumber, pin)
        if self.isPinVerified:
            self.pin = pin
        else:
            print("유효하지 않은 핀입니다.")

    # 계좌 선택
    def select_account(self):
        print("계좌를 선택해주세요.")
        print("1. 자유 입출금")
        print("2. 예금")
        self.accountType = input()
        self.show_options()

    # 옵션 선택
    def show_options(self):
        print("옵션을 선택해주세요.")
        print("1. 잔고 확인")
        print("2. 예금")
        print("3. 인출")
        self.option = input()

    def perform_transaction(self):
        if self.option == "1":
            balance = self.bank.get_account_balance(self.cardNumber, self.accountType)
            print(f"잔고: ${balance}")
        elif self.option == "2":
            print("입금하실 금액을 입력해주세요.")
            amount = input()
            balance = self.bank.post_account_deposit(self.cardNumber, self.accountType, amount)
            print("입금이 완료되었습니다.")
            print(f"잔고: ${balance}")

        elif self.option == "3":

            while True:
                balance = self.bank.get_account_balance(self.cardNumber, self.accountType)
                print(f"인출하실 금액을 ${balance} 이하로 입력해주세요.")
                amount = int(input("인출할 금액을 입력하세요: $"))

                if int(amount) > int(balance):
                    print("잔액보다 큰 금액을 인출할 수 없습니다. 다시 입력해주세요.")
                else:
                    balance = self.bank.post_account_withdraw(self.cardNumber, self.accountType, amount)
                    print("인출이 완료되었습니다.")
                    print(f"잔고: ${balance}")
                    break

while True:
    try:
        # ATM 초기화
        atm = ATMController()

        # 카드 삽입
        atm.insert_card()

        if atm.isCardInserted and atm.isPinVerified:
            # 계좌 선택
            atm.select_account()

            # 거래 확인
            atm.perform_transaction()

            print("이용해주셔서 감사합니다. 놓고가시는 물건이 없는지 확인해주세요.")
    except Exception as e:
        print("사유:", e)
        break

    print()