import json
import requests
from time import sleep


def get_enrichr_results(gene_set_library, genelist, description):
    ADDLIST_URL = 'http://amp.pharm.mssm.edu/Enrichr/addList'
    payload = {
        'list': (None, genelist),
        'description': (None, description)
    }

    response = requests.post(ADDLIST_URL, files=payload)
    if not response.ok:
        raise Exception('Error analyzing gene list')
    sleep(1)
    data = json.loads(response.text)

    RESULTS_URL = 'http://amp.pharm.mssm.edu/Enrichr/enrich'
    query_string = '?userListId=%s&backgroundType=%s'
    user_list_id = data['userListId']
    response = requests.get(RESULTS_URL + query_string % (user_list_id, gene_set_library))
    sleep(1)
    return [data['shortId'], json.loads(response.text)]


def get_libraries():
    libs_json = json.loads(requests.get('http://amp.pharm.mssm.edu/Enrichr/datasetStatistics').text)
    libs = [lib['libraryName']for lib in libs_json['statistics']]
    return libs

def main():
    for library in get_libraries():
        crisp = open('test.txt', 'r').read()
        data = get_enrichr_results(library, crisp, 'Sample gene list')
        print('http://amp.pharm.mssm.edu/Enrichr/enrich?dataset={0}'.format(data[0]))
        # Result fields:
        # 0 - Index
        # 1 - Term
        # 2 - P-value
        # 3 - Z-score
        # 4 - Combined score
        # 5 - Genes
        # 6 - Adjusted p-value
        # 7 - Old p-value
        # 8 - Old adjusted p-value
        # Old p-value and old adjusted p-value were added for backward compatibility.
        # In general you don't need them
        print('Term\tP-Value\tAdjusted p-value\tZ-score\tCombined score\tGenes')
        for term in data[1][library]:
            print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(term[1], term[2], term[6], term[3], term[4], '\t'.join(term[5])))
    return None


if __name__ == '__main__':
    main()