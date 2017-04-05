#!/usr/bin/python3

import os
import argparse

def list_filenames_from_directory(directory):
    files = set()
    paths = {}
    sizes = {}

    number_of_files = 0
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            files.add(filename)

            file_path = os.path.join(dirpath, filename)
            file_size = os.stat(file_path).st_size
            if filename not in paths:
                paths[filename] = [dirpath]
                sizes[filename] = [file_size]
            else:
                paths[filename].append(dirpath)
                sizes[filename].append(file_size)

        number_of_files += 1

    print("Total number of files from directory {} is {}".format(directory, number_of_files))

    return {'fileset': files, 'paths': paths, 'sizes': sizes}

def main(directory1, directory2):
    directory_information_1 = list_filenames_from_directory(directory1)
    directory_information_2 = list_filenames_from_directory(directory2)

    print("Files in {} but not in {}:".format(directory1, directory2))

    missing_files = directory_information_1['fileset'] - directory_information_2['fileset']

    missing_files = list(missing_files)
    missing_files.sort()

    directory_to_missing_files = {}

    for file in missing_files:
        print("File missing: {}".format(file))
        print("It can be found in:")
        for path in directory_information_1['paths'][file]:
            print("  '{}'".format(path))

            if path in directory_to_missing_files:
                directory_to_missing_files[path].append(file)
            else:
                directory_to_missing_files[path] = [file]

        print()

    print("Total missing files: {}".format(len(missing_files)))
    print("===================================================")

    for directory in directory_to_missing_files.keys():
        print("The files below can no longer be found. They were found in: '{}':".format(directory))
        for file in directory_to_missing_files[directory]:
            print("   {}".format(file))

        print()

    for file in directory_information_1['sizes']:
        found = False

        if file in directory_information_2['sizes']:
            for size in directory_information_2['sizes'][file]:
                if size in directory_information_1['sizes'][file]:
                    found = True

            if not found:
                print("File: {} has different size in both directories".format(file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lists file names with their path in dir1 not in dir2")
    parser.add_argument("directory1", type=str, help="Directory to get the initial file set")
    parser.add_argument("directory2", type=str, help="Directory with the ending file set")

    args = parser.parse_args()

    main(args.directory1, args.directory2)