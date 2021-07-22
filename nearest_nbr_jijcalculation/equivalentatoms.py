import pymatgen as mg
from pymatgen.symmetry.analyzer import PointGroupAnalyzer


def get_unique_pairs_from_equivalent_sets(structure, pairs):
    ase_atoms = structure.get_ase()
    species = ase_atoms.get_chemical_symbols()
    coordinates = ase_atoms.get_positions()
    mol = mg.Molecule(species, coordinates)

    pointGroupAnalyzer = PointGroupAnalyzer(mol)

    equivalent_site_sets = pointGroupAnalyzer.get_equivalent_atoms()["eq_sets"]
    unique_pairs = []
    for equiv_set in equivalent_site_sets.values():
        for pair in pairs:
            if pair[1] in equiv_set:
                unique_pairs.append(pair)
                break

    return unique_pairs
