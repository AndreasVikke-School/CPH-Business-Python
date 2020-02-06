import os

def write_folder_content_to_file(folder, output):
    with open(output, 'w') as File:
        for f in os.listdir(folder):
            File.write(folder + f + "\n")

def write_folder_content_to_file_with_dir(folder, output):
    with open(output, 'w') as File:
        for path,dirs,files in os.walk(folder):
            for filename in files:
                File.write(os.path.join(path,filename) + "\n")

def print_first_line_of_files(filenames):
    for f in filenames:
        if os.path.isfile(f):
            with open(f, 'r') as File:
                print(File.readline())

def print_emails_of_files(filenames):
    for f in filenames:
        if os.path.isfile(f):
            with open(f, 'r') as File:
                for line in File:
                    if '@' in line:
                        print(line)

def print_headers_of_md(filenames):
    for f in filenames:
        if os.path.isfile(f):
            with open(f, 'r') as File:
                for line in File:
                    if line.startswith("#") and line[1] == " ":
                        print(line)