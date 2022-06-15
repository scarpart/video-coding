def parse(to_be_parsed):
    with open("./{}".format(to_be_parsed), 'r') as txt:
        text = txt.read().split("\n")
        for line in text:
            if "YUV-PSNR" in line.split():
                data_line = text[text.index(line)+1].split()
                break
        txt.close()
        psnr = data_line[2]
        bitrate = data_line[5]

parse("./foo.txt")