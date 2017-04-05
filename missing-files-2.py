#!/usr/bin/python3

import os
import argparse

def list_filenames_from_directory(directory):
    files = set()
    paths = {}

    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            files.add(filename)

            if filename not in paths:
                paths[filename] = [dirpath]
            else:
                paths[filename].append(dirpath)

    return {'fileset': files, 'paths': paths}

def main(directory1, directory2, directory3, directory4):
    directory_information_1 = list_filenames_from_directory(directory1)
    directory_information_2 = list_filenames_from_directory(directory2)
    directory_information_3 = list_filenames_from_directory(directory3)
    directory_information_4 = list_filenames_from_directory(directory4)

    print("Files in {} or {} not in {} neither {}:".format(directory1, directory2, directory3, directory4))

    set1 = directory_information_1['fileset'].union(directory_information_2['fileset'])
    set2 = directory_information_3['fileset'].union(directory_information_4['fileset'])

    missing_files = set1 - set2

    missing_files = list(missing_files)
    missing_files.sort()

    directory_to_missing_files = {}

    for file in missing_files:
        #print("File missing: {}".format(file))
        #print("It can be found in:")
        if file in directory_information_1['paths']:
            for path in directory_information_1['paths'][file]:
                print("cp '{}/{}' {}".format(path, file, "/mnt/data_admin/project_05_before_cleaning_up/"))
                # print("  '{}'".format(path))

        if file in directory_information_2['paths']:
            for path in directory_information_2['paths'][file]:
                print("cp '{}/{}' {}".format(path, file, "/mnt/data_admin/project_05_before_cleaning_up/"))
                # print("  '{}'".format(path))

        print()

    # print("Total missing files: {}".format(len(missing_files)))
    # print("===================================================")
    #
    # for directory in directory_to_missing_files.keys():
    #     print("The files below can no longer be found. On the server they were in the following folder: '{}':".format(
    #         directory))
    #     for file in directory_to_missing_files[directory]:
    #         print("   {}".format(file))
    #
    #     print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lists file names with their path in dir1 not in dir2")
    parser.add_argument("directory1", type=str, help="Directory to get the initial file set")
    parser.add_argument("directory2", type=str, help="Directory to get the initial file set")
    parser.add_argument("directory3", type=str, help="Directory with the ending file set")
    parser.add_argument("directory4", type=str, help="Directory with the ending file set")

    args = parser.parse_args()

    main(args.directory1, args.directory2, args.directory3, args.directory4)