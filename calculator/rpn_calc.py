# A very simple calculator.
# Note that anything after the pound/number/sharp/hash/octothorpe symbol is a comment and is ignored by the interpreter.

# Set up variables
x = 0.0        # The stack variables: x is the last value entered, or the result.
y = 0.0        #                      y is where x gets pushed.
looping = True # looping is a Boolean variable, it can hold either True or False.

# Print out a message and instructions.
print('Simple RPN Calculator')
print('Enter numbers or commands at the prompt.')
print('Since it is an RPN calculator, the order of entering is: number, number, operator.')
print('Enter "+" to add, "q" to quit.')
print('Example: 4 <Enter> 5 <Enter> + <Enter> will result in 20')

# The main loop
while looping:
    print('y: ', y)
    print('x: ', x)
    user_input = input('>  ') # Get a string of characters from the user and assign it to the variable user_input.

    # Test the string
    if user_input == 'q':
        looping = False # This is how we quit; the next time we hit the while above we will exit the loop.
    elif user_input == '+':
        x = x + y
        y = 0.0
    else:
        # Else occurs if the user did not enter either '+' or 'q', so it must be a number.
        temp = float(user_input) # Convert the input to a floating-point number.
        y = x                    # Shift the value that was in x to y (deleting what was in y).
        x = temp                 # The new value of x is what was entered.

print('Calculator end')
