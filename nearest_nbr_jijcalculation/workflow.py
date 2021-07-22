# -*- coding: utf-8 -*-
"""Simple workflow example"""
from __future__ import absolute_import
from __future__ import print_function

from aiida.engine import run, Process, calcfunction, workfunction
from aiida.orm import Dict, Str
from aiida.plugins import CalculationFactory
from six.moves import zip

from configuration import configJson
from neighbourCalculation import get_neighbours
from structureInput import create_structure, generate_scf_input_params, create_super_cell, set_tags
from calculation import calculate_jij
from equivalentatoms import get_unique_pairs_from_equivalent_sets
from logger import logger

PwCalculation = CalculationFactory(configJson["calculationFactoryName"])


@calcfunction
def create_exchange_coupling_dictionary(**kwargs):
    exchange_coupling = [(result.dict.energy, result.dict.volume, result.dict.energy_units, label) for label, result in
                         kwargs.items()]
    print("printing create exchange_coupling result ", exchange_coupling)
    logger.info('Result saved in DB')
    return Dict(dict={'exchange_coupling': exchange_coupling})


@workfunction
def run_exchange_coupling_wf(code, pseudo_family, element):
    print('Running run_exchange_coupling_wf<{}>'.format(Process.current().pid))
    logger.info('Running run_exchange_coupling_wf<{}>'.format(Process.current().pid))

    calculations = {}
    structure = create_structure()
    structure.store()
    spinCombinationArray = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    jijPrevious = 0
    logger.info("-------------------------################ Calucation Intiated for element {} "
                "################-------------------------".format(element))

    for superCellNum in range(1, configJson["noOfSuperCells"] + 1):
        superCell = create_super_cell(structure, superCellNum, configJson["isMaterial3d"])
        logger.info("-------------------------################ SUPERCELL No is Selected {} "
                    "################-------------------------".format(superCellNum))
        pairs = get_neighbours(superCell, superCellNum)

        if not pairs:
            logger.info("Pairs Not Found for supecell Number {} ".format(superCellNum))
            continue

        unique_pairs = get_unique_pairs_from_equivalent_sets(superCell, pairs)

        if not unique_pairs:
            logger.info("No unique pair Found for supecell Number {} ".format(superCellNum))
            continue

        for pair in unique_pairs:

            for spinCombinationLabel, spinValue in list(zip(configJson["spinCombinationLabels"], spinCombinationArray)):
                calc_unique_key = spinCombinationLabel + "_" + str(superCellNum) + "_" + str(pair[0]) + "_" + str(
                    pair[1])
                superCell = set_tags(superCell, pair, superCellNum)
                scfInput = generate_scf_input_params(superCell, code, pseudo_family, spinValue[0], spinValue[1],
                                                     superCellNum, configJson["isMaterial3d"])
                logger.info(
                    'Running a scf for element {} with super cell number {} and pair {} with spin label : {} and spin values {}:'.format(
                        element, superCellNum, [x + 1 for x in pair], spinCombinationLabel, spinValue))

                calculations[calc_unique_key] = run(PwCalculation, **scfInput)
                logger.info('Result for unique key {}  is  :{}'.format(calc_unique_key, calculations[calc_unique_key][
                    'output_parameters']))
                logger.info('energy for unique key {}  is  :{}'.format(calc_unique_key, calculations[calc_unique_key][
                    'output_parameters'].dict.energy))
                logger.info('volume for unique key {}  is  :{}'.format(calc_unique_key, calculations[calc_unique_key][
                    'output_parameters'].dict.volume))
                logger.info('energy units for unique key {}  is  :{}'.format(calc_unique_key, calculations[calc_unique_key][
                    'output_parameters'].dict.energy_units))

            jijCurrent = calculate_jij(calculations, superCellNum, pair)

            logger.info('jijcurrent : {} for Supercell number {} with prv jij: {}'.format(jijCurrent, superCellNum,
                                                                                          jijPrevious))
            if abs(jijCurrent - jijPrevious) <= configJson['jijThreshold']:
                logger.info('JIJ converged for super cell {} and pair {}  '.format(superCellNum, [x + 1 for x in pair]))
                break
            else:
                jijPrevious = jijCurrent

    outputParameterResult = {
        label: result['output_parameters']
        for label, result in calculations.items()
    }

    exchange_coupling = create_exchange_coupling_dictionary(**outputParameterResult)
    print(" printing exchange_coupling result ", exchange_coupling)
    result = {'structure': structure, 'exchange_coupling': exchange_coupling}

    logger.info("-------------------------################ Calucation Completed for element {} "
                "################-------------------------".format(element))
    return result


def run_exchange_coupling(code=load_code(configJson["code_name"]), pseudo_family=configJson["pseudo_family_name"],
                          element=configJson["element_name"]):
    run_exchange_coupling_wf(code, Str(pseudo_family), Str(element))


if __name__ == '__main__':
    run_exchange_coupling()
