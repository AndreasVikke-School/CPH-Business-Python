import csv

def print_file_content(file):
    with open(file, encoding = "ISO-8859-1") as File:  
        reader = csv.reader(File)
        for row in reader:
            print(row)

def write_list_to_file(output_file, *strings):
    with open(output_file, 'w') as File:
        for s in strings:
            File.write(s + "\n")

def read_csv(input_file):
    with open(input_file, encoding = "ISO-8859-1") as File:  
        l = []
        reader = csv.reader(File)
        for row in reader:
            l.append(row)
        return l