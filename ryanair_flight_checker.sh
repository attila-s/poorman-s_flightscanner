#!/bin/bash

DATE_CMD=date

display_usage() { 
  cat <<EOF
Usage: $0 [options]
Retrieve flight dates and prices from RyainAir REST API 
 -h| --help           display this help and exit
 -d|--day             start day in format %YYYY-%MM-%DD; defaults to NOW
 -o|--origin          origin; defaults to BUD
 -p|--period          Number of periods; 1 period equals to 10 days; if start is 2016-10-01 and period is 1 then we search between 2016-10-01 and 2016-10-11
 -dest|--destinations comma separated list of destinations using airport codes LTN; defaults to all destinations from BUD
 --out                output directory where flight data is downloaded in JSON files (filename format - [destination]_%YYYY-%MM-%DD.json)
 -l|--list            List airport codes available from BUD

Examples:
  $0 --out CANARY -o BUD --dest FUE,ACE,TFS -d 2016-11-02 -p 4
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

process() {
  for d in ${destinations[@]}; do 
    day=${start_day};
    for i in $(seq 1 ${period}); do   
      next=$($DATE_CMD '+%Y-%m-%d' -d "$day+4 days")    
      curl "https://desktopapps.ryanair.com/hu-hu/availability?ADT=1&CHD=0&DateIn=${next}&DateOut=${day}&Destination=${d}&FlexDaysIn=0&FlexDaysOut=4&INF=0&Origin=${origin}&RoundTrip=true&TEEN=0" \
        -H "Pragma: no-cache" -H "Origin: https://www.ryanair.com" \
        -H "Accept-Encoding: gzip, deflate, sdch, br" \
        -H "Accept-Language: en-US,en;q=0.8" \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36" \
        -H "Accept: application/json, text/plain, */*" \
        -H "Referer: https://www.ryanair.com/hu/hu/booking/home"\
        -H "Connection: keep-alive" -H "Cache-Control: no-cache" \
      --compressed > ${output_dir}/${origin}-${d}_${day}.json
  
  #curl 'https://desktopapps.ryanair.com/hu-hu/availability?ADT=1&CHD=0&DateIn=2017-01-13&DateOut=2017-01-06&Destination=VDA&FlexDaysIn=6&FlexDaysOut=2&INF=0&Origin=BUD&RoundTrip=true&TEEN=0&exists=false' -H 'Origin: https://www.ryanair.com' -H 'Accept-Encoding: gzip, deflate, sdch, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://www.ryanair.com/hu/hu/booking/home' -H 'Connection: keep-alive' --compressed
  day=${next}
    done
  done
}

airports() {
  cat > airports.txt <<END
Alghero (Sardinia)              AHO
Alicante                        ALC
Baku                            GYD
Barcelona El Prat               BCN
Bari                            BRI
Bergen                          BGO
Birmingham                      BHX
Bologna                         BLQ
Bourgas (Black Sea)             BOJ
Brussels Charleroi              CRL
Bucharest                       OTP
Catania (Sicily)                CTA
Corfu                           CFU
Dortmund                        DTM
Dubai                           DWC
Eindhoven                       EIN
Faro                            FAO
Frankfurt Hahn                  HHN
Fuerteventura (Canary Islands)  FUE
Glasgow                         GLA
Gothenburg Landvetter           GOT
Hanover                         HAJ
Heraklion (Crete)               HER
Ibiza                           IBZ
Karlsruhe/Baden-Baden           FKB
Kutaisi (Georgia)               KUT
Kyiv Zhulyany                   IEV
Lamezia Terme                   SUF
Lanzarote (Canary Islands)      ACE
Larnaca (Cyprus)                LCA
Lisbon                          LIS
Liverpool                       LPL
London Luton                    LTN
Madrid                          MAD
Malaga                          AGP
Malmo                           MMX
Malta                           MLA
Milan Malpensa                  MXP
Moscow                          VKO
Naples                          NAP
Nice                            NCE
Palma de Mallorca               PMI
Porto Airport                   OPO
Reykjavik                       KEF
Rhodes                          RHO
Riga                            RIX
Rome Fiumicino                  FCO
Sofia                           SOF
Stockholm Skavsta               NYO
Targu Mures                     TGM
Tel Aviv                        TLV
Tenerife (Canary Islands)       TFS
Thessaloniki                    SKG
Varna (Black Sea)               VAR
Warsaw Chopin                   WAW
Zakynthos                       ZTH
END

  cat airports.txt | rev| awk '{print $1}' | rev > airport_codes.txt 
}

list() {
  cat airports.txt
}

parse $@
airports
setup
process
