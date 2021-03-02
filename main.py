import json
import requests
from time import sleep


def get_enrichr_results(gene_set_library, genelist, description):
    ADDLIST_URL = 'https://maayanlab.cloud/Enrichr/addList'
    payload = {
        'list': (None, genelist),
        'description': (None, description)
    }

    response = requests.post(ADDLIST_URL, files=payload)
    if not response.ok:
        raise Exception('Error analyzing gene list')
    sleep(1)
    data = json.loads(response.text)

    RESULTS_URL = 'https://maayanlab.cloud/Enrichr/enrich'
    query_string = '?userListId=%s&backgroundType=%s'
    user_list_id = data['userListId']
    response = requests.get(RESULTS_URL + query_string % (user_list_id, gene_set_library))
    sleep(1)
    return [data['shortId'], json.loads(response.text)]


def get_libraries():
    libs_json = json.loads(requests.get('https://maayanlab.cloud/Enrichr/datasetStatistics').text)
    libs = [lib['libraryName']for lib in libs_json['statistics']]
    return libs

def main():
    crisp = open('test.txt', 'r').read()
    libraries = get_libraries()
    for library in libraries:
        data = get_enrichr_results(library, crisp, 'Sample gene list')
        print('https://maayanlab.cloud/enrich?dataset={0}'.format(data[0]))
    return None


if __name__ == '__main__':
    main()
