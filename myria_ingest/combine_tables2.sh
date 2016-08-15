#!/bin/bash
set -e #command fail -> script fail
set -u #unset variable reference causes script fail

_usage() {
  echo "Usage: $0 myria_host:myria_port myria_web_host:myria_web_port QueryPrefix QuerySuffix ResultRelation [-2]"
  echo "  QueryPrefix: the search term prefix for relations in Myria to combine"
  echo "  QuerySuffix: the search term suffix for relations in Myria to combine"
  echo "  ResultRelation: the name of the new relation to store in Myria"
  echo "  ex: $0 node-109:8753 node-109:8080 kmercnt_11_forward_S \"\" kmercnt_11_forward"
  echo "  This script queries a Myria instance for all the relations that match a search term."
  echo "  It creates a MyriaL query that unions together all the matching relations and stores them."
  exit 1
}

if [ "$#" -lt "5" ]; then
  _usage
fi

MyriaHostAndPort="${1}"
MyriaWebHostAndPort="${2}"
QueryPrefix="$3"
QuerySuffix="$4"
ResultRelation="$5"

BatchSize=100

# Check pre-requisite
command -v jsawk >/dev/null 2>&1 || { echo >&2 "I require 'jsawk' but it's not installed. Aborting."; exit 1; }

if [ -e "/tmp/myriaIngestDir_$(whoami)" ]; then
  if [ -d "/tmp/myriaIngestDir_$(whoami)" ]; then
    TDIR="/tmp/myriaIngestDir_$(whoami)" 
  else
    echo "Warning: the path \"/tmp/myriaIngestDir\" is taken"
    TDIR=`mktemp -d myriaIngestDir_XXXXXXXXXX`
  fi
else
  mkdir "/tmp/myriaIngestDir_$(whoami)"
  TDIR="/tmp/myriaIngestDir_$(whoami)"
fi

GlobalCounter=0

do_query() {
    # global TDIR
    Query="$1"
    echo $1
  GlobalCounter=$((GlobalCounter+1))
}

str=""
counter=0
while read rn; do {
    if [[ "$rn" != "$QueryPrefix"* ]] || [[ "$rn" != *"$QuerySuffix" ]]; then
      continue
    fi

    sid=`expr "$rn" : '.*\(S[0-9]\{4\}\)'`

    if [ -z "$str" ]; then
      str="R = scan($rn);"
    else
      str="${str}
R = R + scan($rn);"
    fi

    counter=$((counter+1))
    if [[ "$counter" -eq "$BatchSize" ]]; then
      # process this batch
      str="$str
store(R, ${ResultRelation}_Pkmer, [kmer]);"

      do_query "$str"
      # reset
      str="R = scan(${ResultRelation}_Pkmer);"
      counter=0
    fi

}; done < <(curl -s -XGET "$MyriaHostAndPort"/dataset/search?q="${QueryPrefix}${QuerySuffix}" \
    | jsawk 'return this.relationName' -a 'return this.join("\n")' ) || :


if [[ "$counter" -gt 0 ]]; then
  # process last batch
  str="$str
store(R, ${ResultRelation}_Pkmer, [kmer]);"

  do_query "$str"
fi




# to remove newlines from the output
# | tr '\n' ' ' | less
