import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import collections



# 0 Regeln und Werte festlegen
# 1a Abspeichern von Werten nach Wurf => Werte berechnen anhand von Regeln
# 1b Abspeichern von Werten während Wurfen
# 2 Würfler
# 3 Wahrscheinlichkeiten Berechnungsfunktion
# => ALle Option, 3 Würfe, 
# 4 Berechner-Vorhersager
# 4 
# Würfel Event: [], [], [], []
# Würfel FiX, Würfel Aktueller Wurf, Tries
    # self.zahlenNamen = ["einser","zweier", "dreier", "vierer", "funfer", "sechser"]
    # self.paarNamen = ["1paar","2paar"]
    # self.gleicheNamen = ["3gleiche","4gleiche"]
    # self.straßenNamen = ["klStr","gStr"]
    # self.fhNamen = ["FullHouse"]
    # self.kniffelNamen = ["kniffel"]

    # self.namen = (self.zahlenNamen + self.paarNamen +
    #               self.gleicheNamen + self.straßenNamen +
    #               self.fhNamen + self.kniffelNamen)
class Evaluator:
    # Allgemeine Deklaration, unabhängig ovn spezifischer Klasse
    zahlenNamen = ["einser","zweier", "dreier", "vierer", "funfer", "sechser"]
    paarNamen = ["1paar","2paar"]
    gleicheNamen = ["3gleiche","4gleiche"]
    straßenNamen = ["klStr","gStr"]
    fhNamen = ["FullHouse"]
    kniffelNamen = ["kniffel"]

    straßenVals = [25,35]
    fhVal = 25
    kniffelVal = 50
    thresh = np.sum(np.arange(1,7))*3

    namen = (zahlenNamen + paarNamen +
             gleicheNamen + straßenNamen +
             fhNamen + kniffelNamen)
    vals = np.arange(1,7)


    def __init__(self):
        self.scoresheet = {} 
        # self.scoresheet.keys = self.namen
        # AttributeError: 'dict' object attribute 'keys' is read-only

    def checker(self, wurf, call):  
        """ If Call in einzelne Funktionen aufteilen für Übersichtlichkeit""" 
        wurf = np.array(wurf)
        res = 0
        if call in self.zahlenNamen:
            idx = self.zahlenNamen.index(call)
            res = wurf[idx]*self.vals[idx]
        elif call in self.paarNamen:
            # Entscheidet ob 1paar or 2paar
            paarZahl = self.paarNamen.index(call) + 1
            # Anzahl Paare im Array: vals[vals>=2] returns all values larger or equal to two
            countPairs = len(vals[vals>=2])
            if countPairs > paarZahl:
                res = wurf*self.vals
                print("Did not fulfill condition")
        elif call in self.gleicheNamen:
            gleiche_Zahl = gleicheNamen.index(call) + 3
            # Anzahl Paare im Array: vals[vals>=2] returns all values larger or equal to two
            if np.any(wurf>gleiche_Zahl):
                res = wurf*self.vals
                print("Did not fulfill condition")
        elif call in self.straßenNamen:
            idx = self.straßenNamen.index(call)
            straßenMin = idx + 4
            count = 0
            reward = False
            for anzahl in wurf:
                if anzahl:
                    count += 1
                else: 
                    count = 0
                if count >= straßenMin:
                    reward = True
                    break
            if reward:
                res = self.straßenVals[idx]
        elif call in self.fhNamen:
            if 2 in wurf and 3 in wurf:
                res = self.fhVal
        elif call in self.kniffelNamen:
            if 5 in wurf:
                res = self.kniffelVal

        self.scoresheet[call] = res




    def interaction(self,zahlen, call): # 3 Würfe, sich merkt was weggelegt wird
        zahlen = np.array(zahlen)
        wurf = np.zeros(6)
        if not call in self.namen:
            print("Invalid Name")
            return 
        elif call in self.scoresheet:
            print("Already played this round")
            return 
        if (not (1<=zahlen).all or not (zahlen<=6).all
        or  len(zahlen)!= 5):
            print("Invalid Values or length")
            return 
        for z in zahlen:
            wurf[z-1] += 1
        self.checker(wurf, call)

    
    def calcPoints(self, verbose=0):
        zahlenSum = 0
        for z in {key: self.scoresheet.get(key, 0)
                 for key in self.zahlenNamen}.values():
            zahlenSum += z
                
        score = 0
        for key,val in self.scoresheet.items():
            if verbose:
                print(key+": %d"%int(val))
            score += val
        if zahlenSum > self.thresh:
            score += bonus
        print(zahlenSum)
        print(score)

    def reset(self): # setzt score sheet zurück
        self.scoresheet = {} 

# Class Würfler: #
#     for i in range(3):
#         self.würfel
#         self.decide
#     Evaluator.interaction(wurf,call="einer")

    # [1,2,3,4,5,6]
    # [2,0,0,3,0,0]
    # Würfler Sagt: 
    # [2,3,4,4,3]
    # Wir sagen:
    # [2,3,4]
    # Würfel 2x:

#
# collections.Counter(np.random.randint(1,7,n))

# result = []
# for i in range(0,100):
#     first_throw = np.random.randint(1,7,5)
#     nums = len(first_throw[first_throw == 3])
#     if (5-nums) > 0:
#         n = 5-nums
#         next_throw = np.random.randint(1,7,n)
#         nums += len(next_throw[next_throw == 3])

#         if (5-nums) > 0:
#             n = 5-nums
#             next_throw = np.random.randint(1,7,n)
#             nums += len(next_throw[next_throw == 3])
            
#     result.append(nums)
# result = np.array(result)
    
# dists = []
# for i in range(0,6):
#     dists.append(len(result[result==i]))


# def countvals(arr_stuff):
#     unique, counts = numpy.unique(arr_stuff, return_counts=True)
#     return(dict(zip(unique, counts))

class Würfler:
    def __init__(self):
        self.throwcount = 3

    def throw(self, n_dice):
        if self.throwcount > 0 and n_dice > 0:
            self.throw_res = np.random.randint(1,7, n_dice)
            self.throwcount -= 1

            return self.throw_res
        else:
            print("Keine Würfe übrig!")

    def get_vals(self,vals):
        self.n_dice -= len(vals)

        return vals, self.n_dice

class expected_values:
    #für die werte oben (einser, zweier usw) nach erstem wurd
    def calc_numbers_first_throw:
        total_exv = []
        for i in categories:
            for n in rows:
                if n < 5:
                    add = []
                    for b in range(0, 5 - n + 1):
                        in_val = ((1 / 6) ** b) * ((5 / 6) ** (5 - n - b))
                        if (5 - (n + b)) > 0:
                            for c in range(0, 5 - (n + b) + 1):
                                add.append(in_val * ((1 / 6) ** (c)) * (5 / 6) ** (5 - (n + b + c)) * (b + c) * i)
                        else:
                            add.append(in_val * b * i)
                    total_exv.append(sum(add) + n * i)
                else:
                    total_exv.append(n * i)

        total_exv = np.array(total_exv)
        total_exv = total_exv.reshape((6, 6))
        exv_table = pd.DataFrame(total_exv.T, index=rows, columns=categories)
        #rows --> zahlen nach dem ersten wurf, column einser zweier usw, data --> expected value

#expected value multiplyer für 0 würfe oben 2.1062350999999997
#prob gr. straße 0.2491861 -- exp value 9.967444
#prob kl. straße 0.545356 -- exp value 16.36068


def main():
    test = Evaluator()
    probeWurf = [1,2,3,3,4]
    probeAnsage = "klStr"
    test.interaction(probeWurf, probeAnsage)
    probeWurf = [1,2,3,4,5]
    probeAnsage = "gStr"
    test.interaction(probeWurf, probeAnsage)
    probeWurf = [1,1,1,4,4]
    probeAnsage = "FullHouse"
    test.interaction(probeWurf, probeAnsage)
    test.calcPoints(verbose=True)
    test2 = Würfler()
    print(test2.throw(5))
    print(test2.throw(5))
    print(test2.throw(5))
    test2.throw(5)
if __name__ == "__main__":
    main()
    pass