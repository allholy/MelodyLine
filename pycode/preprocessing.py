'''
Loading and preprocessing of the paths.
'''

def names_list(filepath):
    ''' Open file and put paths to list.
    Args:
        filepath (str): Path to a .txt file.

    Returns:
        pathlist (list): List with the paths that are found in the file.
    '''
    with open(filepath, 'r') as f:
        pathlist = f.read().splitlines()
        pathlist = [i for i in pathlist if i != '']
    return pathlist

formats = [".wav", ".ogg", ".flac", ".mp3", ".aiff", ".aif", ".mv4"]
def fix_path(path_list, sounds_path):
    ''' Correct the paths.
    Args:
        path_list (list): List with paths.
        sounds_path (str): Path that specifies where the sounds are stored.
    '''
    for pos, path in enumerate(path_list):
        #remove format ending
        for format in formats:
            path_list[pos] = path_list[pos].replace(format, '')

        #add path and .ogg
        path_list[pos] = sounds_path + str(path_list[pos]).strip() + ".ogg"

        #print(path_list[pos])
    print(' ..preprocessing done \n ------------------------------------------------')
    #print(len(path_list))
    return path_list


if __name__ == '__main__':
    import os,sys

    dir = os.path.normpath(os.getcwd() + os.sep + os.pardir) + "/mirlc2"

    names_path= dir + str(sys.argv[1])
    sounds_path= dir + str(sys.argv[2])

    pathlist = names_list(names_path)
    paths = fix_path(pathlist,sounds_path)
    print(paths)

#python3 preprocessing.py  /python/soundnames_analysis.txt /sounds/ /python/shape.txt
