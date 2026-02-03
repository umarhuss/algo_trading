from indicators import sma, daily_returns


class SMA_Crossover:
    def __init__(self, short_window = 20, long_window = 50):
        self.short_window = short_window
        self.long_window = long_window

    def positions(self, prices):
        n = len(prices)
        # call the sma function for the short position
        short_sma = sma(prices, self.short_window)
        long_sma = sma(prices,self.long_window)

        # Initialise positions list to len(prices)
        positions = [0]*n

        # return (f"this is short: {short_sma}\nthis is long:{long_sma}")

        # Compare the two lists at each corresponding index starting from long window as this is the first time there is
        # a viable comparison
        for i in range(self.long_window-1, n):
            # If short[i] > long[i] position = 1 else position = 0
            short = short_sma[i]
            long = long_sma[i]

            if short is None or long is None:
                positions[i] = 0
            elif short > long:
                positions[i] = 1
            else:
                positions[i] = 0

        return positions

    


prices = [200, 199, 198, 197, 196, 195, 194, 193, 192, 191,
 190, 189, 188, 187, 186, 185, 184, 183, 182, 181,
 180, 179, 178, 177, 176, 175, 174, 173, 172, 171,
 171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
 191, 192, 193, 194, 195, 196, 197, 198, 199, 200]

test = SMA_Crossover()
print(test.positions(prices))




