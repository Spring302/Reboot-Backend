def change_currency_language(kor_money):
    kor_money = kor_money.replace(" ", "").replace(",", "").replace(".", "")
    for i, word in enumerate(kor_money):
        if word == "억":
            ten_thounsand_won = int(kor_money[:i]) * 10000
            rest_won = 0
            if len(kor_money) > i+1:
                rest_won = int(kor_money[i+1:])
            return ten_thounsand_won + rest_won
