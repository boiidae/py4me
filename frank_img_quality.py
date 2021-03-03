#!/usr/bin/env python3
# coding=utf-8
import sys

try:
    import getopt
    import requests
    import urllib3
    import uuid
    import json
    import base64
except ImportError as e:
    print(e)
    print("This example needs python >=3.5 and following libraries : \" sys, getopt, requests, urllib3, uuid, json "
          "and base64 \" .Please install the required libraries using \"pip3/pip\"")
    sys.exit(1)
except Exception:
    print("This example needs python >=3.5 and following libraries : \" sys, getopt, requests, urllib3, uuid, json "
          "and base64 \" .Please install the required libraries using \"pip3/pip\"")
    sys.exit(1)

HTTP_200_OK = 200
HTTP_201_CREATED = 201
EYE_DISTANCE_MINIMUM = 59

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class bColors:
    SEPARATOR = "\033[95m"
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    IMAGEQUALITY = "\033[94m"
    DESCRIBE = "\033[97m"


def main(argv):
    """
       Example showing enrollment process

       Args:
       arg1: --id ... the client id needed for authentication
       arg2: --secret ... secret needed for authentication
       arg3: --hostname ...Hostname of CnC server
       arg4: --image ...complete path of image
       arg5: --video ...complete path of video
       arg6: --ssl ...If added, SSL verification will be performed
       """

    client_id = None
    client_secret = None
    cnc_hostname = None
    image_path = None
    video_path = None
    enable_ssl = False

    try:
        opts, args = getopt.getopt(argv, "i:s:p:v:o:", ["id=", "secret=", "image=", "video=", "hostname="])
    except getopt.GetoptError:
        print(bColors.BOLD + 'properties.py --id <Client Id needed for authentication > '
                             '--secret <Client Secret needed for authentication> '
                             '--hostname <Hostname of CnC server> --image <complete path of image> / '
                             '--video <complete path of video>'
                             ' [-ssl <If present, SSL verification will be performed> ] ')
        print(bColors.RESET + "")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("")
            print(bColors.BOLD + 'properties.py --id <Client Id needed for authentication > '
                                 '--secret <Client Secret needed for authentication> '
                                 '--hostname <Hostname of CnC server> --image <complete path of image> / '
                                 '--video <complete path of video>'
                                 ' [-ssl <If present, SSL verification will be performed> ] ')
            print(bColors.RESET + "")
            sys.exit(2)
        elif opt in ("-i", "--id"):
            client_id = arg
        elif opt in ("-s", "--secret"):
            client_secret = arg
        elif opt in ("-p", "--image"):
            image_path = arg
        elif opt in ("-v", "--video"):
            video_path = arg
        elif opt in ("-o", "--hostname"):
            cnc_hostname = arg
        elif opt == "-ssl":
            enable_ssl = True

    if cnc_hostname is None:
        print("")
        print(bColors.BOLD + 'properties.py --id <Client Id> --secret <Client Secret> --hostname <CnC HostName> '
                             '--image <Image Path> / --video <Video Path> [-ssl <Enable SSL Verification] ')
        print("Please provide hostname of Command & Control Server.")
        print(bColors.RESET + "")
        sys.exit(2)

    if client_id is None or client_secret is None:
        print("")
        print(bColors.BOLD + 'properties.py --id <Client Id> --secret <Client Secret> --hostname <CnC HostName> '
                             '--image <Image Path> / --video <Video Path> [-ssl <Enable SSL Verification] ')
        print("Please provide Client-Id and Client-Secret. You can find them on CnC server under etc folder")
        print(bColors.RESET + "")
        sys.exit(2)

    if image_path is None and video_path is None:
        print("")
        print(bColors.BOLD + 'properties.py --id <Client Id> --secret <Client Secret> --hostname <CnC HostName> '
                             '--image <Image Path> / --video <Video Path> [-ssl <Enable SSL Verification] ')
        print("Please provide image/video that you want to enroll")
        print(bColors.RESET + "")
        sys.exit(2)

    cnc_url = "https://" + cnc_hostname


    request_payload = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}
    token_url = cnc_url + "/token/"

    print(bColors.SEPARATOR + "*************************************************************************")
    print("")

    try:
        response = requests.post(token_url, data=request_payload, verify=enable_ssl)
    except requests.exceptions.RequestException:
        print("")
        print(bColors.FAIL + "   Command And Control Server is not reachable ")
        print(bColors.RESET + "")
        sys.exit(1)
    except Exception as e:
        print("")
        print(bColors.FAIL + "   Command And Control Server is not reachable : " + str(e))
        print(bColors.SEPARATOR + "*************************************************************************")
        print(bColors.RESET + "")
        sys.exit(1)

    if response.status_code is not HTTP_200_OK:
        print("")
        print(bColors.FAIL + "   Command And Control Server is reachable but Authentication failed")
        print(bColors.SEPARATOR + "*************************************************************************")
        print(bColors.RESET + "")
        sys.exit(1)

    print(bColors.OKGREEN + "   - Command And Control Server is reachable")

    token = response.json()['access_token']

    print("   - The access token was created: " + bColors.BOLD + token)

    print(bColors.RESET + "")

    print(bColors.SEPARATOR   + "")

    # Edits portrait characteristics
    print(bColors.SEPARATOR + "* ABOUT TO TRY  ************")

    properties_url = cnc_url + "/portrait-assessment/"
    header = {'Authorization': 'Bearer ' + token}

    print(bColors.SEPARATOR + "* Build header  ************")
    files = {'portrait': open(image_path, 'rb')}
    try:
        response = requests.post(properties_url, headers=header, files=files, verify=enable_ssl)
    except Exception as e:
        print("")
        print(bColors.FAIL + "   Error Getting Port Characteristics" + str(e))
        print(bColors.SEPARATOR + "*************************************************************************")
        print(bColors.RESET + "")
        sys.exit(1)

    print(bColors.SEPARATOR   + "* STATUS CODE:  "  + str(response.status_code))

    print(bColors.SEPARATOR)

    print(bColors.IMAGEQUALITY + bColors.BOLD + "*** Frank's Technical Image Quality Check ***")

    print(bColors.RESET + "")

    eye_distance = str((response.json()['characteristics'])['eye_distance'])

    print(bColors.IMAGEQUALITY + " 1) Eye distance in pixels: " + bColors.BOLD + eye_distance)
    if float(eye_distance) < float(EYE_DISTANCE_MINIMUM):
        print(bColors.FAIL + bColors.BOLD + "    Insufficient pixel distance between the center of the eyes")
        #sys.exit(1)

    print(bColors.RESET + "")

    is_frontal_best_practice = str((response.json()['iso_compliance'])['is_frontal_best_practice'])

    print(bColors.IMAGEQUALITY + " 2) The face is frontal: " + bColors.BOLD + is_frontal_best_practice)
    if str(is_frontal_best_practice) is not 'True':
        print(bColors.FAIL + "    The face is not sufficiently frontal for an enrollment")
        #sys.exit(1)

    print(bColors.RESET + "")

    is_sharp = str((response.json()['iso_compliance'])['is_sharp'])

    print(bColors.IMAGEQUALITY + " 3) The image is sharp with sufficient focus and depth of field: " + bColors.BOLD + is_sharp)
    if str(is_sharp) is not 'True':
        print(bColors.FAIL + "    The face is not in focus")
        #sys.exit(1)

    print(bColors.RESET + "")

    good_gray_scale_profile = str((response.json()['iso_compliance'])['good_gray_scale_profile'])

    print(bColors.IMAGEQUALITY + " 4) The image has a good gray scale profile: " + bColors.BOLD + good_gray_scale_profile)
    if str(good_gray_scale_profile) is not 'True':
        print(bColors.FAIL + "    Inconsistent lighting of the face area")
        #sys.exit(1)

    print(bColors.SEPARATOR)

    print(bColors.RESET + "")

    # End of inserted test code

    create_case_url = cnc_url + "/cases/"
    header = {'Authorization': 'Bearer ' + token}
    try:
        response = requests.post(create_case_url, headers=header, verify=enable_ssl)
    except Exception as e:
        print("")
        print(bColors.FAIL + "   Error creating Case" + str(e))
        print(bColors.SEPARATOR + "*************************************************************************")
        print(bColors.RESET + "")
        sys.exit(1)

    if response.status_code is not HTTP_201_CREATED:
        print("")
        print(bColors.FAIL + "   Case creation failed")
        print(bColors.SEPARATOR + "*************************************************************************")
        print(bColors.RESET + "")
        sys.exit(1)

    print(bColors.SEPARATOR   + "* STATUS CODE IN CASE SECTION:  " + str(response.status_code))

    print(bColors.SEPARATOR   + "")

    case_id = response.json()['id']
    print(bColors.OKGREEN + "   - Case created with Id \"" + str(case_id) + "\"")


    add_portrait_url = cnc_url + '/cases/' + str(case_id) + "/portraits/"


    if video_path is not None and image_path is None:
        video_analysis_url = cnc_url + '/video-assessment/'
        try:
            video_file = {'video': open(video_path, 'rb')}
            form_data = {"include_frames_with_multiple_faces": True}
            response = requests.post(video_analysis_url, headers=header, files=video_file, data=form_data, verify=enable_ssl)
            response_dict = response.json()
            error = response_dict['error']
            if len(error):
                print(bColors.FAIL + "  Video analysis failed: " + str(response.json['error']))
                print(bColors.SEPARATOR + "*************************************************************************")
                print(bColors.RESET + "")
                sys.exit(1)

            result_array = response_dict['results']
            if len(result_array):
                files = {'portrait': base64.b64decode(result_array[0]['portrait'])}
            else:
                print("")
                print(bColors.FAIL + "  No image received from DBScanID")
                print(bColors.SEPARATOR + "*************************************************************************")
                print(bColors.RESET + "")
                sys.exit(1)

        except Exception as e:
            print("")
            print(bColors.FAIL + "  Video analysis failed . ERROR : " + str(e))
            print(bColors.SEPARATOR + "*************************************************************************")
            print(bColors.RESET + "")
            sys.exit(1)

    else:
        try:
            files = {'portrait': open(image_path, 'rb')}
        except Exception as e:
            print("")
            print(bColors.FAIL + "  Error reading image . ERROR : " + str(e))
            print(bColors.SEPARATOR + "*************************************************************************")
            print(bColors.RESET + "")
            sys.exit(1)

    try:
        response = requests.post(add_portrait_url, headers=header, files=files, verify=enable_ssl)
    except Exception as e:
        print("")
        print(bColors.FAIL + "  Portrait could not be added to case with Id \"" + str(case_id) +
              "\" . ERROR : " + str(e))
        print(bColors.SEPARATOR + "*************************************************************************")
        print(bColors.RESET + "")
        sys.exit(1)

    if response.status_code is not HTTP_201_CREATED:
        print("")
        print("   Portrait " + str(image_path) + " could not be added to case with Id \"" + str(case_id)) + "\" "
        print(bColors.FAIL + bColors.SEPARATOR +
              "*************************************************************************")
        print(bColors.RESET + "")
        sys.exit(1)

    print(bColors.SEPARATOR)

    print(bColors.OKGREEN + "   - Added Portrait with id \"" + str(response.json()['portrait_id']) +
          "\" to Case with Id \"" + str(case_id) + "\" ")

    enrollment_url = cnc_url + "/cases/" + str(case_id) + "/enrollment/"

    request_payload = {"Name": "ENROLL-TEST"}

    try:
        response = requests.post(enrollment_url, headers=header, data=request_payload, verify=enable_ssl)
    except Exception as e:
        print("")
        print(bColors.FAIL + "  Enrollment failed for case with Id \"" + str(case_id) + "\" . ERROR : " + str(e))
        print(bColors.SEPARATOR + "*************************************************************************")
        print(bColors.RESET + "")
        sys.exit(1)

    if response.status_code is not HTTP_200_OK:
        print("")
        print(bColors.FAIL + "   Enrollment failed for case with Id \"" + str(case_id) + "\" ")
        print(bColors.SEPARATOR + "*************************************************************************")
        sys.exit(1)

    print(bColors.SEPARATOR)

    print(bColors.OKGREEN + "   - Case (" + str(case_id) + ") Enrolled")

    print("")
    print(bColors.SEPARATOR + "*************************************************************************")
    print(bColors.RESET + "")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        print(e)
