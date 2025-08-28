import csv
def generate_csv(data, filename):
    #import csv

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(data[0].keys())

        # Write the data
        for row in data:
            writer.writerow(row.values())

            

def generate_csv_json(data, filename):
    """
    Parse a list of JSON objects and write them to a CSV file.
    Assumes 'data' is a list of dicts (parsed from JSON).
    """
    import csv
    if not data:
        return
    # Collect all possible keys from all objects
    print("inside json:")
    all_keys = set()
    for obj in data:
        all_keys.update(obj.keys())
    all_keys = list(all_keys)
    print("all keys are:", all_keys)
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=all_keys)
        writer.writeheader()
        for obj in data:
            writer.writerow(obj)

