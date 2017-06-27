DATE_CMD=date

display_usage() { 
  cat <<EOF
Usage: $0 [options]
Retrieve flight dates and prices
 -h| --help           display this help and exit
 -d|--day             start day in format %YYYY-%MM-%DD; defaults to now
 -o|--origin          origin; defaults to BUD
 -p|--period          Number of periods; 1 period equals to 10 days; if start is 2016-10-01 and period is 1 then we search between 2016-10-01 and 2016-10-11
 -dest|--destinations comma separated list of destinations using airport codes LTN; defaults to all destinations from BUD
 --out                output directory where flight data is downloaded in JSON files (filename format - [destination]_%YYYY-%MM-%DD.json)
 -l|--list            List airport codes available from BUD

Examples:
  $0 --out CANARY -o BUD --dest FUE,ACE,TFS -d $(date +"%Y-%m-%d") -p 4
EOF
  exit
}

parse() {
  while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
      -d|--day)
        start_day="$2"
        shift 
        ;;
      -o|--origin)
        origin="$2"
        shift 
        ;;
      -p|--period)
        period="$2"
        shift
        ;;    
      --dest|--destinations)
        destinations="$2"
        ;;
      --out)
        output_dir="$2"
        mkdir -p $2
        ;;
      -l|--list)
        list
        exit
        ;;
      --help)
        display_usage
        ;;
    esac
    shift 
  done
}  


setup() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    command -v gdate >/dev/null 2>&1 || { echo "GNU date but is not installed.  Aborting." >&2; exit 1; }
    DATE_CMD=gdate 
  fi
  if [ "${start_day}" != "" ]; then
    echo Using day ${start_day}
  else
    export start_day=$($DATE_CMD '+%Y-%m-%d')
  fi

  if [ "${origin}" != "" ]; then
    echo Using origin ${origin}
  else
    export origin=BUD
  fi

  if [ "${period}" != "" ]; then
    echo Using period ${period}
  else
    export period=10
  fi

  if [ "${destinations}" != "" ]; then
    destinations=(${destinations//,/ })
    echo Using destinations ${destinations} 
  else
    destinations=$(cat airport_codes.txt)
  fi

  if [ "${output_dir}" != "" ]; then
    echo Using output_dir ${output_dir} 
  else
    output_dir=report
    mkdir -p ${output_dir}
  fi
}


list() {
  cat airports.txt
}

main() {
  parse $@
  airports
  setup  
}
