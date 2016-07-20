
# This script uploads generated data to S3

# Requires aws-cli to be installed
# currently assumes account access and credentials set up
command -v aws >/dev/null 2>&1 || { echo >&2 "aws-cli not found - aborting."; exit 1; }

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input directory>"
    exit 1
fi

INDIR=$1
if [ ! -d $INDIR ]; then
    echo "Error: $INDIR not found"
fi

BUCKET="oceankmers"
DIR="overlapped"

# Input directory
S3="s3://${BUCKET}/${DIR}/"

for f in $(ls $INDIR); do
    # Upload the data to S3 - grants everyone read access
    aws s3 cp $f $S3 --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers
done
