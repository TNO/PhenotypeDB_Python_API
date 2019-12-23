import os
import logging 
import subprocess
import hashlib 
import requests
from requests.auth import HTTPBasicAuth

def md5_digest(input_string):
    """Generates MD5 hash from the input str.
    
    Arguments:
        input_string {str} -- Input str to generate MD5 hash from. 
    
    Returns:
        str -- MD5 hash
    """
    md5 = hashlib.md5()
    md5.update(input_string.encode('utf-8'))
    return md5.hexdigest()

def generate_device_id(user_name):
    """Generates MD5 hash from unique device id.
        
    Arguments:
        user_name {str} -- Phenotype DB user name
    
    Returns:
        str -- Device id
    """
    machine_id = ".".join(list(os.uname()))
    # machine_id = subprocess.check_output('wmic csproduct get uuid')\
    # .decode().split('\n')[1].strip().lower()
    device_id = md5_digest(machine_id + user_name)
    return device_id

class PhenoDBAPI:
        
    def __init__(self, user_name, password, api_key):
        """Object that communicates with Phenotype Database API.
        It authenticates as soon as the object is created. 
        
        Arguments:
            user_name {str} -- Phenotype Database account user name
            password {str} -- Phenotype Database account password
            api_key {str} -- Phenotype Database user API key
        """        
        self.base_url = "https://dashin.eu/interventionstudies/api/"
        self.device_id = generate_device_id(user_name)
        self.user_name = user_name 
        self.password = password
        self.api_key = api_key
        self.token = None
        self.api_token = None
        self.validate = None
        try: 
            self.token = self._authenticate()
            self.api_token = self.token['token']
        except Exception as e:
            logging.error(e)

    def _authenticate(self):
        """Authenticates to Phenotype DB API
        
        Returns:
            dict -- Dictionary with session token and sequence number.
        """        
        token = requests.get(self.base_url + 'authenticate', 
                             params={'deviceID':self.device_id}, 
                             auth=HTTPBasicAuth(self.user_name, self.password))
        logging.info("Authentication successful.")
        return token.json()

    def _gen_validation(self):
        """ Generates a validation str for getting requests. 
        """        
        self.token['sequence'] = str(int(self.token['sequence']) + 1)
        self.validate = md5_digest(self.api_token + self.token['sequence'] + self.api_key)

    def _get_request(self, query, parameters=None):
        """Collects the data from API with the relevant query. 
        
        Arguments:
            query {str} -- Query string such as `getStudies` or `getSubjectsForStudy`.
        
        Keyword Arguments:
            parameters {dict} -- Dictionary that contains relevant tokens for query (default: {None})
        
        Returns:
            dict -- Data in JSON format.
        """        
        try:
            self._gen_validation()
            params = {'validation': self.validate, 'deviceID': self.device_id}
            if parameters is not None:
                for k,v in parameters.items():
                    params[k] = v
            response = requests.get(self.base_url + query, params=params)
            if response.status_code == 200:
                data = response.json()
            elif response.status_code == 403:
                print("Authentication error.")
                data = None
            else:
                print("Unknown error.")
                data = None
            return data
        except Exception as e:
            logging.error(e)
            print(e)
        return None
        
    def get_studies(self):
        """Get data about all the studies. 
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getStudies')
        return data['studies']

    def get_subjects_for_study(self,study_token):
        """Get data about all the studies.
        
        Arguments:
            study_token {str} -- Study token
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getSubjectsForStudy',
                                 parameters={'studyToken':study_token})
        return data['subjects']

    def get_subject_groups_for_study(self, study_token):
        """Get subject groups for study using study token.
        
        Arguments:
            study_token {str} -- Study token
        
        Returns:
             dict -- Data in JSON format.
        """
        data = self._get_request('getSubjectGroupsForStudy',
                                 parameters={'studyToken':study_token})
        return data['subjectGroups']

    def get_sample_and_treatment_groups_for_study(self,study_token):
        """Get sample and treatment groups using study token.
        
        Arguments:
            study_token {str} -- Study token
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getSampleAndTreatmentGroupsForStudy',
                                 parameters={'studyToken':study_token})
        return data['sampleAndTreatmentGroups']

    def get_treatment_types_for_study(self,study_token):
        """Get treatment types of a study using study token.
        
        Arguments:
            study_token {str} -- Study token
        
        Returns:
            dict -- Data in JSON format.
        """
        data = self._get_request('getTreatmentTypesForStudy',
                                 parameters={'studyToken':study_token})     
        return data['treatmentTypes']

    def get_sample_types_for_study(self, study_token):
        """Get sample types from a study using study token.
        
        Arguments:
            study_token {str} -- Study token
        
        Returns:
            dict -- Data in JSON format.
        """
        data = self._get_request('getSampleTypesForStudy',
                                 parameters={'studyToken':study_token})    
        return data['sampleTypes']

    def get_assays_for_study(self, study_token):
        """Collect assays for the given study. 
        
        Arguments:
            study_token {str} -- Study token
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getAssaysForStudy',
                                 parameters={'studyToken':study_token})
        return data['assays']

    def get_samples_for_study(self, study_token):
        """Collect samples for the given study.
        
        Arguments:
            study_token {str} -- Assay token
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getSamplesForStudy',
                                 parameters={'studyToken':study_token})
        return data['samples']

    def get_subjects_for_assay(self, assay_token):
        """Collect subjects for given assay.
        
        Arguments:
            assay_token {str} -- Assay token
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getSubjectsForAssay',
                                 parameters={'assayToken':assay_token})
        return data['subjects']

    def get_samples_for_assay(self, assay_token):
        """Collect samples for given assay. 
        
        Arguments:
            assay_token {str} -- Assay token
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getSamplesForAssay',
                                 parameters={'assayToken':assay_token})
        return data['samples']

    def get_features_for_assay(self, assay_token):
        """Collect features for the given assay. 
        
        Arguments:
            assay_token {str} -- Assay token
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getFeaturesForAssay',
                                 parameters={'assayToken':assay_token})
        return data['features']

    def get_measurement_data_for_assay(self, assay_token):
        """Collect measurements for the given assay 
        
        Arguments:
            assay_token {str} -- Assay token
        
        Returns:
            dict -- Data in JSON format.
        """        
        data = self._get_request('getMeasurementDataForAssay',
                                 parameters={'assayToken':assay_token})
        return data['measurements']

    