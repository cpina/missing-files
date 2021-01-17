#!/usr/bin/env python3

import argparse
import datetime
import os
import sys


def list_filenames_from_directory(directory):
    files = set()
    paths = {}
    sizes = {}
    dates = {}

    number_of_files = 0
    for (root, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            files.add(filename)

            file_path = os.path.join(root, filename)
            file_size = os.stat(file_path).st_size
            date = datetime.datetime.utcfromtimestamp(os.stat(file_path).st_mtime)

            if filename not in paths:
                paths[filename] = [root]
                sizes[filename] = [file_size]
                dates[filename] = [date]
            else:
                paths[filename].append(root)
                sizes[filename].append(file_size)
                dates[filename].append(date)

            number_of_files += 1

    print('Total number of files from directory {} is {}'.format(directory, number_of_files))

    return {'fileset': files, 'paths': paths, 'sizes': sizes, 'dates': dates}


def list_filenames_from_directories(directories):
    information = None

    for directory in directories:
        directory_information = list_filenames_from_directory(directory)

        if information:
            keys = information.keys()
            for key in keys:
                if type(information[key]) == set:
                    information[key] = information[key].union(directory_information[key])
                elif type(information[key]) == dict:
                    information[key].update(directory_information[key])
        else:
            information = directory_information

    return information


def abort_if_directories_does_not_exist(directories):
    for directory in directories:
        if not os.path.isdir(directory):
            print('Directory: ', directory, 'does not exist, exiting')
            sys.exit(1)


def main(source_directory, destination_directories):
    abort_if_directories_does_not_exist([source_directory] + destination_directories)
    source_files = list_filenames_from_directory(source_directory)
    destination_files = list_filenames_from_directories(destination_directories)

    print('Files in {} but not in {}:'.format(source_directory, destination_directories))

    # To check based only on file names:
    # missing_files = source_files['fileset'] - destination_files['fileset']

    missing_files = set()
    # To check based on file name AND file size
    for file in source_files['fileset']:
        if file not in destination_files['fileset']:
            missing_files.add(file)
        elif file in destination_files['fileset'] and source_files['sizes'][file][0] not in destination_files['sizes'][file]:
            print('Missing file because of size', file)
            missing_files.add(file)

    missing_files = list(missing_files)
    missing_files.sort()

    count = 0
    print('MISSING FILES')

    for file in missing_files:
        full_paths = []
        for path in source_files["paths"][file]:
            full_paths.append(os.path.join(path, file))

        full_paths = ', '.join(full_paths)
        print(full_paths)
        count += 1

    print('Total missing files:', count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lists file names with their path in dir1 not in dir2')
    parser.add_argument('source', type=str, help='Directory to get the initial file set (e.g. /mnt/camera)')
    parser.add_argument('destinations', metavar='N', type=str, nargs='+',
                        help='Directories with the copied file set (/mnt/backup/2020 /mnt/backup/2021)')

    args = parser.parse_args()

    main(args.source, args.destinations)
