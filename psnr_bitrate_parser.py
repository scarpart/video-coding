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
    video_res = v[div_index+1:-4]                                          # uses aforementioned index to get the resolution only
    video_cfg_filepath = "/home/arthurscarpatto/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/cfg/per-sequence/{}.cfg".format(v[:div_index]) # gets the video name only and appends it to string to get its cfg file path

    # lines below input a command into the terminal and extract information from its output by means of a .txt file 
    for qp in configs['qps']:
        if configs['encoder'] == "VTM":
            os.system("/home/arthurscarpatto/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/bin/EncoderAppStatic -c /home/arthurscarpatto/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/cfg/encoder_randomaccess_vtm.cfg -c {} -f {} -q {} > output.txt".format(video_cfg_filepath, str(num_frames), str(qp)))
        elif configs['encoder'] == "vvenc":
            os.system('/home/arthurscarpatto/VC/BD-Rate/vvenc/bin/release-static/vvencapp -i /home/arthurscarpatto/VC/BD-Rate/Video-Samples/{} --output=bit.266 --frames {} --qp {} > output.txt'.format(v, str(configs['num_frames']), str(qp)))
        bit_rate, psnr = parse("output.txt")

        # appends the information gathered into a csv file with all the relevant parameters  
        with open("./results2.csv", 'a') as csv_file:
            writer_object = writer(csv_file)
            writer_object.writerow([configs['encoder'], v, video_res, configs['num_frames'], qp, bit_rate, psnr, video_cfg_filepath])
            csv_file.close()
