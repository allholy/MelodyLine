'''
Main script that calls all the others and implements the whole pipeline,
as long as connects with SuperCollider.
'''

import argparse
import sys

from pythonosc import osc_message_builder
from pythonosc import udp_client

from preprocessing import names_list, fix_path
from melody_extraction import final_contours_all
from default_shapes import make_shape, shape_functions
from similarity import similarity_all, return_sorted


IP_ADDRESS = "127.0.0.1" #local network
PORT = 57120 #port that osc server is listening on

# Make client
client = udp_client.SimpleUDPClient(IP_ADDRESS, PORT)


# pass arguments from SuperCollider
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--soundnames", required=False, help="Path for .txt file with soundnames for analysis.")
parser.add_argument("-a", "--audiofiles", required=False, help="Path for folder with audiofiles")
parser.add_argument("-i", "--inputdata", required=False, help="Path for .txt file with data customized by user.")
args = vars(parser.parse_args())

names_path = str(args['soundnames'])
sounds_path = str(args['audiofiles'])
data_path = str(args['inputdata'])


def main(names_path_,sounds_path_,data_path_):

    # open file with input data of user.
    with open(data_path_, 'r') as f:
        data = f.read().splitlines()
        data = [i for i in data if i != '']

    # data into variables
    shape = str(data[0].strip())
    pitch_base = float(data[1])
    slope = float(data[2])

    # preprocessing
    list_of_paths = names_list(names_path_)
    fixed_list_of_paths = fix_path(list_of_paths, sounds_path_)

    # melody/contour extraction
    coefs, times_len = final_contours_all(fixed_list_of_paths)

    # user shape
    shape = shape_functions(shape,slope,pitch_base)

    # similarity/distance
    distances = similarity_all(coefs,times_len,shape)

    # final list
    sorted_path_list = return_sorted(distances, fixed_list_of_paths)
    print(*sorted_path_list,sep='\n')
    print("Sorting done.")


    # send to SC
    client.send_message("/py", sorted_path_list[0])
    print("Data sent.")


if __name__ == '__main__':

    # test python without SC3
    import os
    dir = os.path.normpath(os.getcwd() + os.sep + os.pardir) + "/mirlc2"
    names_path = dir +"/python/soundnames_analysis.txt"
    sounds_path = dir + "/sounds/"
    data_path = dir + "/python/shape.txt"

    # run everything
    main(names_path, sounds_path, data_path)
