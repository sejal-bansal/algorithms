import os
import shutil
import sqlite3
import requests
import subprocess
import zipfile
import pathlib
from os.path import basename
import json
import numpy as np
from scipy.io import loadmat
from copy import deepcopy
import sys, traceback
import logging
from predictor import predict
from xml.etree import ElementTree
import stat


'''
    Steps
    ----------------------
    a. Call the api
    b. Get n number of jobs
    c. For each job in parallel processing
        a. Download the image file for secondary image generation
        b. Generate secondary images
        c. Copy rp0 file to datapool
        d. Do Correlation Analysis between the rp0 file and the pool
        e. zip all the files
        f. Call the api and upload the zip file
'''


user, passwd = 'admin', '@dmin123#'
host = 'https://dyslexia.computing.clemson.edu/'
single_correlation_value = 0
multiple_correlation_value = 0

# host = 'http://localhost:8001/'
# user, passwd = 'roshan2', 'roshan123'

def get_jobs():
    endpoint = 'api/jobs'
    response = requests.get(host + endpoint, auth=(user, passwd), verify=False)
    jobs = response.json()
    return jobs

def get_email(username):
    endpoint = 'emailapi/'
    response = requests.post(host + endpoint, data = {'user':username}, auth=(user, passwd),verify=False)

    return JsonResponse(


def update_job_status(id, status, processing_step_no):
    endpoint = 'dataset/status/{}'.format(id)
    response = requests.post(
        host + endpoint, auth=(user, passwd),
        data={'status': status, 'processing_step_no': processing_step_no},
        verify=False
    )
    try:
        print(response.json())
    except:
        print(response.text)

def create_directory(directory):
    try:
        os.makedirs(directory)
    except Exception as e:
        # print(str(e))
        pass

def download_file(url, directory, job, processing_step_no):
    image_name = job['brain_file']
    logging.debug("job:: %s",job)
    r = requests.get(url, auth=(user, passwd), verify=False)
    with open(directory +'/' + image_name, 'wb') as f:
        f.write(r.content)

    print ("Successfully Downloaded: ", image_name)
    print("In directory: ", directory)
    update_job_status(job['id'], 'Dataset downloaded successfully.', processing_step_no)

def zip_dir(path, name, job, processing_step_no):

    # Create 'path\to\zip_file.zip'
    shutil.make_archive(path, 'zip', name)

    update_job_status(
        job['id'],
        'Uploading secondary dataset zip file to the dyslexia server.',
        processing_step_no
    )

def copy_all_scripts_to_user_directory(destination):
    command = 'cp -r CAT12* {}'.format(destination)
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    # This makes the wait possible
    p_status = p.wait()

def copy_rp_file_to_pool(source, pool="correlationdatapool/"):
    command = 'cp {}/mri/rp1* {}'.format(source, pool)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    # This makes the wait possible
    p_status = p.wait()


def process_brain_volume_using_ofc__and_sts_mask_and_save_results(directory, job, processing_step_no):
    endpoint = 'correlation'
    files = os.listdir(directory + "/mri")
    files_1 = os.listdir(directory + "/report")

    wpo_name = ''
    for each_file in files:
        if 'mwp1' in each_file:
            wpo_name = each_file
            break


    with open(directory + '/maskImages.txt', 'w') as file:
        file.write(directory + "/mri/"+ wpo_name +"\n")

    with open(directory + '/smwp1Images.txt', 'w') as file:
        file.write(directory + "/mri/s"+ wpo_name +"\n")

    command = 'cp -r smooth* {} && cp -r mask* {} && cd {} && matlab -r "smooth" && matlab -r "mask_ofc" && matlab -r "mask_sts"'.format(
        directory, directory, directory
    )
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    # This makes the wait possible
    p_status = p.wait()

    for each_file in files_1:
        if each_file.endswith('.xml'):
            file_name_for_xml = each_file

    tree = ElementTree.parse(directory + "/report/" + file_name_for_xml)
    root = tree.getroot()
    count = 0
    inner_count = 0
    outer_count = 0
    subject_measures_tag_volume_data = []
    tiv_volume = []
    for child in root:
        if child.tag == 'subjectmeasures':
            for sub_child in child:
                if sub_child.tag == 'vol_abs_CGW':
                    subject_measures_tag_volume_data = root[outer_count][inner_count].text
                if sub_child.tag == 'vol_TIV':
                    tiv_volume = root[outer_count][inner_count].text
                else:
                    inner_count += 1

        else:
            outer_count +=1

    occurrence = 3
    val = -1
    volume_values_data = []
    for i in range(0, occurrence):
        logging.debug(subject_measures_tag_volume_data)
        if len(subject_measures_tag_volume_data) == 0:
            with open(directory + '/readme.txt', 'w') as f:
                f.write(job['brain_file'])
        else:
            val = subject_measures_tag_volume_data.find(" ", val + 1)
            volume_values_data.append(val)

    index_1 = volume_values_data[0]
    index_2 = volume_values_data[1]
    index_3 = volume_values_data[2]

    count = 0
    value_csf = []
    value_gm = []
    value_vm = []
    second_value = subject_measures_tag_volume_data[index_1:index_2]
    third_value = subject_measures_tag_volume_data[index_2:index_3]

    for i in subject_measures_tag_volume_data:
        count += 1
        if i == '[':
            pass
        elif i == '\n':
            pass
        elif i == ']':
            pass
        else:
            value_csf.append(i)

        if count == index_1:
            break

    count = 0
    for i in second_value:
        count += 1
        if i == '[':
            pass
        elif i == '\n':
            pass
        elif i == ']':
            pass
        else:
            value_gm.append(i)

        if count == index_2:
            break

    count = 0
    for i in third_value:
        count += 1
        if i == '[':
            pass
        elif i == '\n':
            pass
        elif i == ']':
            pass
        else:
            value_vm.append(i)

        if count == index_3:
            break

    total_gm_value = round(float(''.join(map(str,value_gm))),2)
    total_vm_value = round(float(''.join(map(str,value_vm))),2)
    total_csf_value = round(float(''.join(map(str,value_csf))),2)

    f_gm = open(directory + "/" + "total_gm_volume.txt", "w")
    f_gm.write(str(total_gm_value))
    f_gm.close()

    f_vm = open(directory + "/" + "total_vm_volume.txt", "w")
    f_vm.write(str(total_vm_value))
    f_vm.close()

    f_csf = open(directory + "/" + "total_csf_volume.txt", "w")
    f_csf.write(str(total_csf_value))
    f_csf.close()


    for each_file in files_1:
        if each_file.endswith('.txt'):
            file_name_for_txt = each_file

    path_for_text_file = directory + "/report/" + file_name_for_txt

    with open(path_for_text_file) as temp_f:
        datafile = temp_f.readlines()
        string_line = ' '
        for line in datafile:
            if 'Image Quality Rating (IQR):' in line:
                string_line = line

    IQR_value = string_line[29:34]

    f_iqr = open(directory + "/" + "IQR.txt", "w")
    f_iqr.write(str(IQR_value))
    f_iqr.close()

    with open(path_for_text_file) as temp_f:
        datafile = temp_f.readlines()
        string_value = ' '
        for line in datafile:
            if 'Average thickness:' in line:
                string_value = line

    avg_cortical_thickness_value = string_value[41:]

    f_avg = open(directory + "/" + "avg_cortical_thickness_value.txt", "w")
    f_avg.write(str(avg_cortical_thickness_value))
    f_avg.close()


    # Read the volumes
    with open(directory + '/STSVol.txt') as f:
        sts_volume = f.readline()

    with open(directory + '/OFCVol.txt') as f:
        ofc_volume = f.readline()

    with open(directory + '/total_gm_volume.txt') as f:
        total_gm_volume = f.readline()

    with open(directory + '/total_vm_volume.txt') as f:
        total_wm_volume = f.readline()

    with open(directory + '/total_csf_volume.txt') as f:
        total_csf_volume = f.readline()

    with open(directory + '/IQR.txt') as f:
        iqr_value = f.readline()

    with open(directory + '/sc.txt') as f:
        mni_value = f.readline()

    with open(directory + '/avg_cortical_thickness_value.txt') as f:
        avg_cortical_thickness = f.readline()

    with open(directory + '/mc_max_to.txt') as f:
        mc_max_to = f.readline()


    with open(directory + '/mc.txt') as f:
        mc = f.readline()

    with open(directory + '/niiNames.txt') as f:
        image_id = f.readline()

    data_dict = {
        'type': 'mask',
        'id': job['id'],
        'ofc_volume': ofc_volume.replace('\n',''),
        'sts_volume': sts_volume.replace('\n',''),
        'total_csf_volume':total_csf_volume.replace('\n',''),
        'total_gm_volume': total_gm_volume.replace('\n',''),
        'total_wm_volume': total_wm_volume.replace('\n',''),
        'iqr_value':iqr_value.replace('\n',''),
        'mni_value':mni_value.replace('\n',''),
        'mc':mc.replace('\n',''),
        'average_cortical_thickness':avg_cortical_thickness.replace('\n',''),
        'mc_max_to':mc_max_to.replace('\n',''),
        'image_name':image_id.replace('\n','')
    }


    # using jobid send update to the server
    r = requests.post(host + endpoint,  auth=(user, passwd), data=json.dumps(data_dict), verify=False)
    print(r.text)
    update_job_status(
        job['id'],
        'Successfully completed estimating brain volume for the subject.',
        processing_step_no
    )


def perform_correlation_analysis_with_wp1_pool_and_save_results(directory):
    files = os.listdir(directory + "/mri")
    wpo_name = ''
    for each_file in files:
        if 'mwp1' in each_file:
            wpo_name = each_file
            break

    with open(directory + '/rp1Names.txt', 'w') as file:
        file.write(directory + "/mri/"+ wpo_name +",1\n")
        file.write("/home/sejalb/CPSC8910-DyslexiaDataConsortium/spm12/toolbox/cat12/templates_volumes/Template_6_IXI555_MNI152.nii,1\n")

    command = 'cd {} && matlab -r "CAT12_QC"'.format(directory)
    logging.debug('Executing Command: ' + command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    # This makes the wait possible
    p_status = p.wait()

def perform_correlation_analysis_with_rp1_pool_and_save_results(directory):
    files = os.listdir("correlationdatapool")
    with open(directory + '/rp1Names.txt', 'w') as file:
        for each_file in files:
            file.write("../correlationdatapool/"+each_file +"\n")
            file.write("../correlationdatapool/"+each_file +"\n")

    command = 'cd {} && matlab -r "CAT12_QC"'.format(directory)
    logging.debug('Executing Command: ' + command)
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    # This makes the wait possible
    p_status = p.wait()

def process_correlation_matfile_get_correlation(location, type, jobid, processing_step_no):
    endpoint = 'correlation'
    mat = loadmat(location + '/YpY.mat')  # load mat-file
    mdata = mat['YpY']  # variable in mat file

    data_dict = {'type': type}
    n_files = len(mat['job'][0][0][0][0][0])

    for i in range(0, n_files):
        first_file_name = mat['job'][0][0][0][0][0][i][0][0]
        first_file_name = first_file_name.replace('/home/sejalb/CPSC8910-DyslexiaDataConsortium/user__admin__job__{}/mri/'.format(jobid), '')
        first_file_name = first_file_name.replace('/home/sejalb/CPSC8910-DyslexiaDataConsortium/spm12/toolbox/cat12/templates_volumes/', '')

        for j in range(0, n_files):
            second_file_name = mat['job'][0][0][0][0][0][j][0][0]

            second_file_name = second_file_name.replace('/home/sejalb/CPSC8910-DyslexiaDataConsortium/user__admin__job__{}/mri/'.format(jobid), '')
            second_file_name = second_file_name.replace('/home/sejalb/CPSC8910-DyslexiaDataConsortium/spm12/toolbox/cat12/templates_volumes/', '')

            if 'mwp1' in first_file_name and 'mwp1' not in second_file_name:
                corr_coefficient = mdata[i][j]
                data_dict['from'] = first_file_name.replace('mmwp1', '')
                data_dict['correlation'] =  corr_coefficient

    logging.debug("single_correlation:: %s", data_dict)
    for key,value in data_dict.items():
        if key == 'correlation':
            single_correlation_value = round(value,2)
            sc_iqr = open(location + "/" + "sc.txt", "w")
            sc_iqr.write(str(single_correlation_value))
            sc_iqr.close()


    # using jobid send update to the server
    r = requests.post(host + endpoint,  auth=(user, passwd), data=json.dumps(data_dict), verify=False)
    print("Line 189:: ", r.text)
    update_job_status(
        jobid,
        'Successfully completed calculating correlation of mwp1 and template image.',
        processing_step_no
    )

def process_correlation_matfile_get_max_correlation(location, type, jobid, processing_step_no):
    endpoint = 'correlation'
    mat = loadmat(location + '/YpY.mat')  # load mat-file
    mdata = mat['YpY']  # variable in mat file

    data = []
    n_files = len(mat['job'][0][0][0][0][0])

    for i in range(0, n_files):
        max_file_name = None
        max_correlation = None

        first_file_name = mat['job'][0][0][0][0][0][i][0][0]
        first_file_name = first_file_name.replace('', '')
        first_file_name = first_file_name.replace('/home/sejalb/CPSC8910-DyslexiaDataConsortium/spm12/toolbox/cat12/templates_volumes/', '')
        first_file_name = first_file_name.replace('/home/sejalb/CPSC8910-DyslexiaDataConsortium/correlationdatapool/','')
        for j in range(0, n_files):
            second_file_name = mat['job'][0][0][0][0][0][j][0][0]
            second_file_name = second_file_name.replace('', '')
            second_file_name = second_file_name.replace('/home/sejalb/CPSC8910-DyslexiaDataConsortium/spm12/toolbox/cat12/templates_volumes/', '')
            second_file_name = second_file_name.replace('/home/sejalb/CPSC8910-DyslexiaDataConsortium/correlationdatapool/','')
            if (second_file_name != first_file_name) and (max_correlation is None or mdata[i][j] > max_correlation):
                max_correlation = mdata[i][j]
                max_file_name = second_file_name

        data_dict = {
            'from': first_file_name,
            'max_to': max_file_name,
            'max_correlation': max_correlation
        }


        if data_dict not in data:
            data.append(data_dict)

    job_number = str(jobid)
    logging.debug("job_number:: %s",job_number)
    from_value = []

    for i in data:
        for key,value in i.items():
            if key == 'from':
                vp = value.split('/')[-1]
                if job_number == vp[9:13]:
                    from_value.append(i)

    logging.debug("from_value:: %s",from_value)
    for i in from_value:

        for key,values in i.items():

            if key == 'from':
                multiple_correlation_from = values.split('/')[-1]
                mc_from = open(location + "/" + "mc_from.txt", "w")
                mc_from.write(str(multiple_correlation_from))
                mc_from.close()

            elif key == 'max_to':
                multiple_correlation_max_to = values.split('/')[-1]
                mc_max = open(location + "/" + "mc_max_to.txt", "w")
                mc_max.write(str(multiple_correlation_max_to))
                mc_max.close()

                source = '/home/sejalb/palmetto-dyslexia/CPSC8910-DyslexiaDataConsortium/correlationdatapool/' + str(multiple_correlation_max_to)
                logging.debug('Source :: %s',source)
                dest = location + '/'
                logging.debug('Dest:: %s',dest)
                com = 'cd {} && mkdir correlated_image'.format(dest)
                g = subprocess.Popen(com,shell=True)
                destination = dest + 'correlated_image'
                logging.debug('Destination :: %s',destination)

                command = 'cd {} && cp -r {} {}'.format(dest,source,destination)
                p = subprocess.Popen(command,shell = True)
                stdout, stderr = p.communicate()

            else:
                multiple_correlation_value = round(values,2)
                mc_iqr = open(location + "/" + "mc.txt", "w")
                mc_iqr.write(str(multiple_correlation_value))
                mc_iqr.close()


    #logging.debug("Multiple Correlation:: %s", data)
    # using jobid send update to the server
    r = requests.post(host + endpoint,  auth=(user, passwd), data=json.dumps({'correlation_data': data, 'type': type}), verify=False)
    update_job_status(
        jobid,
        'Successfully completed calculating correlation of mwp1 and template image.',
        processing_step_no
    )

def generate_secondary_dataset(directory, job, processing_step_no):
    update_job_status(job['id'], 'Calling matlab base code for image generation.', processing_step_no)
    # # Step 3: Run the job for secondary image generation
    command = 'cd {} && matlab -nodisplay -nodesktop -r "CAT12_seg_batch"'.format(directory)
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #This makes the wait possible
    p_status = p.wait()

    # Update job status
    update_job_status(job['id'], 'Secondary datasets generated successfully.', processing_step_no)

def create_nii_images_file(directory, job, processing_step_no):
    current_wd = os.getcwd()
    image_list_file = directory + '/niiNames.txt'
    with open(image_list_file, 'w') as file:
        image_file_name = job['brain_file']
        file.write(image_file_name + '\n')

    image_path = directory + "/" + job['brain_file']
    final_list = []
    command = 'cd {} && mkdir bse_files'.format(directory)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    command = 'cd {} && cd bse_files && mkdir generated_images'.format(directory)
    p = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    output_image = job['brain_file'].split('.')[0] + 'nan.nii'

    command = 'cd {} && fslmaths {} -nan {}'.format(directory,job['brain_file'],output_image)
    p = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    points = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    # static_path = '/home/sejalb/palmetto-dyslexia/CPSC8910-DyslexiaDataConsortium'
    for x in points:
        path_for_shell = 'bet' + " " + directory +'/'+ output_image + " " + directory + '/bse_files/' + output_image + "_" + str(x) +" " + '-f' + " " + str(x)
        final_list.append(path_for_shell)

    MyFile=open(directory + '/shell_script.sh','w')
    MyFile.write('#!/bin/sh')
    MyFile.write('\n')
    for element in final_list:
        MyFile.write(element)
        MyFile.write('\n')
    MyFile.write('exit 101')
    MyFile.close()

    setts = image_path.split('/')[5]
    sett = ''.join(setts)
    lop = os.getcwd()

    os.chdir(lop + '/' + sett)
    x = os.listdir()
    index = 0
    for i in range(len(x)):
        if x[i] == 'shell_script.sh':
            index = i

    filename = x[index]
    os.chmod(filename, 509)

    # fsl_path = '/home/sejalb/fsl2'
    # command = 'cd && cd {} && ./fsl_setup.sh'.format(fsl_path)
    # logging.debug(command)
    # p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    # (output, err) = p.communicate()
    # p_status = p.wait()

    try:
        command = 'cd && cd {} && sh shell_script.sh'.format(directory)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
    except:
        logging.debug("The shell script is not getting executed")

    os.chdir(current_wd)

    update_job_status(job['id'], 'Successfully created nii images.', processing_step_no)

def upload_files_to_the_server(username, job, processing_step_no):
    endpoint = 'dataset/updownbyid/' + str(job['id'])
    files = {'file': open('user__' + username + '__job__' + str(job['id']) + '.zip','rb')}
    r = requests.post(host + endpoint, files=files, auth=(user, passwd), verify=False)

    # Update job status
    update_job_status(
        job['id'],
        'Successfully uploaded generated secondary files to the server.',
        processing_step_no
    )

def process_xml_files(job, processing_step_no):
    endpoint = 'dataset/processxml/' + str(job['id'])
    r = requests.post(host + endpoint, data=json.dumps({'type':'load_xml'}), auth=(user, passwd), verify=False)

    # Update job status
    update_job_status(
        job['id'],
        'Successfully completed generation of secondary images.',
        processing_step_no)

def find_brain_and_face_scores(host, directory, job, processing_step_no):
    endpoint = host + 'updateprediction/' + str(job['id'])
    value = 1
    check = False
    scores = predict(directory,job['brain_file'],directory + '/',value, check)

    print(scores)
    print(endpoint)
    r = requests.post(endpoint, data=scores, auth=(user, passwd), verify=False)

    # Update job status
    update_job_status(
        job['id'],
        'Successfully calculated brain score and face score for the dataset.',
        processing_step_no)

def create_working_directory(job):
    # Step 2: Create a user directory to store files
    username, job_id = job['user']['username'], job['id']
    path = str(pathlib.Path(__file__).parent.absolute())
    directory = path + '/' + 'user__' + username + '__job__' + str(job_id)
    create_directory(directory)
    update_job_status(job['id'], 'Completed creating working directory.', 0)
    return path, directory

def run_one_job(job, path, directory):
    logging.debug("i am at 636")
    logging.debug(job)
    username, job_id = job['user']['username'], job['id']
    logging.debug('Started Downloading FIle from API ... ')
    processing_step_no = job['processing_step_no']

    if str(processing_step_no) == '0':
        # Step 3: Download the file for further processing
        endpoint = 'dataset/updownbyid/' + str(job['id'])
        download_file(host + endpoint, directory, job, processing_step_no)
        logging.debug('Downloading FIle from API completed. ')

        logging.debug('Started predicting brain and face scores ... ')
        find_brain_and_face_scores(host, directory, job, processing_step_no)
        logging.debug('Successfully completed generating brain and face scores. ')
        processing_step_no = '1'

    logging.debug('Started Creating NII images ... ')
    if str(processing_step_no) == '1':
        # Write the names of the files to the directory
        create_nii_images_file(directory, job, processing_step_no)

        logging.debug('Completed Creating nii image.')
        processing_step_no = '2'

    if str(processing_step_no) == '2':
        logging.debug('Creating coorelation data pool...')
        # New Steps
        # 1. Create /home/correlationdatapool
        create_directory("correlationdatapool")
        logging.debug('Completed creating coorelation data pool..')
        processing_step_no = '3'

    if str(processing_step_no) == '3':
        logging.debug('Copying files to the correlationdatapool for analysis..')
        # 2. Copy all the scripts to user directory
        copy_all_scripts_to_user_directory(directory)
        logging.debug('Completed copying files to the correlationdatapool for analysis..')
        processing_step_no = '4'

    logging.debug('Generating secondary dataset...')
    if str(processing_step_no) == '4':
        # 3. Run the dataset generation
        generate_secondary_dataset(directory, job, processing_step_no)
        logging.debug('Completed generating secondary dataset..')
        processing_step_no = '5'

    if str(processing_step_no) == '5':
        # 4. Copy the rp0 file to the datapool
        copy_rp_file_to_pool(directory)
        logging.debug('Completed copying rp file to the pool..')
        processing_step_no = '6'

    if str(processing_step_no) == '6':
        try:
            # 5. Perform Correlation analysis with wp0 and process the YpY file
            perform_correlation_analysis_with_wp1_pool_and_save_results(directory)
            process_correlation_matfile_get_correlation(directory, 'single_correlation', job['id'], processing_step_no)
            logging.debug('Completed performing correlation with wp1 pool..')
            processing_step_no = '7'
        except Exception as e:
            logging.debug("Exception occurred while calculating correlation with wp1")
            logging.exception('Ignoring exception occurred while calculating correlation with wp1 and moving ....')

    if str(processing_step_no) == '7':
        try:
            # 6. Perform Correlation analysis with the rp1 pool and process the YpY file
            perform_correlation_analysis_with_rp1_pool_and_save_results(directory)
            process_correlation_matfile_get_max_correlation (directory, 'multiple_correlation', job['id'], processing_step_no)
            logging.debug('Completed performing correlation with rp1 pool..')
            processing_step_no = '8'
        except Exception as e:
            logging.debug("Exception occurred while calculating correlation with rp1")
            logging.exception('Ignoring exception occurred while calculating correlation and moving....')

    if str(processing_step_no) == '8':
        try:
            process_brain_volume_using_ofc__and_sts_mask_and_save_results(directory, job, processing_step_no)
            logging.debug('Completed performing brain volume estimation ..')
            import glob

            files = glob.glob(directory + '/bse_files/*.nii.gz')
            probs = []

            for i in range(11):
                source = files[i].split('/')[:7]
                source = '/'.join(source)
                logging.debug(source)

                filename = files[i].split('/')[-1]
                logging.debug(filename)

                dest = files[i].split('/')[:7]
                dest = '/'.join(dest)
                dest = dest + '/generated_images'
                logging.debug(dest)

                face , brain = predict(source,filename,dest,i,check=True)
                probs.append([face,brain])

            f = open(directory + '/probabilities.txt', 'w')
            for element in probs:
                f.write(str(element[0][0]))
                f.write('\n')
                f.write(str(element[1][0]))
                f.write('\n')

            processing_step_no = '9'

        except Exception as e:
            logging.debug("Exception occurred while estimating brain volume!!!!!")
            logging.exception('Ignoring brain volume estimation and moving ....')

    if str(processing_step_no) == '9':
        # Once job completes script terminates so on the script at the end
        # Step 7: Call Python Script to zip the output files in user directory
        zip_dir(directory, 'user__' + username + '__job__' + str(job_id), job, processing_step_no)
        logging.debug('Completed zipping output files..')
        processing_step_no = '10'

    if str(processing_step_no) == '10':
        # Step 8: Upload the zip file back to the server
        upload_files_to_the_server(username, job, processing_step_no)
        logging.debug('Completed uploading output files to dyslexia..')
        processing_step_no = '11'

    if processing_step_no == '11':
        process_xml_files(job, processing_step_no)
        logging.debug('Completed loading xml files to database.')

    #         logging.debug('Successfully completed prcessing job' + str(job['id']) + '.')
    #         logging.debug("starting copying")
    #         pool = 'user__' + username + '__job__' + str(job['id'])
    #         source = 'palmetto-dyslexia/CPSC8910-DyslexiaDataConsortium/' + 'user__' + username + '__job__' + str(job['id'])
    #         dest = '/scratch1/sejalb'
    #         command = 'cd && cp -R {} {}'.format(source,dest)
    #         p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #         (output, err) = p.communicate()
    #         # This makes the wait possible
    #         p_status = p.wait()
    #         logging.debug("copying completed")


    #         zip_filename = 'user__' + username + '__job__' + str(job['id']) + '.zip'
    #         logging.debug(zip_filename)

    #         command = 'cd && rm -rf ./{}'.format(source)
    #         p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #         (output, err) = p.communicate()
    #         # This makes the wait possible
    #         p_status = p.wait()


    #         logging.debug("File starting to delete ....")
    #         command = 'cd && rm -rf ./{}'.format('palmetto-dyslexia/CPSC8910-DyslexiaDataConsortium/' + zip_filename)
    #         p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #         (output, err) = p.communicate()
    #         # This makes the wait possible
    #         p_status = p.wait()
    #         logging.debug("Files deleted")


    logging.debug('Successfully completed prcessing job' + str(job['id']) + '.')
    return processing_step_no

def run():
    # Step 1: Get Jobs
    jobs = get_jobs()

    if len(jobs) > 0:
        job = jobs[0]
        username = job['user']['username']
        processing_step_no = 0
        try:
            path, directory = create_working_directory(job)
            print("Created:: ", path, directory)
            LOG_FILENAME = directory + '/log.txt'
            logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

            logging.debug('Created working directory')
            logging.debug(len(jobs))
            processing_step_no = run_one_job(job, path, directory)

        except Exception as e:
            # Update job status
            logging.exception('Got exception....')
            update_job_status(
                job['id'],
                'Failed. Exception - ' + str(e) + '. Check log file for details. ',
                processing_step_no
            )

        print("Completed")
        if len(jobs) < 2:
            get_email(username)


    else:
        print("There are no datasets that needs to be processed at this time.")


if __name__ == '__main__':
    # get_email('rptan')

    run()