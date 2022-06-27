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
        line_time = text[-2].split()
        total_time = line_time[2]

    return bitrate, psnr, total_time


for encoder in configs['encoder']: 
    for v in configs['videos']:
        div_index = v.index("_")                                             # gets the _ index to separate the video name as follows: Video_WIDTHxHEIGHT --> Video / WIDTHxHEIGHT
        video_res = v[div_index+1:-4]                                        # uses aforementioned index to get the resolution only
        video_name = v[:div_index]                                          # uses aforementioned index to get the name only
        video_cfg_filepath = f"~/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/cfg/per-sequence/{video_name}.cfg"

        # lines below input a command into the terminal and extract information from its output by means of a .txt file 
        for qp in configs['qps']:
            # creating a unique name for the txt file based on the parameters
            outcome = f"{encoder}_{video_name}_{str(configs['num_frames'])}frames_{str(qp)}qsize"
            txt_dir = os.listdir('./text-outcomes/') 
            
            # handling different encoder options
            # if name_txt already exists in target dir, the following script does not execute as the result is the same
            if outcome + ".txt" not in txt_dir:
                if encoder == "VTM":            
                    # configures VTM and directs its output to a unique txt file
                    os.system(f"~/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/bin/EncoderAppStatic \
                                -c ~/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/cfg/encoder_randomaccess_vtm.cfg  -b ./binary-outcomes/{outcome}.bin \
                                    -c {video_cfg_filepath} -f {str(configs['num_frames'])} -q {str(qp)} {configs['settings_VTM']} > ./text-outcomes/{outcome}.txt")

                elif encoder == "vvenc":
                    # configures vvenc and directs its output to a unique txt file
                    os.system(f"~/VC/BD-Rate/vvenc/bin/release-static/vvencapp -i ~/VC/BD-Rate/Video-Samples/{v} \
                        --output=./binary-outcomes/{outcome}.bin --frames {str(configs['num_frames'])} --qp {str(qp)} {configs['settings_vvenc']} > ./text-outcomes/{outcome}.txt")

                # parses the output txt file to acquire relevant information 
                bit_rate, psnr, total_time = parse(f"text-outcomes/{outcome}.txt")

                # appends the information gathered into a csv file with all the relevant parameters  
                with open("./results.csv", 'a') as csv_file:
                    writer_object = writer(csv_file)

                    # appends : name of encoder - video sample name - video resolution - number of frames - quantization parameter - bit rate - psnr - optional settings
                    writer_object.writerow([encoder, video_name, video_res, configs['num_frames'], qp, bit_rate, psnr, configs[f"settings_{encoder}"], total_time])
                    csv_file.close()
