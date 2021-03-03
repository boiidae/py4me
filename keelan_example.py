import zeep
import os
import sys
import csv
import datetime

cluster_controller_hostname = "192.168.0.24"  # Put the hostname of your cluster controller machine here. If you are running the script from the same machine you can put localhost
integration_port = "1063"                     # Leave this as default of 1063 unless you have changed the integration port
path_to_wsdl = "C:\\FVDBScanID_5_5_1\\etc\\FVDBScanID.wsdl"              # modify this to point to your WSDL file
integration_client = zeep.Client(path_to_wsdl)
integration_client_service = integration_client.create_service("{urn:cognitec.com/DBScanID/WS/2.4/XMLSchema/FVDBScanID.wsdl}FVDBScanID",
                                                               "http://{}:{}".format(cluster_controller_hostname, integration_port))

images = []

# Walk the selected directory to get all image files
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        if name.lower().endswith((".jpg",".jpeg",".png",".bmp",".tiff")):
            images.append(os.path.join(root, name))

# Set up the CSV file to write to
csv_file = open("{}_portrait_analysis.csv".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")), "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["File", "Age", "Gender", "Ethnicity"])

# Process the images
for image in images:
    with open(image, 'rb') as img:
        img_data = img.read()

    results = zeep.helpers.serialize_object(getattr(integration_client_service, "analyze-portrait")({"binaryImg": img_data}))
    age = results["featureSet"]["age"]
    gender = results["featureSet"]["gender"]
    ethnicity = results["featureSet"]["ethnicity"]
    print("Age: {}; Gender: {}; Ethnicity: {}".format(age, gender, ethnicity))

    # write the results to a CSV file
    csv_writer.writerow([image, age, gender, ethnicity])

csv_file.close(
