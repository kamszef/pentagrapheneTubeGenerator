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
    unitCellId = 1

    for i in range(y):
            for j in range(x):
                atoms = []

                for k in range(6):
                    atoms.append({
                        "id_global": elementarCell[k][3] + (unitCellId - 1) * 6,
                        "id_local": elementarCell[k][3],
                        "coordinates": [elementarCell[k][0] + 1 * j , elementarCell[k][1] + 1 * i, elementarCell[k][2]]
                    })

                sheet.append({
                     "id_cell": unitCellId,
                      "m": j,
                      "n": i,
                      "atoms": atoms
                })

                unitCellId += 1

    return sheet

def findAtoms(sheet, unitCell, vector):
    """
    This function finds certain node, based on given requirments.
    """
    m = unitCell["m"]
    n = unitCell["n"]
    position = [vector[0] + m, vector[1] + n]

    for node in sheet:
        if node.get("m") == position[0] and node.get("n") == position[1]:
            return node
    return unitCell 

def calculateStruts (sheet, d22, h):
    """
    This function calculates struts based on given sheet.
    """
    d12 = np.sqrt(h**2 + (d22 * (d22 - np.sqrt(2)) + 1)/4)
    struts = []

    for cell in sheet:
        i = 1
        struts.extend(({
            "strut_id": i,
            "eql_length": d12,
            "nodes_connected": [cell["atoms"][0]["id_global"], cell["atoms"][2]["id_global"]]
        },
        {
            "strut_id": i+1,
            "eql_length": d12,
            "nodes_connected": [findAtoms(sheet, cell, [1,1])["atoms"][0]["id_global"], cell["atoms"][3]["id_global"]]
        },
        {
            "strut_id": i+2,
            "eql_length": d12,
            "nodes_connected": [findAtoms(sheet, cell, [0,1])["atoms"][0]["id_global"], cell["atoms"][4]["id_global"]]
        },
        {
            "strut_id": i+3,
            "eql_length": d12,
            "nodes_connected": [findAtoms(sheet, cell, [1,0])["atoms"][0]["id_global"], cell["atoms"][5]["id_global"]]
        },
        {
            "strut_id": i+4,
            "eql_length": d12,
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][2]["id_global"]]
        },
        {
            "strut_id": i+5,
            "eql_length": d12,
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][3]["id_global"]]
        },
        {
            "strut_id": i+6,
            "eql_length": d12,
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][4]["id_global"]]
        },
        {
            "strut_id": i+7,
            "eql_length": d12,
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][5]["id_global"]]
        },
        {
            "strut_id": i+8,
            "eql_length": d22,
            "nodes_connected": [cell["atoms"][2]["id_global"], findAtoms(sheet, cell, [0,-1])["atoms"][3]["id_global"]]
        },
        {
            "strut_id": i+9,
            "eql_length": d22,
            "nodes_connected": [findAtoms(sheet, cell, [1,0])["atoms"][4]["id_global"], cell["atoms"][5]["id_global"]]
        }
        ))
        i += 1

    return struts

def main(d22, h, x, y, isPeriodic):
    elementarCell = calcElementarCell(d22, h)
    sheet = sheetGenerator(elementarCell, x, y)
    struts = calculateStruts(sheet, d22, h)

    with open("pentagraphene.xyz", "w") as f:
        f.write(str(len(sheet) * 6) + "\n")
        f.write("Sheet\n")
        for atom in sheet:
            for i in range(6):
                f.write("C " + str(atom["atoms"][i]["coordinates"][0]) + " " + str(atom["atoms"][i]["coordinates"][1]) + " " + str(atom["atoms"][i]["coordinates"][2]) + "\n")
        

    with open("struts.xyz", "w") as f:
        f.write(str(len(struts)) + "\n")
        f.write("Struts\n")
        for strut in struts:
            f.write(str(strut["strut_id"]) + " " + str(strut["eql_length"]) + " " + str(strut["nodes_connected"]) + "\n")

    