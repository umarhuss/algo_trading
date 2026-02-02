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
