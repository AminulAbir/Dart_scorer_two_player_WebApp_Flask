class Calculation:
    def __init__(self):
        self.totalA = 0
        self.totalB = 0

    def playerA(self, total1, d1):
        if d1 <= 60:
            if (d1 > 20 and d1 < 41) and d1 % 2 == 0:
                self.totalA = total1 - d1

                if self.totalA < 0:
                    self.totalA = total1 + d1
                    return "You can not score more than required!"
                else:
                    return self.totalA

            elif (d1 > 20 and d1 < 61) and d1 % 3 == 0:
                self.totalA = total1 - d1
                if self.totalA < 0:
                    self.totalA = total1 + d1
                    return "You can not score more than required!"
                else:
                    return self.totalA

            elif (d1 <= 20):
                self.totalA = total1 - d1
                if self.totalA < 0:
                    self.totalA = total1 + d1
                    return "You can not score more than required!"
                else:
                    return self.totalA

            elif (d1 == 50 or d1 == 25):
                self.totalA = total1 - d1
                if self.totalA < 0:
                    self.totalA = total1 + d1
                    return "You can not score more than required!"
                else:
                    return self.totalA
            else:
                return 'Wrong number you have selected. Please try again'

        else:
            return 'Wrong number you have selected. Please try again'

    def playerB(self, total2, d2):
        if d2 <= 60:
            if (d2 > 20 and d2 < 41) and d2 % 2 == 0:
                self.totalB = total2 - d2

                if self.totalB < 0:
                    self.totalB = total2 + d2
                    return "You can not score more than required!"
                else:
                    return self.totalB

            elif (d2 > 20 and d2 < 61) and d2 % 3 == 0:
                self.totalB = total2 - d2
                if self.totalB < 0:
                    self.totalB = total2 + d2
                    return "You can not score more than required!"
                else:
                    return self.totalB

            elif (d2 <= 20):
                self.totalB = total2 - d2
                if self.totalB < 0:
                    self.totalB = total2 + d2
                    return "You can not score more than required!"
                else:
                    return self.totalB

            elif (d2 == 50 or d2 == 25):
                self.totalB = total2 - d2
                if self.totalB < 0:
                    self.totalB = total2 + d2
                    return "You can not score more than required!"
                else:
                    return self.totalB
            else:
                return 'Wrong number you have selected. Please try again'

        else:
            return 'Wrong number you have selected. Please try again'
