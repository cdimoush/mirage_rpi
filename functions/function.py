from kivy.core.window import Window


'''
    Function receives the number of columns and rows desired and returns variables to create a grid.
    When using the function ask for:

    Window Width(x), Window Height(y), Column Width(col_sp), Row Height(row_sp), List of Column X Coordinates(x_list),
    and List of Row Y Coordinates(y_list)
'''


def grid_function(cols, rows):

    x = Window.size[0]
    y = Window.size[1]
    col_sp = x/cols
    row_sp = y/rows
    x_list = []  # list of x coordinates
    y_list = []  # list of y coordinates
    for i in range(0, cols):
        x_list.append(i*col_sp)
    for i in range(0, rows):
        y_list.append(i*row_sp)

    return x, y, col_sp, row_sp, x_list, y_list



