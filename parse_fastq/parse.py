#!.env/bin/python2
import sys
import os
from Bio import SeqIO
from tqdm import tqdm

outdir = "./parsed"
# Careful to maintain consistent order
columns = ["id", "seq", "instrument", "flowcell_lane", "tile_num", "x", "y", 
        "index", "pair"]

def sampleid_from_filename(filename):
    return os.path.basename(filename).split('_')[0]

def record_to_dict(record):
    d = {}
    d["id"] = record.id
    d["seq"] = str(record.seq)

    # Parse ID further - not sure if needed:
    exp_details, sample_details = record.id.split("#")
    
    e = exp_details.split(":")
    assert len(e) == 5
    d["instrument"], d["flowcell_lane"], d["tile_num"], d["x"], d["y"] = e

    s = sample_details.split("/")
    assert len(s) == 2
    d["index"], d["pair"] = s

    return d

def record_to_csv(record, detail):
    if detail == "full":
        fields = []
        d = record_to_dict(record)
        for col in columns:
            fields.append(d[col])
        return ",".join(fields) + "\n"
    else:
        return "%s,%s\n" % (record.id, str(record.seq))

def parse_file(infile, detail="low"):
    sample = sampleid_from_filename(infile)
    outfile = "%s/%s.csv" % (outdir, sample)
    if os.path.exists(outfile):
        print "%s already exsits. Skipping..." % outfile
        return

    print "Processing %s to %s" % (infile, outfile)
    with open(outfile, 'w') as of, open(infile, 'rU') as f:
        # First write header
        if detail == "full":
            of.write(",".join(columns) + "\n")
        else:
            of.write("id,seq\n")
        for record in tqdm(SeqIO.parse(f, "fastq")):
            of.write(record_to_csv(record, detail))

def main():
    if len(sys.argv) < 2:
        print "Usage: %s <fastq filename(s)>" % sys.argv[0]
        exit(1)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for filename in sys.argv[1:]:
        parse_file(filename)

if __name__ == "__main__":
    main()
