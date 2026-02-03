def sma(prices, time):
    # set up window and pointers
    left = 0
    window = sum(prices[:time])
    len_of_list = len(prices)

    # Edge cases
    if time > len(prices):
        return [None] * len(prices)

    # initialise sma array
    sma = [None] * (time - 1)
    sma.append(window / time)

    # Loop through rest of the elements
    for right in range(time, len_of_list):
        # Adjust the current window
        current_window = window - prices[left] + prices[right]
        # update the window for the next iteration
        window = current_window
        sma.append(current_window / time)
        # Update the left pointer so it moves along with the loop
        left += 1

    return sma

def daily_returns(prices):
    length = len(prices)
    returns = [0]* length

    for i in range(1,length):
        current_rt = (prices[i] - prices[i-1]) / prices[i-1]
        returns[i] = current_rt

    return returns


