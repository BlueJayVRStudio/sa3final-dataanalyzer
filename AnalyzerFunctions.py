#!/usr/bin/env python3

import requests
import json

# model for testing
class Artpieces:
    def __init__(self, id, name, image_id, dimensions_detail):
        self.id = id
        self.name = name
        self.image_id = image_id
        self.dimensions_detail = dimensions_detail

## ANALYSIS: analysis functions
class analysis_functions:
    ## ANALYSIS: returns API address for the thumbnail image given an art work id
    def get_iif(self, identifier):
        return f"https://www.artic.edu/iiif/2/{identifier}/full/843,/0/default.jpg"

    ## ANALYSIS: helper function
    def get_volume_string(self, detail):
        return str(detail['depth_cm'] * detail['width_cm'] * detail['height_cm'])

    ## ANALYSIS: helper function
    def get_area_string(self, detail):
        return str(detail['width_cm'] * detail['height_cm'])

    ## ANALYSIS: returns list of parts of the artwork and their calculated volumes or areas
    def get_dimensions_detail(self, details):
        # raise NotImplementedError
        toReturn = []
        for i in json.loads(details):
            # print(type(i['depth_cm'])) # it's int
            isVolume = True if i['depth_cm'] != 0 else False
            if isVolume:
                toReturn.append({ 'part_name': i['clarification'], 'processed' : "Volume: " + self.get_volume_string(i) + " cm^3" } )
            else:
                toReturn.append({ 'part_name': i['clarification'], 'processed' : "Area: " + self.get_area_string(i) + " cm^2" } )

        # print(type(toReturn))
        return toReturn

    ## ANALYSIS: data processing entry point
    def ArtpiecesJson(self, rows):
        tempList = []
        for i in rows:
            data = { 
                'id': i.id,
                'name': i.name,
                'image_link': self.get_iif(i.image_id),
                'dimensions_detail': self.get_dimensions_detail(i.dimensions_detail)
            }
            tempList.append(data)
        return json.dumps(tempList)

def delete_records(address):
    response = requests.get(address + "delete_records")
    # print(address)
    return response
