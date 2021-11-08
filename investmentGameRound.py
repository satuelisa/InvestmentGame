INVESTOR = 0
TRUSTEE = 1
BOTH = 2

class Round:

    def __str__(self):
        return '[%.2f, %.2f]' % (self.investedPercentage, self.returnedPercentage)

    def __repr__(self):
        return '[%.2f, %.2f]' % (self.investedPercentage, self.returnedPercentage)

    def getValue(self, type, raw = False):
        if type == INVESTOR:
            if not raw:
                return self.investedPercentage
            else:
                return self.investedAmount
        elif type == TRUSTEE:
            if not raw:
                return self.returnedPercentage
            else:
                return self.returnedAmount
        else:
            return None

    def __init__(self, inv, tot, roi, gain):
        self.investedAmount = inv
        self.returnedAmount = roi
        if tot > 0.0:
            self.investedPercentage = inv / (1.0 * tot)
        else:
            self.investedPercentage = None
        if gain > 0.0:
            self.returnedPercentage = roi / (1.0 * gain)
        else:
            self.returnedPercentage = None
        return

