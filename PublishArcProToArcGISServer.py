# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 11:51:53 2019

@author: Kristen Jordan Koenig- kristen@kgs.ku.edu
@purpose: This script will loop through maps saved in one ArcPro project to publish
or republish as map services in ArcGIS Server
"""

from os.path import join, exists
from arcpy.mp import ArcGISProject
from arcpy.sharing import CreateSharingDraft
from arcpy.server import StageService, UploadServiceDefinition
from arcpy import Delete_management


def main():
    # set up maps to be updated
    prj_path = "" # full path to the ArcPro project
    map_list = ["", "", ""] # list maps in the project to be published
     
    # define variables
    sd_draft_path = "" # folder path on where to save the sd drafts
    conn_file = "" # full path to the ArcGIS Server connection file, will end in .ags
    server_folder = "" # if you're publishing services in a folder, put the folder name here
    
    # run the update
    results = updateNonHostedServices(prj_path, map_list, sd_draft_path, conn_file, server_folder)

    # print results
    print("Success: " + ", ".join(results[0]))
    if results[1] != []:
        print("Issues: " + ", ".join(results[1]))
          
        
def updateNonHostedServices(prj_path, map_list, sd_draft_path, conn_file, server_folder):

    # set ArcGIS Project
    aprx = ArcGISProject(prj_path)

    # set up for reporting
    successList = []
    failList = []

    # loop through maps in the list
    for map_name in map_list:
        m = aprx.listMaps(map_name)[0]
        
        out_sddraft = join(sd_draft_path, map_name + ".sddraft")
        
        # remove sd draft if it exists already
        if exists(out_sddraft):
            Delete_management(out_sddraft)
        
        # Create MapServiceDraft and set service properties
        service_draft = CreateSharingDraft("STANDALONE_SERVER", "MAP_SERVICE", map_name, m)
        service_draft.targetServer = conn_file
        service_draft.serverFolder = server_folder 
        service_draft.overwriteExistingService = True # toggle based on publishing/republishing
        
        try:
        
            # Create Service Definition Draft file
            service_draft.exportToSDDraft(out_sddraft)
            
            # Stage Service
            sd_filename = map_name + ".sd"
            sd_output_filename = join(sd_draft_path, sd_filename)
            
            # remove staged service if it exists
            if exists(sd_output_filename):
                Delete_management(sd_output_filename)
                
            # stage the serve
            StageService(out_sddraft, sd_output_filename)
            
            # Share to ArcGIS Server
            print("Uploading %s Service Definition..." % map_name)
            UploadServiceDefinition(sd_output_filename, conn_file, map_name, '', 
                                                 "FROM_SERVICE_DEFINITION", server_folder, "STARTED", 
                                                 "USE_DEFINITION", "NO_SHARE_ONLINE", "PRIVATE", 
                                                 "NO_SHARE_ORGANIZATION", None)
            
            successList.append(map_name)
            
            print("Successfully Uploaded service %s." % map_name)
            
        except Exception as e:
            # if there was an error, add what service failed and the error to the fail list
            failList.append(map_name + ": " + str(e))
            print("Failed publishing %s." % map_name)

    return [successList, failList]
    
if __name__ == '__main__':
    main()
