import random as rd
class Calculation:
    def __init__(self):
        self.totalA = 0
        self.totalB = 0

        # uncomment this if u use recommend functions
        #self.str1 = None
        #self.str2 = None
        #self.str3 = None

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

"""
    def recommend_func(self, score):
        if score > 60:
            a = rd.randint(1, 61)
            b = rd.randint(1, 61)
            c = rd.randint(1, 61)
        else:
            a = rd.randint(1, score + 1)
            b = rd.randint(1, score + 1)
            c = rd.randint(1, score + 1)

        def randomized_number(a, b, c):

            if (a <= 40 and a % 2 == 0):
                self.str1 = f'{int(a / 2)}D'
            elif (a <= 60 and a % 3 == 0):
                self.str1 = f'{int(a / 3)}T'
            elif a == 50:
                self.str1 = 'Bull'
            else:
                self.str1 = str(a)

            if (b <= 40 and b % 2 == 0):
                self.str2 = f'{int(b / 2)}D'
            elif (b <= 60 and b % 3 == 0):
                self.str2 = f'{int(b / 3)}T'
            elif b == 50:
                self.str2 = 'Bull'
            else:
                self.str2 = str(b)

            if (c <= 40 and c % 2 == 0):
                self.str3 = f'{int(c / 2)}D'
            elif (c <= 60 and c % 3 == 0):
                self.str3 = f'{int(c / 3)}T'
            elif c == 50:
                self.str3 = 'Bull'
            else:
                self.str3 = str(c)

        while True:
            if ((a + b + c == score) and (((((a > 40 and a <= 60) and a % 3 == 0) or a == 50) and (
                    ((b > 40 and b <= 60) and b % 3 == 0) or b == 50) and (
                                                   ((c > 40 and c <= 60) and c % 3 == 0) or c == 50)) or ((
                                                                                                                  a == 1 or a == 5 or a == 7 or a == 11 or a == 13 or a == 17 or a == 19 or a == 25 or (
                                                                                                                  (
                                                                                                                          a > 0 and a <= 40) and (
                                                                                                                          a % 2 == 0 or a % 3 == 0))) and (
                                                                                                                  b == 1 or b == 5 or b == 7 or b == 11 or b == 13 or b == 17 or b == 19 or b == 25 or (
                                                                                                                  (
                                                                                                                          b > 0 and b <= 40) and (
                                                                                                                          b % 2 == 0 or b % 3 == 0))) and (
                                                                                                                  c == 1 or c == 5 or c == 7 or c == 11 or c == 13 or c == 17 or c == 19 or c == 25 or (
                                                                                                                  (
                                                                                                                          c > 0 and c <= 40) and (
                                                                                                                          c % 2 == 0 or c % 3 == 0))))) and (
                    a <= 60 and b <= 60 and c <= 60)):
                randomized_number(a, b, c)
                return self.str1, self.str2, self.str3
            else:
                if score > 60:
                    a = rd.randint(1, 61)
                    b = rd.randint(1, 61)
                    c = rd.randint(1, 61)
                else:
                    a = rd.randint(1, score + 1)
                    b = rd.randint(1, score + 1)
                    c = rd.randint(1, score + 1)

    def recommend_func2(self, score):
        if score > 60:
            a = rd.randint(1, 61)
            b = rd.randint(1, 61)
        else:
            a = rd.randint(1, score + 1)
            b = rd.randint(1, score + 1)

        def randomized_number(a, b):

            if (a <= 40 and a % 2 == 0):
                self.str1 = f'{int(a / 2)}D'
            elif (a <= 60 and a % 3 == 0):
                self.str1 = f'{int(a / 3)}T'
            elif a == 50:
                self.str1 = 'Bull'
            else:
                self.str1 = str(a)

            if (b <= 40 and b % 2 == 0):
                self.str2 = f'{int(b / 2)}D'
            elif (b <= 60 and b % 3 == 0):
                self.str2 = f'{int(b / 3)}T'
            elif b == 50:
                self.str2 = 'Bull'
            else:
                self.str2 = str(b)

        while True:
            if ((a + b == score) and (((((a > 40 and a <= 60) and a % 3 == 0) or a == 50) and (
                    ((b > 40 and b <= 60) and b % 3 == 0) or b == 50)) or ((
                                                                                   a == 1 or a == 5 or a == 7 or a == 11 or a == 13 or a == 17 or a == 19 or a == 25 or (
                                                                                   (a > 0 and a <= 40) and (
                                                                                   a % 2 == 0 or a % 3 == 0))) and (
                                                                                   b == 1 or b == 5 or b == 7 or b == 11 or b == 13 or b == 17 or b == 19 or b == 25 or (
                                                                                   (b > 0 and b <= 40) and (
                                                                                   b % 2 == 0 or b % 3 == 0))))) and (
                    a <= 60 and b <= 60)):
                randomized_number(a, b)
                return self.str1, self.str2, self.str3
            else:
                if score > 60:
                    a = rd.randint(1, 61)
                    b = rd.randint(1, 61)
                else:
                    a = rd.randint(1, score + 1)
                    b = rd.randint(1, score + 1)

    def recommend_func3(self, score):
        if score <= 40 and score % 2 == 0:
            return f'{int(score / 2)}D', None, None
        elif score <= 60 and score % 3 == 0:
            return f'{int(score / 3)}T', None, None
        elif score <= 20:
            return str(score), None, None
        elif score == 50:
            return 'Bull', None, None
        elif score == 25:
            return str(score), None, None 
"""