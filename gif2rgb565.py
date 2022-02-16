#!/usr/bin/python
import struct
import sys

from PIL import Image


#isSWAP = False
isSWAP = True

def main():
    len_argument = len(sys.argv)
    if len_argument not in [4,6]:
      print ("Correct Usage:")
      print ("\tpython gif2rgb565.py <gif_file> -h <output_header_file> -o <output_binary_file>")
      sys.exit(0)

    try:
        im = Image.open(sys.argv[1])
    except IOError:
        print("Cant load input GIF file")
        sys.exit(1)
    #mypalette = im.getpalette()

    h_out = False
    bin_out = False

    if sys.argv[2] == "-h":
        try:
            h_out = True
            outfile = open(sys.argv[3], "w")
        except:
            print("Can't write the file %s" % sys.argv[3])
            sys.exit(0)
    if h_out:
        var_offset = 2
    else:
        var_offset = 1

    if (sys.argv.__contains__("-o")):
        try:
            bin_out = True
            binoutfile = open(sys.argv[2*var_offset+1], "wb")
        except:
            print("Can't write the binary file %s" % sys.argv[2*var_offset+1])
            sys.exit(0)


    if h_out :
        array_name = sys.argv[3].split(".")[0];
        print("#ifndef __%s__" % sys.argv[3].replace(" ","_"), file=outfile)
        print("#define __%s__" % sys.argv[3].replace(" ","_"), file=outfile)
        print("", file=outfile)
        print("/* gif related variables */", file=outfile)
        print("const unsigned int %s_width = %d;" % (array_name, im.size[0]), file=outfile)
        print("const unsigned int %s_height = %d;" % (array_name, im.size[1]), file=outfile)
        print("const unsigned int %s_frames = %d;" % (array_name, im.n_frames), file=outfile)
        print("", file=outfile)
        print("const static uint16_t %s[%d][%d] PROGMEM= {" % \
                (array_name, im.n_frames,im.size[0]*im.size[1]), file=outfile)

    try:
        for frame in range(im.n_frames):
            im.seek(frame)
            #im.putpalette(mypalette)
            new_im = Image.new("RGB", im.size)
            new_im.paste(im)

            if h_out:
                print("\t\t{", end='', file=outfile)

            image_height = new_im.size[1]
            image_width = new_im.size[0]
            pix = new_im.load()  # load pixel array
            for h in range(image_height):
                for w in range(image_width):
                    if w < new_im.size[0]:
                        R = pix[w, h][0] >> 3
                        G = pix[w, h][1] >> 2
                        B = pix[w, h][2] >> 3

                        rgb = (R << 11) | (G << 5) | B

                        if (isSWAP == True):
                            swap_string_low = rgb >> 8
                            swap_string_high = (rgb & 0x00FF) << 8
                            swap_string = swap_string_low | swap_string_high
                            if h_out:
                                print("0x%04x," % (swap_string), end='', file=outfile)
                            if bin_out:
                                binoutfile.write(struct.pack('H', swap_string))
                        else:
                            if h_out:
                                print("0x%04x," % (rgb), end='', file=outfile)
                            if bin_out:
                                binoutfile.write(struct.pack('H', rgb))
                    else:
                        rgb = 0
                #
            if h_out:
                print("},", file=outfile)

    except EOFError:
        pass # end of sequence

    if h_out:
        print("", file=outfile)
        print("};", file=outfile)
        print("#endif // __%s__" % sys.argv[3].replace(" ", "_"), file=outfile)
        outfile.close()
    if bin_out:
        binoutfile.close()

    print ("GIF file \"%s\"" % sys.argv[1], "converted to \"%s\"" % sys.argv[3])

if __name__=="__main__":
  main()
