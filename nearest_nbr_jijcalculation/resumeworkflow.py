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

    jijPrevious = configJson['resumeWorkflow']['jij_prv']
    logger.info("-------------------------################ Calucation Intiated for element {} "
                "################-------------------------".format(element))
    pairs = []
    try:
        for superCellNum in range(1, configJson["noOfSuperCells"] + 1):
            superCell = create_super_cell(structure, superCellNum, configJson["isMaterial3d"])
            logger.info("-------------------------################ SUPERCELL No is Selected {} "
                        "################-------------------------".format(superCellNum))
            if not pairs:
                pairs = get_neighbours(superCell, superCellNum)

            if not pairs:
                logger.info("Pairs Not Found for supecell Number {} ".format(superCellNum))
                continue

            if superCellNum < configJson['resumeWorkflow']['supercell']:
                logger.info(
                    "Calculation being skipped for  supercell : {} ".format(superCellNum))
                continue
            pair = pairs[0]

            for spinCombinationLabel, spinValue in list(
                    zip(configJson["spinCombinationLabels"], spinCombinationArray)):
                calc_unique_key = spinCombinationLabel + "_" + str(superCellNum) + "_" + str(pair[0]) + "_" + str(
                    pair[1])
                superCell = set_tags(superCell, pair, superCellNum, configJson["isMaterial3d"])
                scfInput = generate_scf_input_params(superCell, code, pseudo_family, spinValue[0], spinValue[1],
                                                     superCellNum, configJson["isMaterial3d"])
                logger.info(
                    'Running a scf for element {} with super cell number {} and pair {} with spin label : {} and spin values {}:'.format(
                        element, superCellNum, [x + 1 for x in pair], spinCombinationLabel, spinValue))
                if configJson['resumeWorkflow'][spinCombinationLabel]:
                    logger.info(
                        "Calculation being loaded from db for supercell : {} and spin label : {}".format(superCellNum,
                                                                                                         spinCombinationLabel))
                    calculations[calc_unique_key] = load_calc_data(configJson['resumeWorkflow'][spinCombinationLabel])
                else:
                    calculations[calc_unique_key] = run(PwCalculation, **scfInput)
                output_dict = calculations[calc_unique_key]['output_parameters'].dict
                logger.info('Unique key {}  is  energy :{}, volume: {}, energy_units: {} '.format(calc_unique_key,
                                                                                                  output_dict.energy,
                                                                                                  output_dict.volume,
                                                                                                  output_dict.energy_units))

            jijCurrent = calculate_jij(calculations, superCellNum, pair)

            logger.info('jijcurrent : {} for Supercell number {} with prv jij: {}'.format(jijCurrent, superCellNum,
                                                                                          jijPrevious))
            if abs(jijCurrent - jijPrevious) <= configJson['jijThreshold']:
                logger.info(
                    'JIJ converged for super cell {} and pair {}  '.format(superCellNum, [x + 1 for x in pair]))
                break
            else:
                jijPrevious = jijCurrent
    except:
        logger.info('Error occurred while calculation.')

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


def load_calc_data(pk):
    from aiida.orm import load_node
    calc = load_node(pk)
    logger.info("pk == ".format(pk))
    logger.info(pk, calc.res.energy, calc.res.volume, calc.res.energy_units)
    return {
            "dict": {
                'energy': calc.res.energy,
                'volume': calc.res.volume,
                'energy_units': calc.res.energy_units
            }
        }


def run_exchange_coupling(code=load_code(configJson["code_name"]), pseudo_family=configJson["pseudo_family_name"],
                          element=configJson["element_name"]):
    run_exchange_coupling_wf(code, Str(pseudo_family), Str(element))


if __name__ == '__main__':
    run_exchange_coupling()
