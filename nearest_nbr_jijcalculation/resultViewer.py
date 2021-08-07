def exchange_interaction(exchange_coupling_pk):
    from aiida.orm import load_node
    exchange_coupling_calc = load_node(exchange_coupling_pk)
    print(exchange_coupling_calc.outputs)
    finalResultDict = {}

    for E, V, units, label in exchange_coupling_calc.outputs.exchange_coupling.dict.exchange_coupling:

        print("Energy is :: ", E, "Volume is :: ", V, "Units is :: ", units, "label is :: ", label)
        labels = label.split("_")
        if labels[1] in finalResultDict:
            if labels[0] in finalResultDict[labels[1]]:
                finalResultDict[labels[1]][labels[0]].add(labels[2], E)
            else:
                temp = {
                    labels[2]: E
                }
                finalResultDict[labels[1]].add(labels[0], temp)
        else:
            temp = {
                labels[0]: {
                    labels[2]: E
                }
            }
            finalResultDict.add(labels[1], temp)

    for pair, value in finalResultDict.items():
        for superCellNum, spinValues in value.items():
            print(" JIJ value with pair :: " + pair + " and with super Cell number :: " + str(
                superCellNum) + "result :: ",
                  (spinValues['a'] - spinValues['b'] -
                   spinValues['c'] + spinValues['d']) / (4 * 1.5 * 1.5))


if __name__ == '__main__':
    exchange_interaction(10717)
