# PhenotypeDB_Python_API

Python API for collecting data from Phenotype Database.

## Installation 

In order to install, clone the repository first: 
```
git clone git@gitlab-dv.tno.nl:DataScience-MSB/Tools/phenotypedb_python_api.git --depth 1 
```
Then change directory to the folder of the repository:
```
cd phenotypedb_python_api
```
Run install:
```
python setup.py install
```

## Usage 

In order to make requests from [Phenotype Database](https://dashin.eu/interventionstudies/), you need to have your user name, password and API key ready. 

```python
>>> from phenodb_api import PhenoDBAPI
>>> ap = PhenoDBAPI(user_name, password, api_key)
>>>
>>> # get_studies method collects the study data as list of dictionaries (JSON)
>>>
>>> list(map(lambda study: study.get('code'),ap.get_studies()))
['PRA_131461', 'foodmix_mouse_AtherosclerosisStudy', 'foodmix_mouse_CRPstudy', 'NASH', 'AGER-MELO', 'ADMIT_01', 'Human_IPF_data', 'VP9-fibrosis', 'VP-9_fibrosis_part2', 'UUO-study', 'IFC-CNR-DEI', 'Diclofenac', 'DIMISA-HA', 'AVAG', 'ETHERPATHS', 'HealthGrain', 'ELI-Co_Fibrosis', 'VitC-LPS-PBMC', 'Foodmix', 'NuGO_PPSH', '10_OAD_', 'LIPGENE', 'SU.VI.MAX', '13-0245', 'nash_public_002', 'PhenFlex1_1_CHDR1211', 'PhenFlex1_2_CHDR1230', 'NuGO_PPS1', 'NuGO_PPS2', 'NuGO_PPS3', 'AIRC-ISS', 'mouse_combi_study', 'HuMet_mrt_2012', 'VP9-LPS_TNO-P8600', 'FLAVURS', 'NCT02710513', 'TUTORIAL', 'UCD_TWIN', '9218_Fat_challenge_tests']
```

Almost all of the methods are copied from [R API](https://gitlab-dv.tno.nl/DataScience-MSB/RPackages/PhenotypeDatabase-RClient).

## Contact 

In case of questions or issues, contact [@ozsezens](https://gitlab-dv.tno.nl/ozsezens). 