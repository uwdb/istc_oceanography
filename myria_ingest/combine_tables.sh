#!/bin/bash
set -e #command fail -> script fail
set -u #unset variable reference causes script fail

_usage() {
  echo "Usage: $0 myria_host:myria_port QueryPrefix QuerySuffix ResultRelation"
  echo "  QueryPrefix: the search term prefix for relations in Myria to combine"
  echo "  QuerySuffix: the search term suffix for relations in Myria to combine"
  echo "  ResultRelation: the name of the new relation to store in Myria"
  echo "  ex: $0 node-109:8753 kmercnt_11_forward_S \"\" kmercnt_11_forward"
  echo "  This script queries a Myria instance for all the relations that match a search term."
  echo "  It creates a MyriaL query that unions together all the matching relations and stores them."
  exit 1
}
# ./combine_tables.sh localhost:8753 kmercnt_11_forward_S _ol kmercnt_11_forward_ol > kmercnt_11_forward_ol
# ./combine_tables.sh localhost:8753 kmercnt_11_rc_S _ol kmercnt_11_rc_ol > kmercnt_11_rc_ol
# ./combine_tables.sh localhost:8753 kmercnt_11_lex_S _ol kmercnt_11_lex_ol > kmercnt_11_lex_ol

if [ "$#" -lt "4" ]; then
  _usage
fi

MyriaHostAndPort="${1}"
QueryPrefix="$2"
QuerySuffix="$3"
ResultRelation="$4"

# Check pre-requisite
command -v jsawk >/dev/null 2>&1 || { echo >&2 "I require 'jsawk' but it's not installed. Aborting."; exit 1; }

str=""
while read rn; do {

    if [[ "$rn" != "$QueryPrefix"* ]] || [[ "$rn" != *"$QuerySuffix" ]]; then
      continue
    fi

    sid=`expr "$rn" : '.*\(S[0-9]\{4\}\)'`

    if [ -z "$str" ]; then
      str="$rn = scan($rn); R = [from $rn emit \"$sid\" as sampleid, kmer, cnt];
"
    else
      str="$str$rn = scan($rn); R = R + [from $rn emit \"$sid\" as sampleid, kmer, cnt];
"
    fi
}; done < <(curl -s -XGET "$MyriaHostAndPort"/dataset/search?q="${QueryPrefix}${QuerySuffix}" \
    | jsawk 'return this.relationName' -a 'return this.join("\n")' ) || :

str="$str
store(R, ${ResultRelation}_Pkmer, [kmer]);
store(R, ${ResultRelation}_Psampleid, [sampleid]);"

echo "$str"

# to remove newlines from the output
# | tr '\n' ' ' | less
