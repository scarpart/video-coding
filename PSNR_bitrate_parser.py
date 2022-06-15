import os
from csv import writer

# the only bits of information that need to be changed are shown below
videos = os.listdir('/home/arthurscarpatto/VC/BD-Rate/Video-Samples/')
num_frames = 3
qps = [22, 27, 32, 37]
encoder = "VTM"

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
        psnr = data_line[5]

    return bitrate, psnr


for v in videos:
    div_index = v.index("_")                                             # gets the _ index to separate the video name as follows: Video_WIDTHxHEIGHT --> Video / WIDTHxHEIGHT
    video_res = v[div_index]                                             # uses aforementioned index to get the resolution only
    video_cfg_filepath = "cfg/per-sequence/{}.cfg".format(v[:div_index]) # gets the video name only and appends it to string to get its cfg file path

    # lines below input a command into the terminal and extract information from its output by means of a .txt file 
    for qp in qps:
        os.system("./bin/EncoderAppStatic -c cfg/encoder_randomaccess_vtm.cfg -c {} -f {} -q {} > output.txt".format(video_cfg_filepath, str(num_frames), str(qp))) 
        bit_rate, psnr = parse("output.txt")

        # appends the information gathered into a csv file with all the relevant parameters  
        with open("/home/arthurscarpatto/VC/BD-Rate/results.csv", 'a', newline='') as csv_file:
            writer_object = writer(csv_file)
            writer_object.writerow([encoder, v, video_res, num_frames, qp, bit_rate, psnr, video_cfg_filepath])
            csv_file.close()
