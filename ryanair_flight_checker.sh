#!/bin/bash

. common.sh

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

main $@
process
