from configuration import configJson


def calculate_jij(calculations, superCellNum, pair):
    label = configJson["spinCombinationLabels"]

    a = calculations[label[0] + "_" + str(superCellNum) + "_" + str(pair[0]) + "_" + str(pair[1])][
        "output_parameters"].dict.energy
    b = calculations[label[1] + "_" + str(superCellNum) + "_" + str(pair[0]) + "_" + str(pair[1])][
        "output_parameters"].dict.energy
    c = calculations[label[2] + "_" + str(superCellNum) + "_" + str(pair[0]) + "_" + str(pair[1])][
        "output_parameters"].dict.energy
    d = calculations[label[3] + "_" + str(superCellNum) + "_" + str(pair[0]) + "_" + str(pair[1])][
        "output_parameters"].dict.energy
    result = (a - b - c + d) / (4 * configJson["spinValue"] * configJson["spinValue"])
    return result
