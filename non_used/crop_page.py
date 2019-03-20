def crop(page, x_lower_left, y_lower_left, x_upper_right, y_upper_right ):

        x= page.mediaBox.getUpperRight_x() - x_upper_right
        y= page.mediaBox.getUpperRight_y() - y_upper_right
        page.cropBox.lowerLeft = (x_lower_left, y_lower_left)
        page.cropBox.upperRight = (x, y)


