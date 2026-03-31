import datetime

class MetroKart:
    def __init__(self):
        self.pin = "1234"
        self.balance = 0.0
        self.daily_limit = 100.0
        self.added_today = 0.0
        self.mode = 'normal'
        
        self.ride_count = 0
        self.total_paid = 0.0
        self.total_discount = 0.0
        self.transactions = []

    def run(self):
        print("=== MetroKart Simulyatoruna Xoş Gəlmisiniz ===")
        for cehd in range(3, 0, -1):
            user_pin = input(f"4 rəqəmli PIN daxil edin ({cehd} cəhdiniz qaldı): ")
            if user_pin == self.pin:
                self.show_menu()
                return
            print("Yanlış PIN!")
            
        print("3 dəfə yanlış PIN daxil etdiniz. Proqram dayandırılır.")

    def show_menu(self):
        while True:
            print("\n--- ƏSAS MENYU ---")
            print("1) Balansı göstər")
            print("2) Balans artır")
            print("3) Gediş et (turniketi keç)")
            print("4) Son əməliyyatlara bax")
            print("5) Günlük statistika")
            print("6) Parametrlər")
            print("0) Çıxış")
            
            secim = input("Seçiminizi edin: ")

            if secim == '1':
                print(f"Cari balansınız: {self.balance:.2f} AZN")
            elif secim == '2':
                self.add_balance()
            elif secim == '3':
                self.ride()
            elif secim == '4':
                self.show_transactions()
            elif secim == '5':
                self.show_stats()
            elif secim == '6':
                self.settings()
            elif secim == '0':
                print("Proqramdan çıxılır. Uğurlar!")
                break
            else:
                print("Yanlış seçim! 0-6 arası rəqəm daxil edin.")

    def add_balance(self):
        try:
            mebleg = float(input("Artırmaq istədiyiniz məbləği daxil edin (AZN): "))
        except ValueError:
            print("Xəta: Rəqəm daxil etməlisiniz!")
            return

        if mebleg <= 0:
            print("Xəta: Məbləğ müsbət olmalıdır!")
            return

        if self.added_today + mebleg > self.daily_limit:
            print(f"Xəta: Gündəlik limit ({self.daily_limit} AZN) aşıla bilməz.")
            return

        self.balance += mebleg
        self.added_today += mebleg
        self.log_transaction("Balans artırma", mebleg, 0, self.balance)
        
        print(f"Balans uğurla artırıldı! Yeni balans: {self.balance:.2f} AZN")

    def ride(self):
        base_fare = 0.40
        actual_fare = 0.40
        discount = 0.0

        if self.mode == 'telebe':
            actual_fare = 0.20
        elif self.mode == 'pensiyaci':
            actual_fare = 0.15
        else:
            current_ride = self.ride_count + 1
            if 2 <= current_ride <= 4:
                actual_fare = 0.36
            elif current_ride >= 5:
                actual_fare = 0.30
                
        discount = base_fare - actual_fare

        if self.balance >= actual_fare:
            self.execute_ride(actual_fare, discount)
        else:
            if self.mode == 'normal' and 0.30 <= self.balance < actual_fare:
                cavab = input("Balans kifayət etmir. Təcili keçid edilsin? (Bəli - B / Xeyr - X): ").lower()
                if cavab == 'b':
                    self.execute_ride(actual_fare, discount)
                    print("Təcili keçid aktiv edildi. Balansınızda borc yarandı.")
                else:
                    print("Keçid rədd edildi.")
            else:
                print("Xəta: Balansınız kifayət etmir.")

    def execute_ride(self, fare, discount):
        self.balance -= fare
        self.ride_count += 1
        self.total_paid += fare
        self.total_discount += discount
        self.log_transaction("Gediş", -fare, discount, self.balance)
        
        print(f"Keçid uğurlu! Çıxılan məbləğ: {fare:.2f} AZN")
        print(f"Qalan balans: {self.balance:.2f} AZN")

    def show_transactions(self):
        if not self.transactions:
            print("Heç bir əməliyyat tapılmadı.")
            return

        try:
            n = int(input("Neçə son əməliyyatı görmək istəyirsiniz?: "))
        except ValueError:
            print("Xəta: Tam ədəd daxil edin.")
            return

        recent = self.transactions[-n:]
        print(f"\n--- SON {n} ƏMƏLİYYAT ---")
        for t in reversed(recent):
            print(f"[{t['date']}] {t['type']} | Məbləğ: {t['amount']:.2f} | Endirim: {t['discount']:.2f} | Yeni Balans: {t['new_balance']:.2f}")

    def show_stats(self):
        print("\n--- GÜNLÜK STATİSTİKA ---")
        print(f"Ümumi gediş sayı: {self.ride_count}")
        print(f"Xərclənən ümumi məbləğ: {self.total_paid:.2f} AZN")
        print(f"Qənaət edilən (Endirim): {self.total_discount:.2f} AZN")
        print(f"Artırılan ümumi məbləğ: {self.added_today:.2f} AZN")

    def settings(self):
        print("\n--- PARAMETRLƏR ---")
        print(f"1) Limit dəyiş (Cari: {self.daily_limit} AZN)")
        print(f"2) Rejim seçimi (Cari: {self.mode})")
        
        secim = input("Seçim: ")
        if secim == '1':
            yeni_limit = float(input("Yeni limit (AZN): "))
            if yeni_limit >= 1:
                self.daily_limit = yeni_limit
                print("Limit yeniləndi!")
        elif secim == '2':
            yeni_rejim = input("Rejimlər (normal, telebe, pensiyaci): ").lower()
            if yeni_rejim in ['normal', 'telebe', 'pensiyaci']:
                self.mode = yeni_rejim
                print(f"Rejim '{yeni_rejim}' olaraq təyin edildi.")
            else:
                print("Belə rejim yoxdur.")

    def log_transaction(self, t_type, amount, discount, new_balance):
        zaman = datetime.datetime.now().strftime("%H:%M:%S")
        self.transactions.append({
            'date': zaman,
            'type': t_type,
            'amount': amount,
            'discount': discount,
            'new_balance': new_balance
        })

if __name__ == "__main__":
    app = MetroKart()
    app.run()