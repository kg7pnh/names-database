"""
get_surnames
"""

#! /usr/bin/python3
# coding: utf_8 -*-

import json
# import os
import re
# import sys
from pathlib import Path
import requests

URLS_SURNAMES = [
    {
        'base_url': 'http://www.americanlastnames.us/last-names/',
        'type': 'americanlastnames',
        'start_paths': [
            'Albanian/index.html'
            'Algerian/index.html',
            'Amish/index.html',
            'Anglo-Saxon/index.html',
            'Angolan/index.html',
            'Arabic/index.html',
            'Armenian/index.html',
            'Assyrian/index.html',
            'Austrian/index.html',
            'Azeri/index.html',
            'Bahraini/index.html',
            'Bangladeshi/index.html',
            'Basque/index.html',
            'Belarusian/index.html',
            'Belgian/index.html',
            'Beninese/index.html',
            'Bhutanese/index.html',
            'Bosnian/index.html',
            'Botswanan/index.html',
            'Bulgarian/index.html',
            'Burkinabe/index.html',
            'Burundian/index.html',
            'Cambodian/index.html',
            'Cameroonian/index.html',
            'Cape verdean/index.html',
            'Celtic/index.html',
            'Central african republic/index.html',
            'Chilean/index.html',
            'Chinese/index.html',
            'Comoran/index.html',
            'Congolese/index.html',
            'Cornish British/index.html',
            'Creole/index.html',
            'Croatian/index.html',
            'Czech/index.html',
            'Danish/index.html',
            'Djiboutian/index.html',
            'Dutch/index.html',
            'Egyptian/index.html',
            'English/index.html',
            'Estonian/index.html',
            'Ethiopian/index.html',
            'Falkland/index.html',
            'Faroese/index.html',
            'Filipino/index.html',
            'Finnish/index.html',
            'Flemish/index.html',
            'French/index.html',
            'Gabonese/index.html',
            'Gaelic/index.html',
            'Gambian/index.html',
            'Georgian/index.html',
            'German/index.html',
            'Ghanaian/index.html',
            'Greek/index.html',
            'Greenlandic/index.html',
            'Guam/index.html',
            'Guinean/index.html',
            'Haitian/index.html',
            'Herzegovinian/index.html',
            'Hungarian/index.html',
            'Icelandic/index.html',
            'Indian/index.html',
            'Indonesian/index.html',
            'Irish/index.html',
            'Italian/index.html',
            'Japanese/index.html',
            'Jewish/index.html',
            'Jordanian/index.html',
            'Kazakh/index.html',
            'Kenyan/index.html',
            'Korean/index.html',
            'Latvian/index.html',
            'Lebanese/index.html',
            'Lesothan/index.html',
            'Liberian/index.html',
            'Lithuanian/index.html',
            'Macedonian/index.html',
            'Malagasy/index.html',
            'Malawian/index.html',
            'Malian/index.html',
            'Maltese/index.html',
            'Maori/index.html',
            'Mauritanian/index.html',
            'Mauritian/index.html',
            'Moldovan/index.html',
            'Moroccan/index.html',
            'Mozambican/index.html',
            'Namibian/index.html',
            'Nigerian/index.html',
            'Nigerien/index.html',
            'Norwegian/index.html',
            'Pakistani/index.html',
            'Peruvian/index.html',
            'Polish/index.html',
            'Portuguese/index.html',
            'Romanian/index.html',
            'Russian/index.html',
            'Rwandan/index.html',
            'Samoan/index.html',
            'Scottish/index.html',
            'Senegalese/index.html',
            'Serbian/index.html',
            'Sierra leonean/index.html',
            'Slovakian/index.html',
            'Slovenian/index.html',
            'Somali/index.html',
            'South african/index.html',
            'Spanish/index.html',
            'Sudanese/index.html',
            'Swazi/index.html',
            'Swedish/index.html',
            'Swiss/index.html',
            'Tajik/index.html',
            'Tanzanian/index.html',
            'Togonese/index.html',
            'Tunisian/index.html',
            'Turkish/index.html',
            'Ugandan/index.html',
            'Ukrainian/index.html',
            'Uzbek/index.html',
            'Welsh/index.html',
            'Zambian/index.html',
            'Zimbabwean/index.html'
        ]
    }
    # {
    #     'url': 'https://surnames.behindthename.com/names/list',
    #     'type': 'behindthename'
    # }
]

# class App(dict):
#     def __str__(self):
#         return json.dumps(self)

def write_csv(type, names_data):
    """
    write_csv
    """
    with open('./csv/%s.csv' % type, 'w') as names:
        for entry in names_data:
            for name in names_data[entry]['names']:
                names.write('"%s","%s"\n' % (entry, name))
    for nationality in names_data:
        folder_name = nationality.lower()
        Path('./csv/%s' % folder_name).mkdir(parents=True, exist_ok=True)
        with open('./csv/%s/%s.csv' % (nationality, type), 'w') as nationality_names:
            for name in names_data[nationality]['names']:
                nationality_names.write('"%s"\n' % name)

def write_json(type, names_data):
    """
    write_json
    """
    with open('./json/%s.json' % type, 'w') as all_names:
        json.dump(names_data, all_names, sort_keys=True)
    for nationality in names_data:
        folder_name = nationality.lower()
        Path('./json/%s' % folder_name).mkdir(parents=True, exist_ok=True)
        with open(('./json/%s/%s.json' % (folder_name, type)), 'w') as nationality_names:
            json.dump(names_data[nationality], nationality_names, sort_keys=True)

def write_txt(type, names_data):
    """
    write_txt
    """
    for nationality in names_data:
        file_name = nationality.lower()+'_'+type
        with open('./txt/%s.txt' % file_name, 'w') as nationality_names:
            for name in names_data[nationality]['names']:
                nationality_names.write('%s\n' % name)

def merge_names(new_names, consolidated_names):
    """
    merge_names
    """
    if consolidated_names:
        for nationality in new_names:
            if nationality in consolidated_names:
                name_count = consolidated_names[nationality]['count']
                for name in new_names[nationality]['names']:
                    if name not in consolidated_names[nationality]['names']:
                        consolidated_names[nationality]['names'].append(name)
                        name_count += 1
                        consolidated_names[nationality]['count'] = name_count
            else:
                consolidated_names[nationality] = new_names[nationality]
    else:
        consolidated_names = new_names
    return consolidated_names

def get_content(url):
    """
    get_content
    """
    html = requests.get(url)
    return html

def get_american_last_names_alpha(url):
    """
    get_american_last_names_alpha
    """
    names = []
    regex = re.compile(r'<td align=left>(?P<name>[a-zA-Z]{2,})</td>')
    regex_link = re.compile(
        r'<td align=left><a href=\"../../../[a-zA-Z]/[a-zA-Z]*' \
        '.html\">(?P<name>[a-zA-Z]*)</a></td>')
    regex_additional = re.compile(r'<a href=\"(?P<path>[A-Za-z]-[0-9]\.html)' \
        '\"><img border=none src=\"../../../images/nextarrow.jpg\"')
    contents = get_content(url).text.splitlines()
    for content in contents:
        if re.match(regex, content):
            name = re.match(regex, content).groupdict()['name']
            names.append(name)
        elif re.match(regex_link, content):
            name = re.match(regex_link, content).groupdict()['name']
            names.append(name)
        elif re.match(regex_additional, content):
            path = re.match(regex_additional, content).groupdict()['path']
            new_url = url.replace(url.split('/')[6], path)
            names += get_american_last_names_alpha(new_url)
    return names

def get_american_last_names(url, nationality):
    """
    get_american_last_names
    """
    print('\tRetrieving %s names from %s' % (nationality.title(), url))

    names = []
    regex = re.compile(r'[ ]?<a href=\"../../last-names/' \
        '(?P<path>[a-zA-z\- ]*/[a-zA-z]/[a-zA-Z]-[0-9].html)\">')
    contents = get_content(url).text.splitlines()
    for content in contents:
        content_split = content.split('|')
        for split in content_split:
            if re.match(regex, split):
                for match in re.finditer(regex, split):
                    path = match.group('path')
                    alpha_url = url.replace(
                        nationality+'/index.html', path)
                    names += get_american_last_names_alpha(alpha_url)
    if not names:
        names = None
    return names

def process_american_last_names(url, start_paths=None):
    """
    process_american_last_names
    """
    print('\tProcessing entries for %s' % url)
    names = {}
    for start_path in start_paths:
        nationality = start_path.split('/')[0]

        names_response = get_american_last_names(url+start_path, nationality)
        if names_response:
            names[nationality] = {}
            names[nationality]['names'] = names_response
            names[nationality]['count'] = len(names[nationality]['names'])
    return names

def process_names_list(url):
    """
    process_names_list
    """
    print('\tProcessing %s as NamesList' % url)
    return True

def process_behind_the_name(url):
    """
    process_behind_the_name
    """
    print('\tProcessing %s as BehindTheName' % url)
    return True

def process_target(target):
    """
    process_target
    """
    names = {}
    if target['type'] == 'americanlastnames':
        names = process_american_last_names(target['base_url'], target['start_paths'])
    elif target['type'] == 'nameslist':
        names = process_names_list(target['url'])
    elif target['type'] == 'behindthename':
        names = process_behind_the_name(target['url'])
    else:
        print('\tInvalid Type Specified: %s' % target[type])
    return names

def main():
    """
    main
    """
    compiled_names = None
    targets = URLS_SURNAMES
    for target in targets:
        print('Processing target %s' % target['base_url'])
        names = process_target(target)
        compiled_names = merge_names(names, compiled_names)

    write_csv('surnames', compiled_names)
    write_json('surnames', compiled_names)
    write_txt('surnames', compiled_names)

if __name__ == "__main__":
    main()
