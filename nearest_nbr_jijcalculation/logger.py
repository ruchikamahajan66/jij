import logging
from configuration import configJson

logger = logging.getLogger('workflow')
logger.setLevel(logging.INFO)

f_handler = logging.FileHandler(configJson['process_tag']+'workflow.log')
f_formatter = logging.Formatter('%(asctime)s -- %(message)s')
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(f_formatter)
logger.addHandler(f_handler)

jij_calc_logger = logging.getLogger('jij_calc')
jij_calc_logger.setLevel(logging.INFO)

jij_calc_f_handler = logging.FileHandler(configJson['process_tag']+'jij_calc.log')
jij_calc_f_formatter = logging.Formatter('%(asctime)s -- %(message)s')
jij_calc_f_handler.setLevel(logging.INFO)
jij_calc_f_handler.setFormatter(f_formatter)
jij_calc_logger.addHandler(jij_calc_f_handler)

jij_nbr_logger = logging.getLogger('jij_nbr')
jij_nbr_logger.setLevel(logging.INFO)

jij_nbr_f_handler = logging.FileHandler(configJson['process_tag']+'jij_nbr.log')
jij_nbr_f_formatter = logging.Formatter('%(asctime)s -- %(message)s')
jij_nbr_f_handler.setLevel(logging.INFO)
jij_nbr_f_handler.setFormatter(f_formatter)
jij_nbr_logger.addHandler(jij_nbr_f_handler)

