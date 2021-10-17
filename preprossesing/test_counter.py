number_counter = 0

def every_ten():
    global number_counter
    if number_counter == 10:
        print ("Done")
        number_counter = 0
    else:
        number_counter += 1

every_ten()