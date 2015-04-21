from csv            import DictReader
from unicodedata    import normalize as norm

def normalize(s):
    """Normalize utf8 characters to their ascii equivalents"""
    return norm('NFD', s.decode('utf8')).encode('ascii', 'ignore')

def csv_dict(path):
    """Return a dictionary wrapping contents of csv file in path"""
    with open(path, 'r') as hedgefile:
        return DictReader(hedgefile, delimiter='\t', quotechar='\"')

def hedge_usages(path):
    reader = csv_dict(path)
    hedges = {}
    for row in reader:
        hedges[normalize(row['hedge'])] = (row['usage_a'], row['usage_b'])
    return hedges

def format_entry(line):
    return '\"' + line.replace('\"', '\"\"') + '\"'

def append_usage(path):
    """Append usages to tagged lines"""
    usages = hedge_usages(path)
    for line in stdin:
        line = line.strip()
        a, b = usages[line[:line.index(',')].replace('"', '')]
        print '%s,%s,%s,FALSE,FALSE' % \
                (line.strip(), format_entry(a), format_entry(b))

if __name__ == '__main__' and len(argv) == 2:
    append_usage(argv[1])

