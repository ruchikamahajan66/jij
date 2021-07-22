import math

from configuration import configJson
from logger import jij_nbr_logger


def get_neighbours(super_cell_aiida, superCellNum):
    sitesList = []
    for i in range(len(super_cell_aiida.sites)):
        if super_cell_aiida.sites[i].kind_name == configJson["chosenElement"]:
            temp = {
                "index": i,
                "pos": super_cell_aiida.sites[i].position

            }
            sitesList.append(temp)

    sortedAtomIndexList = sort_distance(sitesList, configJson["chosenSite"] - 1, superCellNum)
    atom = get_group_atom_basedon_distance(sortedAtomIndexList, configJson["nearestNbrLimit"],
                                                   configJson["similarCalcThreshold"])
    nbr_pairs = []
    site_index = configJson["chosenSite"] - 1
    jij_nbr_logger.info("###################################  Eligible Pairs with Distance for supercell number {} "
                        "###################################".format(superCellNum))
    jij_nbr_logger.info("                       Atom1           Atom2           Distance ")
    if atom:
        nbr_pairs.append([site_index, atom["index"]])
        jij_nbr_logger.info("                       {}           {}           {} ".format(
            site_index + 1, atom['index'] + 1, atom['distance']))
    return nbr_pairs


def sort_distance(sites, site_index, superCellNum):
    chosenSite = 0
    for i in range(len(sites)):
        if sites[i]["index"] == site_index:
            chosenSite = i
            break

    chosenSiteAtom = sites.pop(chosenSite)
    result = calculate_distance(chosenSiteAtom, sites)
    result.sort(key=lambda x: x['distance'])
    jij_nbr_logger.info("###################################  Total Pair Distances with supercell number  {}"
                        "###################################".format(superCellNum))
    jij_nbr_logger.info("                       Atom1           Atom2           Distance ")

    for atom in result:
        jij_nbr_logger.info("                       {}           {}           {} ".format(
            chosenSite + 1, atom['index'] + 1, atom['distance']))

    return result;


def get_group_atom_basedon_distance(sorted_atomindex_list, nbr_limit, threshold):
    res = []
    nth_nbr = {}

    for atomIndex in sorted_atomindex_list:
        if not res:
            res.append(atomIndex)
        else:
            if atomIndex["distance"] - res[len(res)-1]["distance"] > threshold:
                res.append(atomIndex)

    if len(res) >= nbr_limit:
        nth_nbr = res[nbr_limit - 1]

    return nth_nbr


def calculate_distance(chosen_site_atom, list):
    result = []
    for atom in list:
        dist = euc_distance(chosen_site_atom, atom)
        result.append({
            "index": atom["index"],
            'distance': dist
        })
    return result


def euc_distance(atom1, atom2):
    return math.sqrt((atom1["pos"][0] - atom2["pos"][0]) * (atom1["pos"][0] - atom2["pos"][0]) + (
            atom1["pos"][1] - atom2["pos"][1]) * (
                             atom1["pos"][1] - atom2["pos"][1]) +
                     (atom1["pos"][2] - atom2["pos"][2]) * (atom1["pos"][2] - atom2["pos"][2]))