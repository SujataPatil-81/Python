def generate_csv(data, filename):
    import csv

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(data[0].keys())

        # Write the data
        for row in data:
            writer.writerow(row.values())