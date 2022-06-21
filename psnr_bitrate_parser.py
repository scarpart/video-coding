import os
from csv import writer
import json

file_cfgs = open('configs.json')
configs = json.load(file_cfgs)
file_cfgs.close()


# function for extracting the bitrate and PSNR out of a txt file
def parse(to_be_parsed):
    with open("./{}".format(to_be_parsed), 'r') as txt:
        text = txt.read().split("\n")
        for line in text:
            if "YUV-PSNR" in line.split():
                data_line = text[text.index(line)+1].split()
                break
        txt.close()
        bitrate = data_line[2]
        psnr = data_line[6]

    return bitrate, psnr


for v in configs['videos']:
    div_index = v.index("_")                                             # gets the _ index to separate the video name as follows: Video_WIDTHxHEIGHT --> Video / WIDTHxHEIGHT
    video_res = v[div_index+1:-4]                                        # uses aforementioned index to get the resolution only
    video_name = v[:div_index]                                          # uses aforementioned index to get the name only
    video_cfg_filepath = f"/home/arthurscarpatto/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/cfg/per-sequence/{video_name}.cfg"

    # lines below input a command into the terminal and extract information from its output by means of a .txt file 
    for qp in configs['qps']:
        name_txt = f"{configs['encoder']}_{video_name}_{str(configs['num_frames'])}frames_{str(qp)}qsize"
        txt_dir = os.listdir('./individual_outcomes/')
        
        # handling different encoder options
        if configs['encoder'] == "VTM":            
            # configures VTM and directs its output to a unique txt file
            # if name_txt already exists in target dir, the following script does not execute as the result is the same
            if name_txt not in txt_dir:
                os.system(f"/home/arthurscarpatto/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/bin/EncoderAppStatic \
                            -c /home/arthurscarpatto/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/cfg/encoder_randomaccess_vtm.cfg \
                                -c {video_cfg_filepath} -f {str(configs['num_frames'])} -q {str(qp)} {configs['settings_VTM']}> {name_txt}.txt")

        elif configs['encoder'] == "vvenc":
            # configures vvenc and directs its output to a unique txt file
            if name_txt not in txt_dir:
                os.system(f"/home/arthurscarpatto/VC/BD-Rate/vvenc/bin/release-static/vvencapp -i /home/arthurscarpatto/VC/BD-Rate/Video-Samples/{v} \
                    --output=bit.266 --frames {str(configs['num_frames'])} --qp {str(qp)} {configs['settings_vvenc']}> /individual_outcomes/{name_txt}.txt")

        bit_rate, psnr = parse("output.txt")

        # appends the information gathered into a csv file with all the relevant parameters  
        with open("./results2.csv", 'a') as csv_file:
            writer_object = writer(csv_file)
            writer_object.writerow([configs['encoder'], v, video_res, configs['num_frames'], qp, bit_rate, psnr])
            csv_file.close()
