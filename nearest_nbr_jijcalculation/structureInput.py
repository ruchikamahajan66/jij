# -*- coding: utf-8 -*-
"""Helper functions."""
from __future__ import absolute_import

from aiida.engine import calcfunction
from aiida.plugins import CalculationFactory, DataFactory
from aiida_quantumespresso.utils.pseudopotential import validate_and_prepare_pseudos_inputs

from configuration import configJson

Dict = DataFactory('dict')

PwCalculation = CalculationFactory(configJson["calculationFactoryName"])
StructureData1 = DataFactory('structure')


@calcfunction
def create_structure():
    """creating StructureData object"""
    from aiida import orm
    import numpy as np

    cell = np.array(configJson["crystal_vectors"])
    structure = orm.StructureData(cell=cell)
    for i in range(int(configJson['numberOfAtoms'])):
        structure.append_atom(
            position=(configJson["crystal_atoms"]["x_positions"][i], configJson["crystal_atoms"]["y_positions"][i],
                      configJson["crystal_atoms"]["z_positions"][i]),
            symbols=configJson["crystal_atoms"]["atom_names"][i])

    return structure


def generate_scf_input_params(structure, code, pseudo_family, mag1, mag2, super_cell_num, isMaterial3d):
    """Construct a builder for the `PwCalculation` class and populate its inputs.

    :return: `ProcessBuilder` instance for `PwCalculation` with preset inputs
    """
    scfParams = configJson["parameters"]
    start_mag = get_magnetization(structure, mag1, mag2)

    if any([m != 0 for m in start_mag.values()]):
        scfParams['SYSTEM']['nspin'] = configJson["nSpinValue"]
        scfParams['SYSTEM']['starting_magnetization'] = start_mag

    KpointsData = DataFactory('array.kpoints')

    kPoints = KpointsData()
    list = [round(x / super_cell_num) for x in configJson["kPointsDict"]]

    if not isMaterial3d:
        list[len(list) - 1] = 1
    kPoints.set_kpoints_mesh(list)

    builder = PwCalculation.get_builder()
    builder.code = code
    builder.structure = structure
    builder.kpoints = kPoints
    builder.parameters = Dict(dict=scfParams)
    builder.pseudos = validate_and_prepare_pseudos_inputs(
        structure, pseudo_family=pseudo_family)
    builder.metadata.label = configJson["builder_metadata_label"]
    builder.metadata.options.queue_name = "week"
    builder.metadata.description = configJson["builder_metadata_description"]
    builder.metadata.options.resources = {'num_machines': configJson["builder_metadata_options_resources_machine"]}
    builder.metadata.options.max_wallclock_seconds = configJson["builder_metadata_options_max_wallclock_seconds"]

    return builder


def get_magnetization(structure, mag1, mag2):
    start_mag = {}
    for i in structure.kinds:
        if i.name.endswith("1"):
            start_mag[i.name] = mag1
        elif i.name.endswith("2"):
            start_mag[i.name] = mag2
        elif i.name == configJson["compoundElement1"] + "3":
            start_mag[i.name] = configJson["type1_mag_value"]
        else:
            start_mag[i.name] = configJson["type2_mag_value"]

    return start_mag


def create_super_cell(structure, factor, isMaterial3d):
    if isMaterial3d:
        superCellStructureASE = structure.get_ase() * [factor, factor, factor]
    else:
        superCellStructureASE = structure.get_ase() * [factor, factor, 1]

    structureDataAiiDA = DataFactory('structure')
    superCellStructureAiiDAObject = structureDataAiiDA(ase=superCellStructureASE)
    return superCellStructureAiiDAObject


def set_tags(super_cell_aiida, pair, super_cell_num):
    superCellStructureASE = super_cell_aiida.get_ase()
    tags = []
    for i in range(1, configJson["numberOfAtoms"] * super_cell_num * super_cell_num + 1):
        tags.append(3)
    tags[int(pair[0])] = '1'
    tags[int(pair[1])] = '2'
    superCellStructureASE.set_tags(tags)
    structureDataAiiDA = DataFactory('structure')
    superCellStructureAiiDAObject = structureDataAiiDA(ase=superCellStructureASE)

    return superCellStructureAiiDAObject
