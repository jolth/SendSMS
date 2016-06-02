#!/usr/bin/env bash
#
# --sms="Message SMS"
# --number="send to number"
# --smsend="evaluates whether to send a sms " 
#
# optional argument:
# --payment=
#
# Usage: 
#       ./sendsms.sh file.csv 'message' --name=1 --device=2 --number=3 
#
# MESAJES:
#      
# Dependencias:
#    - Gammu

# Author: Jolth
#

## MAIN ###
CSVFILE=$1
SMSTEXT=$2
NEWCSVFILE="file_to_send.csv"
declare -a NAMES
declare -a PHONES
declare -a PLACAS


function usage {
    echo -e "Usage:\n
            ./sendsms.sh file.csv 'message' --name=1 --device=2 --number=3 --vehicle=4 \n\n"
    echo -e "fichero csv: \n
            ID,NAME,NUMBER
            DEV001,first_name last_name,31000000\n"
}

if [ ${#} -lt 1 ]; then
    echo -e "Error: debe especificar un fichero .csv\n"
    usage
    exit 0
fi

args=("$@")
ELEMENTS=${#args[@]} # get number of elements

# Create vars for the args
for ((i=2; i<$ELEMENTS;i++)); do
    eval $(echo ${args[i]}|awk -F'=' '{print $1"="$2}'|sed 's/-//g')
done

# Evaluate if arg --name existing 
if [ ! $name ]; then 
    echo -e "Error: arg --name is required\n"
    usage
    exit 1
fi 

# Evaluate if arg --number existing
if [ ! $number ]; then
    echo -e "Error: arg --number is required\n"
    usage
    exit 1
fi

if [ ! $placa ]; then
    echo -e "Error: arg --placa is required\n"
    usage
    exit 1
fi

# Evalua if --smsend existing
if [ $smsend ]; then
    echo "SMSEND: $smsend"
    rm $NEWCSVFILE
    count=0
    while read line; do
        if [ $count -eq 0 ]; then
            echo $line > $NEWCSVFILE
            count=$((count+1))
            continue
        fi
        
        l=$(echo $line|awk -F',' '{print tolower($'$smsend')}')
        if [ "$l" == "true" ]; then
            #echo "L:$l"
            echo $line >> $NEWCSVFILE 
        fi
        count=$((count+1))
    done < $CSVFILE
    CSVFILE=$NEWCSVFILE
else
    echo -e "Error: arg --smsend is required\n"
    usage
    exit 1
fi


function separate {
    COUNTER=20
    echo -n "["
    until [  $COUNTER -lt 10 ]; do
        echo -n "####"
        let COUNTER-=1
        sleep 1
    done
    echo -e "]\n"
}


## MAIN ###
#CSVFILE=$1
#SMSTEXT=$2
#declare -a NAMES
#declare -a PHONES
#declare -a PLACAS

echo -e "\nMESSAGE:\n$SMSTEXT\n"
chr_counts=$(echo $SMSTEXT|wc -m)
if (( $chr_counts>155 )); then # Largo del SMS 160 caracteres. 160 - $name = 155
    echo "Error: el Texto del MENSAJE es muy largo: $chr_counts"
    echo "tamaño maximo 155 caracteres"
    exit 1
fi
echo -e "Character number from MESSAGE: $chr_counts"
#separate


function fname {
# devuelve el primer nombre de el cliente
#
    while read line; do
        first_name=$(eval $(echo "awk -F',' '{print \$$name}'")|sed '/^$/d'|cut -d " " -f1)
        #echo -e "$first_name\n"
        #NAMES[$count]=$(eval $(echo "awk -F',' '{print \$$name}'")|sed '/^$/d'|cut -d " " -f1)
    done < $CSVFILE

    count=0
    for i in $first_name
    do
        NAMES[$count]=$i
        count=$((count+1))
    done
} 

function pnumber {
# devuelve el numero telefonico de el cliente
#
    while read line; do
        phone_number=$(eval $(echo "awk -F',' '{print \$$number}'")|sed '/^$/d')
        #echo -e "$phone_number\n"
        #PHONES[$count]=$(eval $(echo "awk -F',' '{print \$$number}'")|sed '/^$/d')
    done < $CSVFILE

    count=0
    for i in $phone_number
    do
        PHONES[$count]=$i
        count=$((count+1))
    done
}

function lplaca {
# devuelve las placas de los vehiculos para los clientes
#
    while read line; do
        placas=$(eval $(echo "awk -F',' '{print \$$placa}'")|sed '/^$/d')
    done < $CSVFILE
    #echo $placas
    count=0
    for i in $placas
    do
        PLACAS[$count]=$i
        count=$((count+1))
    done   
}

declare -a PAYMENTS

function payment {
# devuleve la "deuda total" que tenga el Cliente.
#
    while read line; do
        payments=$(eval $(echo "awk -F',' '{print \$$payment}'")|sed '/^$/d')
    done < $CSVFILE
    count=0
    for i in $payments; do
        PAYMENTS[$count]=$i
        count=$((count+1))
    done
} 


if [ -n "$device" ]; then
    echo "Read devices..."
fi

echo "Read names..."
fname $line
echo "Read phone numbers..."
pnumber $line
echo "Read placas...."
lplaca $line

# Optional argument     
if [ $payment ]; then
    echo -e "Read payment\n"
    payment $line
    if ((${#NAMES[*]} != ${#PAYMENTS[*]})); then
        echo "NAMES: ${#NAMES[*]}"
        echo "PAYMENTS: ${#PAYMENTS[*]}"
        echo -e "Error: un usuario no tiene Payment\n"
        exit 1
    fi
fi


if (( ${#NAMES[*]} == ${#PHONES[*]} && ${#NAMES[*]} == ${#PLACAS[*]} )); then
    echo -e "Procesando MESSAGE"
    separate
else
    echo "Error: un usuario no tiene número telefonico o no existe el usuario o faltan las placas."
    echo -e "NAMES: ${#NAMES[*]}"
    echo -e "PHONES: ${#PHONES[*]}"
    echo -e "PLACAS: ${PLACAS[*]}"
    exit 1
fi

#
#rm -rf send_error.log
echo "plate,,name,,phone,payment,$(date +"%d-%m-%Y %T")," >> send_error.log

echo -e "Start To Sending\n"
echo "#####################################################"
count=1
for i in ${!NAMES[*]}
do
    name=${NAMES[$i]}
    placa=${PLACAS[$i]}
    payment=${PAYMENTS[$i]}

    sms=$(echo $SMSTEXT|sed 's/$name/'$name'/g') 
    sms=$(echo $sms|sed 's/$placa/'$placa'/g') 
    sms=$(echo $sms|sed 's/$payment/'$payment'/g') 
    
    chart_count=$(echo $sms|wc -m)
    #printf "%4d [Chart Count: %s] - [%s]:\t" $i $chart_count ${PHONES[$i]}
    #echo $sms
    ## Descomentar para usar el modem:
    ##echo $sms|gammu sendsms TEXT ${PHONES[$i]}
    ##
    ##echo "RETURN GAMMU: $?"


    # Enviar a varios Celulares:
    for c in $(echo ${PHONES[$i]}|sed 's/|/\n/g'|cut -f1); do
        #printf "%4d [Chart Count: %s] - [%s]:\t" $i $chart_count $c
        printf "%4d [Chart Count: %s] - [%s]:\t" $count $chart_count $c
        echo $sms
        # Descomentar para usar el modem:
        echo $sms|gammu sendsms TEXT $c
        # Salida de Error: 
        if (( $?!=0 )); then
            echo "$placa,,$name,,$c,$payment,$(date +"%d-%m-%Y %T"),TRUE" >> send_error.log
        fi
        echo -e "\n"
        count=$((count+1))
    done
done

exit 0
