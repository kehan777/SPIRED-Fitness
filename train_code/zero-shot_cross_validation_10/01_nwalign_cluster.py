import os
import itertools
import pandas as pd
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

#######################################################################
# predefined parameters
#######################################################################


def calculate_identity(first, second):
    return float(os.popen(f"nwalign {first} {second}").read().split("Sequence identity:")[1].split("(=")[0])


names = ["A0A1I9GEU1_NEIME_Kennouche_2019", "A0A247D711_LISMN_Stadelmann_2021", "A4D664_9INFA_Soh_2019", "A4_HUMAN_Seuma_2022", "AACC1_PSEAI_Dandage_2018", "ADRB2_HUMAN_Jones_2020", "AICDA_HUMAN_Gajula_2014_3cycles", "ANCSZ_Hobbs_2022", "B2L11_HUMAN_Dutta_2010_binding-Mcl-1", "C6KNH7_9INFA_Lee_2018", "CAPSD_AAV2S_Sinai_2021", "CASP3_HUMAN_Roychowdhury_2020", "CASP7_HUMAN_Roychowdhury_2020", "CD19_HUMAN_Klesmith_2019_FMC_singles", "D7PM05_CLYGR_Somermeyer_2022", "ENVZ_ECOLI_Ghose_2023", "ESTA_BACSU_Nutschel_2020", "F7YBW7_MESOW_Ding_2023", "F7YBW8_MESOW_Aakre_2015", "GCN4_YEAST_Staller_2018", "GLPA_HUMAN_Elazar_2016", "GRB2_HUMAN_Faure_2021", "HEM3_HUMAN_Loggerenberg_2023", "KCNE1_HUMAN_Muhammad_2023_expression", "KCNJ2_MOUSE_Coyote-Maestas_2022_function", "LYAM1_HUMAN_Elazar_2016", "MET_HUMAN_Estevam_2023", "MLAC_ECOLI_MacRae_2023", "NRAM_I33A0_Jiang_2016", "OTC_HUMAN_Lo_2023", "OXDA_RHOTO_Vanella_2023_expression", "PAI1_HUMAN_Huttinger_2021", "PHOT_CHLRE_Chen_2023", "PPARG_HUMAN_Majithia_2016", "PPM1D_HUMAN_Miller_2022", "PRKN_HUMAN_Clausen_2023", "Q53Z42_HUMAN_McShan_2019_expression", "Q6WV13_9MAXI_Somermeyer_2022", "Q837P4_ENTFA_Meier_2023", "Q837P5_ENTFA_Meier_2023", "R1AB_SARS2_Flynn_2022", "RDRP_I33A0_Li_2023", "REV_HV1H2_Fernandes_2016", "RNC_ECOLI_Weeks_2023", "RPC1_LAMBD_Li_2019_low-expression", "S22A1_HUMAN_Yee_2023_activity", "SC6A4_HUMAN_Young_2021", "SERC_HUMAN_Xie_2023", "SHOC2_HUMAN_Kwon_2022", "TAT_HV1BR_Fernandes_2016"]

#######################################################################
# nwalign
#######################################################################

files = []
for name in names:
    files.append(f"proteingym/{name}.fasta")

data = pd.DataFrame(index=names, columns=names)
for file1, file2 in list(itertools.combinations(files, 2)):
    name1 = file1.split("/")[-1].split(".")[0]
    name2 = file2.split("/")[-1].split(".")[0]

    score = max(calculate_identity(file1, file2), calculate_identity(file2, file1))
    data.loc[name1, name2] = score
    data.loc[name2, name1] = score

#######################################################################
# cluster
#######################################################################

data[data.isnull()] = 1
data = 1 - data

condense = squareform(data.values)
linkage = hierarchy.linkage(condense, method="complete")
cluster_index = hierarchy.fcluster(linkage, 10, criterion="maxclust")
pd.DataFrame({"protein_name": data.index, "cluster_index": cluster_index}).to_csv("cluster.csv", index=False)
