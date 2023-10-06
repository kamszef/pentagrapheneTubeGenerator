import numpy as np

def calcElementarCell(d22, h):
    """
    This function calculates pentagraphene elementar cell.
    """
    x = 1/2 - np.sqrt(2)/4 * d22
    y = np.sqrt(2)/4 * d22
    z = h

    elementarCell = [
        [0, 0, 0, 1],
        [1/2, 1/2, 0, 2],
        [x, y, z, 3],
        [1-x, 1-y, z, 4],
        [y, 1-x, -z, 5],
        [1-y, x, -z, 6]
    ]

    return elementarCell

def sheetGenerator(elementarCell, x, y):
    """
    This function generates pentagraphene sheet.
    """
    sheet = []
    for node in elementarCell:
        for i in range(x):
            for j in range(y):
                xCoordinate = node[0] + i
                yCoordinate = node[1] + j
                zCoordinate = node[2]
                sheet.append([xCoordinate, yCoordinate, zCoordinate])

    return sheet

isPentagraphene = input("Is pentagraphene? (y/n): ")

if isPentagraphene == "y":
    d22 = 0.3677
    h = 0.1648
else:   
    d22 = float(input("Enter d22: "))
    h = float(input("Enter h: "))
    
x = int(input("Enter repetitions on x axis: "))
y = int(input("Enter repetitions on y axis: "))

elementarCell = calcElementarCell(d22, h)
sheet = sheetGenerator(elementarCell, x, y)

with open("pentagraphene.xyz", "w") as f:
    f.write(str(len(sheet)) + "\n")
    f.write("Sheet\n")
    for node in sheet:
        f.write("C " + str(node[0]) + " " + str(node[1]) + " " + str(node[2]) + "\n")
