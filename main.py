import numpy as np
import copy

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
    x = sheet[-1]["m"]
    y = sheet[-1]["n"]

    for node in sheet:
        if node.get("m") == position[0] and node.get("n") == position[1]:
            return node
        elif position[1] > y and position[0] <= x and position[0] >= 0:
            return findUnitCellByMN(sheet, position[0], 0)
        elif position[1] < 0 and position[0] <= x and position[0] >= 0:
            return findUnitCellByMN(sheet, position[0], y)
        elif position[0] > x and position[1] <= y and position[1] >= 0:
            return findUnitCellByMN(sheet, 0, position[1])
        elif position[0] < 0 and position[1] <= y and position[1] >= 0:
            return findUnitCellByMN(sheet, x, position[1])
        elif position[1] > y and position[0] > x:
            return findUnitCellByMN(sheet, 0, 0)
        elif position[1] < 0 and position[0] > x:
            return findUnitCellByMN(sheet, 0, y)
        elif position[0] < 0 and position[1] > y:
            return findUnitCellByMN(sheet, x, 0)
        elif position[0] < 0 and position[1] < 0:
            return findUnitCellByMN(sheet, x, y)


    # return {"atoms": [{"id_global": None}, {"id_global": None}, {"id_global": None}, {"id_global": None}, {"id_global": None}, {"id_global": None}]} 

def findUnitCellByMN(dictionary_list, m_value, n_value):
    for dictionary in dictionary_list:
        if dictionary.get("m") == m_value and dictionary.get("n") == n_value:
            return dictionary
    return None

def calcStrutEqlValue (node1, node2, cell, sheet):
    """
    This function calculates equal length of struts.
    """
    if cell["m"] == sheet[-1]["m"] and node1["coordinates"][0] < 1:
        return np.sqrt(((node1["coordinates"][0]+sheet[-1]["m"]+1) - node2["coordinates"][0])**2 + (node1["coordinates"][1] - node2["coordinates"][1])**2 + (node1["coordinates"][2] - node2["coordinates"][2])**2)
    elif cell["m"] == 0 and node1["coordinates"][0] > 2:
        return np.sqrt((node1["coordinates"][0]+1-sheet[-1]["m"] - node2["coordinates"][0])**2 + (node1["coordinates"][1] - node2["coordinates"][1])**2 + (node1["coordinates"][2] - node2["coordinates"][2])**2) 
    
    return round(np.sqrt((node1["coordinates"][0] - node2["coordinates"][0])**2 + (node1["coordinates"][1] - node2["coordinates"][1])**2 + (node1["coordinates"][2] - node2["coordinates"][2])**2), 10)

def calculateStruts (sheet):
    """
    This function calculates struts based on given sheet.
    """
    struts = []

    for cell in sheet:
        i = 1
        struts.extend(({
            "strut_id": i,
            "eql_length": calcStrutEqlValue(cell["atoms"][0], cell["atoms"][2], cell, sheet),
            "nodes_connected": [cell["atoms"][0]["id_global"], cell["atoms"][2]["id_global"]]
        },
        {
            "strut_id": i+1,
            "eql_length": calcStrutEqlValue(findAtoms(sheet, cell, [1,1])["atoms"][0], cell["atoms"][3], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [1,1])["atoms"][0]["id_global"], cell["atoms"][3]["id_global"]]
        },
        {
            "strut_id": i+2,
            "eql_length": calcStrutEqlValue(findAtoms(sheet, cell, [0,1])["atoms"][0], cell["atoms"][4], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [0,1])["atoms"][0]["id_global"], cell["atoms"][4]["id_global"]]
        },
        {
            "strut_id": i+3,
            "eql_length": calcStrutEqlValue(findAtoms(sheet, cell, [1,0])["atoms"][0], cell["atoms"][5], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [1,0])["atoms"][0]["id_global"], cell["atoms"][5]["id_global"]]
        },
        {
            "strut_id": i+4,
            "eql_length": calcStrutEqlValue(cell["atoms"][1], cell["atoms"][2], cell, sheet),
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][2]["id_global"]]
        },
        {
            "strut_id": i+5,
            "eql_length": calcStrutEqlValue(cell["atoms"][1], cell["atoms"][3], cell, sheet),
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][3]["id_global"]]
        },
        {
            "strut_id": i+6,
            "eql_length": calcStrutEqlValue(cell["atoms"][1], cell["atoms"][4], cell, sheet),
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][4]["id_global"]]
        },
        {
            "strut_id": i+7,
            "eql_length": calcStrutEqlValue(cell["atoms"][1], cell["atoms"][5], cell, sheet),
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][5]["id_global"]]
        },
        {
            "strut_id": i+8,
            "eql_length": calcStrutEqlValue(cell["atoms"][2], findAtoms(sheet, cell, [0,-1])["atoms"][3], cell, sheet),
            "nodes_connected": [cell["atoms"][2]["id_global"], findAtoms(sheet, cell, [0,-1])["atoms"][3]["id_global"]]
        },
        {
            "strut_id": i+9,
            "eql_length": calcStrutEqlValue(findAtoms(sheet, cell, [1,0])["atoms"][4], cell["atoms"][5], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [1,0])["atoms"][4]["id_global"], cell["atoms"][5]["id_global"]]
        }
        ))
        i += 1

    return struts

def calcAngleEqlValue(j, i, k, cell, sheet):

    if j["id_global"] == None or i["id_global"] == None or k["id_global"] == None:
        return None
    
    if cell["m"] == sheet[-1]["m"] or cell["m"] == 0:
        return None
    
    a = np.array(j["coordinates"])
    b = np.array(i["coordinates"])
    c = np.array(k["coordinates"])

    ba = a -b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return round(np.rad2deg(angle), 10)

def calcAngles(sheet):
    """
    This function calculates angles based on given sheet.
    """
    angles = []
    
    for cell in sheet:
        i = 1
        angles.extend(({
            "angle_id": i,
            "eql_value": calcAngleEqlValue(cell["atoms"][2], cell["atoms"][0], findAtoms(sheet, cell, [0,-1])["atoms"][4], cell, sheet),
            "nodes_connected": [cell["atoms"][2]["id_global"], cell["atoms"][0]["id_global"], findAtoms(sheet, cell, [0,-1])["atoms"][4]["id_global"]]
        },
        {
            "angle_id": i+1,
            "eql_value": calcAngleEqlValue(cell["atoms"][2], cell["atoms"][0], findAtoms(sheet, cell, [-1,0])["atoms"][5], cell, sheet),
            "nodes_connected": [cell["atoms"][2]["id_global"], cell["atoms"][0]["id_global"], findAtoms(sheet, cell, [-1,0])["atoms"][5]["id_global"]]
        },
        {
            "angle_id": i+2,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [-1,-1])["atoms"][3], cell["atoms"][0], findAtoms(sheet, cell, [0,-1])["atoms"][4], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [-1,-1])["atoms"][3]["id_global"], cell["atoms"][0]["id_global"], findAtoms(sheet, cell, [0,-1])["atoms"][4]["id_global"]]
        },
        {
            "angle_id": i+3,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [-1,-1])["atoms"][3], cell["atoms"][0], findAtoms(sheet, cell, [-1,0])["atoms"][5], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [-1,-1])["atoms"][3]["id_global"], cell["atoms"][0]["id_global"], findAtoms(sheet, cell, [-1,0])["atoms"][5]["id_global"]]
        },
        {
            "angle_id": i+4,
            "eql_value": calcAngleEqlValue(cell["atoms"][2], cell["atoms"][1], cell["atoms"][4], cell, sheet),
            "nodes_connected": [cell["atoms"][2]["id_global"], cell["atoms"][1]["id_global"], cell["atoms"][4]["id_global"]]
        },
        {
            "angle_id": i+5,
            "eql_value": calcAngleEqlValue(cell["atoms"][2], cell["atoms"][1], cell["atoms"][5], cell, sheet),
            "nodes_connected": [cell["atoms"][2]["id_global"], cell["atoms"][1]["id_global"], cell["atoms"][5]["id_global"]]
        },
        {
            "angle_id": i+6,
            "eql_value": calcAngleEqlValue(cell["atoms"][3], cell["atoms"][1], cell["atoms"][5], cell, sheet),
            "nodes_connected": [cell["atoms"][3]["id_global"], cell["atoms"][1]["id_global"], cell["atoms"][5]["id_global"]]
        },
        {
            "angle_id": i+7,
            "eql_value": calcAngleEqlValue(cell["atoms"][3], cell["atoms"][1], cell["atoms"][4], cell, sheet),
            "nodes_connected": [cell["atoms"][3]["id_global"], cell["atoms"][1]["id_global"], cell["atoms"][4]["id_global"]]
        },
        {
            "angle_id": i+8,
            "eql_value": calcAngleEqlValue(cell["atoms"][0], cell["atoms"][2], cell["atoms"][1], cell, sheet),
            "nodes_connected": [cell["atoms"][0]["id_global"], cell["atoms"][2]["id_global"], cell["atoms"][1]["id_global"]]
        },
        {
            "angle_id": i+9,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [1,1])["atoms"][0], cell["atoms"][3], cell["atoms"][1], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [1,1])["atoms"][0]["id_global"], cell["atoms"][3]["id_global"], cell["atoms"][1]["id_global"]]
        },
        {
            "angle_id": i+10,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [0,1])["atoms"][0], cell["atoms"][4], cell["atoms"][1], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [0,1])["atoms"][0]["id_global"], cell["atoms"][4]["id_global"], cell["atoms"][1]["id_global"]]
        },
        {
            "angle_id": i+11,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [1,0])["atoms"][0], cell["atoms"][5], cell["atoms"][1], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [1,0])["atoms"][0]["id_global"], cell["atoms"][5]["id_global"], cell["atoms"][1]["id_global"]]
        },
        {
            "angle_id": i+12,
            "eql_value": calcAngleEqlValue(cell["atoms"][0], cell["atoms"][2], findAtoms(sheet, cell, [0,-1])["atoms"][3], cell, sheet),
            "nodes_connected": [cell["atoms"][0]["id_global"], cell["atoms"][2]["id_global"], findAtoms(sheet, cell, [0,-1])["atoms"][3]["id_global"]]
        },
        {
            "angle_id": i+13,
            "eql_value": calcAngleEqlValue(cell["atoms"][1], cell["atoms"][2], findAtoms(sheet, cell, [0,-1])["atoms"][3], cell, sheet),
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][2]["id_global"], findAtoms(sheet, cell, [0,-1])["atoms"][3]["id_global"]]
        },
        {
            "angle_id": i+14,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [1, 1])["atoms"][0], cell["atoms"][3], findAtoms(sheet, cell, [0, 1])["atoms"][2], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [1, 1])["atoms"][0]["id_global"], cell["atoms"][3]["id_global"], findAtoms(sheet, cell, [0,1])["atoms"][2]["id_global"]]
        },
        {
            "angle_id": i+15,
            "eql_value": calcAngleEqlValue(cell["atoms"][1], cell["atoms"][3], findAtoms(sheet, cell, [0, 1])["atoms"][2], cell, sheet),
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][3]["id_global"], findAtoms(sheet, cell, [0,1])["atoms"][2]["id_global"]]
        },
        {
            "angle_id": i+16,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [0, 1])["atoms"][0], cell["atoms"][4], findAtoms(sheet, cell, [-1, 0])["atoms"][5], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [0, 1])["atoms"][0]["id_global"], cell["atoms"][4]["id_global"], findAtoms(sheet, cell, [-1, 0])["atoms"][5]["id_global"]]
        },
        {
            "angle_id": i+17,
            "eql_value": calcAngleEqlValue(cell["atoms"][1], cell["atoms"][4], findAtoms(sheet, cell, [-1, 0])["atoms"][5], cell, sheet),
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][4]["id_global"], findAtoms(sheet, cell, [-1, 0])["atoms"][5]["id_global"]]
        },
         {
            "angle_id": i+18,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [1, 0])["atoms"][0], cell["atoms"][5], findAtoms(sheet, cell, [1, 0])["atoms"][4], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [1, 0])["atoms"][0]["id_global"], cell["atoms"][5]["id_global"], findAtoms(sheet, cell, [1, 0])["atoms"][4]["id_global"]]
        },
        {
            "angle_id": i+19,
            "eql_value": calcAngleEqlValue(cell["atoms"][1], cell["atoms"][5], findAtoms(sheet, cell, [1, 0])["atoms"][4], cell, sheet),
            "nodes_connected": [cell["atoms"][1]["id_global"], cell["atoms"][5]["id_global"], findAtoms(sheet, cell, [1, 0])["atoms"][4]["id_global"]]
        },
        {
            "angle_id": i+20,
            "eql_value": calcAngleEqlValue(cell["atoms"][2], cell["atoms"][0], findAtoms(sheet, cell, [-1, -1])["atoms"][3], cell, sheet),
            "nodes_connected": [cell["atoms"][2]["id_global"], cell["atoms"][0]["id_global"], findAtoms(sheet, cell, [-1, -1])["atoms"][3]["id_global"]]
        },
        {
            "angle_id": i+21,
            "eql_value": calcAngleEqlValue(findAtoms(sheet, cell, [0, -1])["atoms"][4], cell["atoms"][0], findAtoms(sheet, cell, [-1, 0])["atoms"][5], cell, sheet),
            "nodes_connected": [findAtoms(sheet, cell, [0, -1])["atoms"][4]["id_global"], cell["atoms"][0]["id_global"], findAtoms(sheet, cell, [-1, 0])["atoms"][5]["id_global"]]
        },
        {
            "angle_id": i+22,
            "eql_value": calcAngleEqlValue(cell["atoms"][2], cell["atoms"][1], cell["atoms"][3], cell, sheet),
            "nodes_connected": [cell["atoms"][2]["id_global"], cell["atoms"][1]["id_global"], cell["atoms"][3]["id_global"]]
        },
        {
            "angle_id": i+23,
            "eql_value": calcAngleEqlValue(cell["atoms"][4], cell["atoms"][1], cell["atoms"][5], cell, sheet),
            "nodes_connected": [cell["atoms"][4]["id_global"], cell["atoms"][1]["id_global"], cell["atoms"][5]["id_global"]]
        },
        ))

    periodicAdjusment(angles)

    return angles     

def periodicAdjusment(angles):
    for angle in angles:
        if angle["eql_value"] == None:
            for i in range(24):
                print(angle["angle_id"], angles[i+24]["angle_id"])
                if angle["angle_id"] == angles[i+24]["angle_id"]:
                    angle["eql_value"] = angles[i+24]["eql_value"]

def transformIntoTube (sheet, y):
    """
    This function takes sheet and transforms it into tube.
    """
    n = len(sheet)
    tube = copy.deepcopy(sheet)
    for i in range(n):
        for j in range(6): 
            tube[i]["atoms"][j]["coordinates"][0] = sheet[i]["atoms"][j]["coordinates"][0]
            tube[i]["atoms"][j]["coordinates"][1] = ((y)/(2*np.pi) + sheet[i]["atoms"][j]["coordinates"][2]) * np.sin((2*np.pi*sheet[i]["atoms"][j]["coordinates"][1])/(y))
            tube[i]["atoms"][j]["coordinates"][2] = ((y)/(2*np.pi) + sheet[i]["atoms"][j]["coordinates"][2]) * np.cos((2*np.pi*sheet[i]["atoms"][j]["coordinates"][1])/(y))
    return tube 


def main(d22, h, x, y, isPeriodic):
    elementarCell = calcElementarCell(d22, h)
    sheet = sheetGenerator(elementarCell, x, y)
    tube = transformIntoTube(sheet, y)
    struts = calculateStruts(tube)
    angles = calcAngles(tube)

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

    with open("angles.xyz", "w") as f:
        f.write(str(len(angles)) + "\n")
        f.write("Angles\n")
        for angle in angles:
            f.write(str(angle["angle_id"]) + " " + str(angle["eql_value"]) + " " + str(angle["nodes_connected"]) + "\n")

    with open("tube.xyz", "w") as f:
        f.write(str(len(tube)*6) + "\n")
        f.write("Rurka\n")
        for coord in tube:
            for i in range(6):
                f.write("C " + str(coord["atoms"][i]["coordinates"][0]) + " " + str(coord["atoms"][i]["coordinates"][1]) + " " + str(coord["atoms"][i]["coordinates"][2]) + "\n")       

    with open("tube.data", "w") as f:
        f.write("pentagraphene\n")
        f.write(str(len(tube)*6) + "atoms\n")
        f.write(str(len(tube)*6) + "bonds\n")
        for coord in tube:
            for i in range(6):
                f.write("C " + str(coord["atoms"][i]["coordinates"][0]) + " " + str(coord["atoms"][i]["coordinates"][1]) + " " + str(coord["atoms"][i]["coordinates"][2]) + "\n")