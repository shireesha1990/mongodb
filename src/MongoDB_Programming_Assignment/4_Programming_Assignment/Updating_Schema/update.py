#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.

The data is already in the database. But you have been given a task to also include 'binomialAuthority'
information in the data, so you have to go through the data and update the existing entries.

The following things should be done in the function add_field:
- process the csv file and extract 2 fields - 'rdf-schema#label' and 'binomialAuthority_label'
- clean up the 'rdf-schema#label' same way as in the first exercise - removing redundant "(spider)" suffixes
- return a dictionary, with 'label' being the key, and 'binomialAuthority_label' the value
- if 'binomialAuthority_label' is "NULL", skip the item

The following should be done in the function update_db:
- query the database by using the field 'label'
- update the data, by adding a new item under 'classification' with a key 'binomialAuthority'


The resulting data should look like this:
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'binomialAuthority': None,
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
"""
import codecs
import csv
import json
import pprint

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'binomialAuthority_label': 'binomialAuthority'}


def add_field(filename, fields):

    process_fields = fields.keys()
    data = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()
        # YOUR CODE HERE
        for line in reader:
            # iterate over all keys in line to find proper value
            for key in line.keys():
                if key in process_fields:
                    #assign key to new key if label
                    value = None
                    if FIELDS[key] == 'label':
                        new_key = clean_label(line[key])
                    else:
                        if line[key] != 'NULL':
                            
                            value = binominal_split(line[key])
                            #print key, line[key] ,value
                    #print new_key,value   
                    data[new_key] = value
                    
    #pprint.pprint(data) 
    return data

def clean_label(label): 
    #set value to default
    value = label
    if '(' in label and ')' in label:
        #get the index of open parenthesis
        index = label.find('(')
        value = label[:index-1] #get rid of whitespace
 
    return value

def binominal_split(data): 
    output = data
    if data.startswith('{'):
        output = data[1:-1].split('|')
    return output

def update_db(data, db):
    # YOUR CODE HERE
    for key in data.keys():
        db.arachnid.update({'label' : key}, {'$set' : {'classification.binomialAuthority' : data[key]}})


def test():
    # Please change only the add_field and update_db functions!
    # Changes done to this function will not be taken into account
    # when doing a Test Run or Submit, they are just for your own reference
    # and as an example for running this code locally!
    
    data = add_field(DATAFILE, FIELDS)
    pprint.pprint(data)
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    update_db(data, db)

    updated = db.arachnid.find_one({'label': 'Opisthoncana'})
    
    assert updated['classification']['binomialAuthority'] == 'Embrik Strand'
    pprint.pprint(data)



if __name__ == "__main__":
    test()