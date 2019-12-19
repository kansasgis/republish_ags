# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 2019

@author: Kristen Jordan Koenig- kristen@kgs.ku.edu
@purpose: This script publishes/republishes a geocoding service to ArcGIS Server
@details: This script was written in Python 3
"""

def republishGeocodingService():
    from arcpy import CreateGeocodeSDDraft
    from arcpy.server import StageService, UploadServiceDefinition

    # set up variables
    locator_path = r"C:\folder\myLocator.loc" # full path to locator to publish
    sddraft_file = r"C:\folder\myLocator.sddraft" # full path to sd draft file
    sd_file = r"C:\folder\myLocator.sd" # full path to sd file
    service_name = "myGeocodingService" # name of published geocoding service
    conn_file = r"C:\folder\arcgis on blah.blah.ags" # full path to ArcGIS server connection file

    # create service draft
    CreateGeocodeSDDraft(locator_path, sddraft_file, service_name,
                         "FROM_CONNECTION_FILE", conn_file, True, "",
                         overwrite_existing_service=True)

    # stage service
    StageService(sddraft_file, sd_file)

    # republish service
    UploadServiceDefinition(sd_file, conn_file)

    # report
    print("Published geocoding service.")
