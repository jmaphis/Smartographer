# array-int-conversion, by James Maphis - a simple module 
# for converting 2 dimentional arrays of 1s and 0s into 
# integers and back

NEW_LINE = 2

def array_to_int(array: list):
    array_int = 0
    for _, sub_array in enumerate(array):
        # move previous digits over by 1 digit
        array_int *= 10
        # insert a '2' to represent a new line
        array_int += NEW_LINE
        for _, binary_digit in enumerate(sub_array):
            # move previous digits over by 1 digit
            array_int *= 10
            # insert the current digit
            array_int += binary_digit
    return array_int

def int_to_array(array_num: int):
    int_array = []
    current_digit = None
    while array_num != 0:
        sub_array = []
        while True:
            # get the last digit of the number
            current_digit = array_num % 10
            if current_digit == NEW_LINE:
                # 2 represents the end of the current sub array
                break
            else:
                sub_array.insert(0, current_digit)
            array_num //= 10
        # insert the sub array, then remove the 2 to 
        # prepare for the next sub array
        int_array.insert(0, sub_array)
        array_num //=10
    return int_array


if __name__ == '__main__':

    test_array = [[1, 0, 1], [0, 1, 0], [1, 1, 0]]
    print('starting array:')
    print(test_array)
    array_num = array_to_int(test_array)
    print('converting array to int:')
    print(array_num)
    print('converting int to array')
    num_array = int_to_array(array_num)
    print(num_array)