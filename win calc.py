teamapr = int(input("TeamA PR: "))
teambpr = int(input("TeamB PR: "))

homecourt = 10 # 10%
homecourtadv = teamapr*(homecourt/100)
winCoeff = 50

expected_win = 1 / (10**(-((teamapr-teambpr)+homecourtadv)/winCoeff) + 1)
expected_win = round(expected_win, 4) * 100

print(str(expected_win) + "%\n")