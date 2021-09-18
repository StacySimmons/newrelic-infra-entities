import requests
import argparse
import json


def main():
    csv_file = open('existing_hosts.csv', 'w')

    # parse arguments passed by command line
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('apikey', help='New Relic User API Key')

    args = parser.parse_args()
    api_key = args.apikey

    headers = {
        'Content-Type': 'application/json',
        'API-Key': api_key,
    }

    # this should be fed
    query = '{"query":"{\\n actor {\\n entitySearch(queryBuilder: {type: HOST}) {\\n results {\\n entities {\\n ' \
            'guid\\n name\\n reporting\\n permalink\\n tags {\\n key\\n values\\n }\\n }\\n nextCursor\\n }\\n }\\n ' \
            '}\\n}\\n", "variables":""} '

    response = requests.post('https://api.newrelic.com/graphql', headers=headers, data=query)

    if response.status_code == 200:
        c = json.loads(response.text)
        csv_file.write("\"Host Name\",\"Agent Version\",\"Operating System\",\"Full Host Name\",\"Permalink\"\n")
        next_cursor = c['data']['actor']['entitySearch']['results']['nextCursor']

        hosts_list = c['data']['actor']['entitySearch']['results']['entities']
        print(hosts_list)
        for host in hosts_list:
            csv_file.write(host['name'])
            if host['tags']:
                tags = host['tags']
                for tag in tags:
                    if tag['key'] == 'agentVersion':
                        agent_version = tag['values'][0]
                    if tag['key'] == 'operatingSystem':
                        operating_system = tag['values'][0]
                    if tag['key'] == 'fullHostname':
                        full_hostname = tag['values'][0]
                csv_file.write(
                    "," + agent_version + "," + operating_system + "," + full_hostname + "," + host['permalink'] + "\n")
        if next_cursor:
            while next_cursor:
                query = '{"query":"{\\n actor {\\n entitySearch(queryBuilder: {type: HOST}) {\\n results(cursor: \\"' + \
                        next_cursor + '\\") {\\n entities {\\n guid\\n name\\n reporting\\n permalink\\n tags {\\n key\\n ' \
                                      'values\\n }\\n }\\n nextCursor\\n }\\n }\\n }\\n}\\n", "variables":""} '
                response = requests.post('https://api.newrelic.com/graphql', headers=headers, data=query)

                if response.status_code == 200:
                    c = json.loads(response.text)
                    next_cursor = c['data']['actor']['entitySearch']['results']['nextCursor']

                    hosts_list = c['data']['actor']['entitySearch']['results']['entities']
                    print(hosts_list)
                    for host in hosts_list:
                        csv_file.write(host['name'])
                        if host['tags']:
                            tags = host['tags']
                            for tag in tags:
                                if tag['key'] == 'agentVersion':
                                    agent_version = tag['values'][0]
                                if tag['key'] == 'operatingSystem':
                                    operating_system = tag['values'][0]
                                if tag['key'] == 'fullHostname':
                                    full_hostname = tag['values'][0]
                            csv_file.write(
                                "," + agent_version + "," + operating_system + "," + full_hostname + "," + host[
                                    'permalink'] + "\n")
        csv_file.close()


if __name__ == '__main__':
    main()
