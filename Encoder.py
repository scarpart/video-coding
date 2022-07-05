import json
import numpy as np
import os

class Encoder():
    """Class that defines methods for encoding, decoding and parsing data"""

    # Initializing the attributes
    def __init__(self, csv_path: str, configs_path: str) -> None:
        self.__csv_path = csv_path
        config_file = open(configs_path)
        self.__configs = json.load(config_file)
        config_file.close()

    def encode(self) -> None:
        """Method for encoding each sequence using each encoder with all 4 qp options"""

        # Uses each encoder 
        for encoder in self.__configs['encoder']: 

            # Uses each sequence
            for v in self.__configs['videos']:
                div_index = v.index("_")                             # gets the _ index to separate the video name as follows: Video_WIDTHxHEIGHT --> Video / WIDTHxHEIGHT
                video_res = v[div_index+1:-4]                       # uses aforementioned index to get the resolution only
                video_name = v[:div_index]                          # uses aforementioned index to get the name only
                video_cfg_filepath = f"~/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/cfg/per-sequence/{video_name}.cfg"

                # Lines below input a command into the terminal and extract information from its output by means of a .txt file 
                for qp in self.__configs['qps']:
                    # Creating a unique name for the txt file based on the parameters
                    outcome = f"{encoder}_{video_name}_{str(self.__configs['num_frames'])}frames_{str(qp)}qsize"
                    txt_dir = os.listdir('./text-outcomes/') 
                    
                    # Handling different encoder options
                    # If name_txt already exists in target dir, the following script does not execute as the result is the same
                    if outcome + ".txt" not in txt_dir:
                        if encoder == "VTM":            
                            # Configures VTM and directs its output to a unique txt file
                            os.system(f"~/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/bin/EncoderAppStatic \
                                        -c ~/VC/BD-Rate/VVCSoftware_VTM-VTM-17.0/cfg/encoder_randomaccess_vtm.cfg  -b ./binary-outcomes/{outcome}.bin \
                                            -c {video_cfg_filepath} -f {str(self.__configs['num_frames'])} -q {str(qp)} {self.__configs['settings_VTM']} > ./text-outcomes/{outcome}.txt")

                        elif encoder == "vvenc":
                            # Configures vvenc and directs its output to a unique txt file
                            os.system(f"~/VC/BD-Rate/vvenc/bin/release-static/vvencapp -i ~/VC/BD-Rate/Video-Samples/{v} \
                                --output=./binary-outcomes/{outcome}.bin --frames {str(self.__configs['num_frames'])} --qp {str(qp)} {self.__configs['settings_vvenc']} > ./text-outcomes/{outcome}.txt")
    
    # Method for extracting the YUV-PSNR, BitRate and total time taken to encode
    def parse(to_be_parsed: str) -> float:
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
    

