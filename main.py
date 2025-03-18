import csv
with open('before.csv', newline='') as csvfile:
  d = csv.Sniffer().has_header(csvfile.read(1024))
  print(d)
  csvfile.se
  reader = csv.reader(csvfile, delimiter=',')
  for row in reader:
    print(row[0])