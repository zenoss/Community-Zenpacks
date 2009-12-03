#!/bin/bash 
#
# Program: Domain Expiration Check <domain-check>
#
# Author: Matty < matty91 at gmail dot com >
#
# Current Version: 1.6
#
# Revision History:
#
#  Version 1.6
#    Added support for .uk and second-level domains Added Nagios support and return codes. -- Chris Hubbard <guyverix@yahoo.com>
#
#  Version 1.5
#    Added support for .org, .in, .biz and .info domain names -- Vivek Gite <vivek@nixcraft.com>
# 
#  Version 1.4
#    Updated the documentation.
#
#  Version 1.3
#    Gracefully Handle the case where the expiration data is unavailable
#
#  Version 1.2
#    Added "-s" option to allow arbitrary registrars
#
#  Version 1.1
#    Fixed issue with 'e' getopt string -- Pedro Alves
#
#  Version 1.0
#    Initial Release
#
# Last Updated: 12-Aug-2007
#
# Purpose:
#  domain-check checks to see if a domain has expired. domain-check
#  can be run in interactive and batch mode, and provides faciltities 
#  to alarm if a domain is about to expire.
#
# License:
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# Notes:
#   Since each registrar provides expiration data in a unique format (if
#   they provide it at all), domain-check is currently only able to
#   processess expiration information for a subset of the available
#   registrars.
#
# Requirements:
#   Requires whois
#
# Installation:
#   Copy the shell script to a suitable location
#
# Tested platforms:
#  -- Solaris 9 using /bin/bash
#  -- Solaris 10 using /bin/bash
#  -- OS X 10.4.2 using /bin/sh
#  -- OpenBSD using /bin/sh
#  -- FreeBSD using /bin/sh
#  -- Redhat advanced server 3.0MU3 using /bin/sh
#
# Usage:
#  Refer to the usage() sub-routine, or invoke domain-check
#  with the "-h" option.
#
# Example:
#
#  The first example will print the expiration date and registrar for prefetch.net:
#
#  $ domain-check.sh -d prefetch.net
#
#  Domain                              Registrar         Status   Expires     Days Left
#  ----------------------------------- ----------------- -------- ----------- ---------
#  prefetch.net                        INTERCOSMOS MEDIA Valid    13-feb-2006   64   
#
#  The second example prints the expiration date and registrar for the domains 
#  listed in the file "domains":
#
#  $ domain-check.sh -f domains    
#
#  Domain                              Registrar         Status   Expires     Days Left
#  ----------------------------------- ----------------- -------- ----------- ---------
#  sun.com                             NETWORK SOLUTIONS Valid    20-mar-2010   1560 
#  google.com                          EMARKMONITOR INC. Valid    14-sep-2011   2103 
#  ack.com                             NETWORK SOLUTIONS Valid    09-may-2008   880  
#  prefetch.net                        INTERCOSMOS MEDIA Valid    13-feb-2006   64   
#  spotch.com                          GANDI             Valid    03-dec-2006   357  
#
#  The third example will e-mail the address admin@yourdomain.com with the domains that
#  will expire in 60-days or less:
#
#  $ domain-check -a -f domains -q -x 60 -e admin@yourdomain.com
#

PATH=/bin:/usr/bin:/usr/local/bin:/usr/local/ssl/bin:/usr/sfw/bin ; export PATH

# Who to page when an expired domain is detected (cmdline: -e)
# changed to root@localhost for safety
ADMIN="root@localhost"

# Number of days in the warning threshhold  (cmdline: -x)
WARNDAYS=14

# If QUIET is set to TRUE, don't print anything on the console (cmdline: -q)
QUIET="FALSE"

# Don't send emails by default (cmdline: -a)
ALARM="FALSE"

# Whois server to use (cmdline: -s)
WHOIS_SERVER="whois.internic.org"

# Location of system binaries
AWK="/usr/bin/awk"

#WHOIS="/usr/bin/whois"
#Ubuntu users should probably use jwhois since it caches and is VERY fast.
WHOIS="/usr/bin/jwhois"

DATE="/bin/date"
CUT="/usr/bin/cut"
# Place to stash temporary files
WHOIS_TMP="/var/tmp/whois.$$"

#############################################################################
# Purpose: Convert a date from MONTH-DAY-YEAR to Julian format
# Acknowledgements: Code was adapted from examples in the book
#                   "Shell Scripting Recipes: A Problem-Solution Approach"
#                   ( ISBN 1590594711 )
# Arguments:
#   $1 -> Month (e.g., 06)
#   $2 -> Day   (e.g., 08)
#   $3 -> Year  (e.g., 2006)
#############################################################################
date2julian() 
{
    if [ "${1} != "" ] && [ "${2} != ""  ] && [ "${3}" != "" ]
    then
         ## Since leap years add aday at the end of February, 
         ## calculations are done from 1 March 0000 (a fictional year)
         d2j_tmpmonth=$((12 * ${3} + ${1} - 3))
        
          ## If it is not yet March, the year is changed to the previous year
          d2j_tmpyear=$(( ${d2j_tmpmonth} / 12))
        
          ## The number of days from 1 March 0000 is calculated
          ## and the number of days from 1 Jan. 4713BC is added 
          echo $(( (734 * ${d2j_tmpmonth} + 15) / 24 -  2 * ${d2j_tmpyear} + ${d2j_tmpyear}/4
                        - ${d2j_tmpyear}/100 + ${d2j_tmpyear}/400 + $2 + 1721119 ))
    else
          echo 0
    fi
}

#############################################################################
# Purpose: Convert a string month into an integer representation
# Arguments:
#   $1 -> Month name (e.g., Sep)
#############################################################################
getmonth() 
{
       LOWER=`tolower $1`
              
       case ${LOWER} in
             jan) echo 1 ;;
             feb) echo 2 ;;
             mar) echo 3 ;;
             apr) echo 4 ;;
             may) echo 5 ;;
             jun) echo 6 ;;
             jul) echo 7 ;;
             aug) echo 8 ;;
             sep) echo 9 ;;
             oct) echo 10 ;;
             nov) echo 11 ;;
             dec) echo 12 ;;
               *) echo  0 ;;
       esac
}

#############################################################################
# Purpose: Calculate the number of seconds between two dates
# Arguments:
#   $1 -> Date #1
#   $2 -> Date #2
#############################################################################
date_diff() 
{
        if [ "${1}" != "" ] &&  [ "${2}" != "" ]
        then
                echo $(expr ${2} - ${1})
        else
                echo 0
        fi
}

##################################################################
# Purpose: Converts a string to lower case
# Arguments:
#   $1 -> String to convert to lower case
##################################################################
tolower() 
{
     LOWER=`echo ${1} | tr [A-Z] [a-z]`
     echo $LOWER
}

##################################################################
# Purpose: Access whois data to grab the registrar and expiration date
# Arguments:
#   $1 -> Domain to check
##################################################################
check_domain_status() 
{
    # Avoid WHOIS LIMIT EXCEEDED - slowdown our whois client by adding 3 sec 
        if [ "${NAGIOS}" != "TRUE" ]
        then
	    sleep 5
	fi
    # Save the domain since set will trip up the ordering
    DOMAIN=${1}
#    TLDTYPE="`echo ${DOMAIN} | cut -d '.' -f2 | tr '[A-Z]' '[a-z]'`" 

## Changed to allow domain.second-level.type
    TLDTYPE="`echo ${DOMAIN} | awk -F '.' '{print $NF}' | tr '[A-Z]' '[a-z]'`" 

# Invoke whois to find the domain registrar and expiration date
#${WHOIS} -h ${WHOIS_SERVER} "=${1}" > ${WHOIS_TMP}
# Let whois select server 
    if [ "${TLDTYPE}"  == "org" ];
    then
        ${WHOIS} -h "whois.pir.org" "${1}" > ${WHOIS_TMP}
    elif [ "${TLDTYPE}"  == "in" ];
    then
        ${WHOIS} -h "whois.registry.in" "${1}" > ${WHOIS_TMP}
    elif [ "${TLDTYPE}"  == "biz" ];
    then
        ${WHOIS} -h "whois.neulevel.biz" "${1}" > ${WHOIS_TMP}
    elif [ "${TLDTYPE}"  == "uk" ];
    then
        ${WHOIS} -h "whois.nic.uk" "${1}" > ${WHOIS_TMP}
    elif [ "${TLDTYPE}"  == "info" ];
    then
        ${WHOIS} -h "whois.afilias.info" "${1}" > ${WHOIS_TMP}
    elif [ "${TLDTYPE}"  == "com" -o "${TLDTYPE}"  == "net" -o "${TLDTYPE}"  == "edu" ];
    then
	${WHOIS} -h ${WHOIS_SERVER} "=${1}" > ${WHOIS_TMP}
    else
	${WHOIS} "${1}" > ${WHOIS_TMP}
    fi

#####
    # Parse out the expiration date and registrar -- uses the last registrar it finds
    if [ "${TLDTYPE}"  == "us" ];
    then
	REGISTRAR=`cat ${WHOIS_TMP} | grep "Created by Registrar:" | ${AWK} -F: '{print $2}' | awk '{sub(/^[ \t]+/, "")};1'`
    elif [ "${TLDTYPE}"  == "uk" ];
    then
	REGISTRAR=`cat ${WHOIS_TMP} | grep -i "Registrar" -A 1 | tr -d '\n' | ${AWK} -F: '{print $2}' | awk '{sub(/^[ \t]+/, "")};1' | awk -F'[' '{print $1}'`
    else
	REGISTRAR=`cat ${WHOIS_TMP} | ${AWK} -F: '/Registrar/ && $2 != ""  { REGISTRAR=substr($2,2,17) } END { print REGISTRAR }'`
    fi

#####


    # If the Registrar is NULL, then we didn't get any data
    if [ "${REGISTRAR}" = "" ]
    then
        prints "$DOMAIN" "Unknown" "Unknown" "Unknown" "Unknown"
        return
    fi

    # The whois Expiration data should resemble teh following: "Expiration Date: 09-may-2008"

    # for .in, .info, .org domains
    if [ "${TLDTYPE}" == "in" -o "${TLDTYPE}" == "info" -o "${TLDTYPE}" == "org" ];
    then
	    DOMAINDATE=`cat ${WHOIS_TMP} | ${AWK} '/Expiration Date:/ { print $2 }' | cut -d':' -f2`
    elif [ "${TLDTYPE}" == "uk" -o "${TLDTYPE}" == "uk"  ]; # for .uk addresses only
    then
             DOMAINDATE=`cat ${WHOIS_TMP} | awk '/Renewal/ { print $NF }'`
    elif [ "${TLDTYPE}" == "biz" -o "${TLDTYPE}" == "us"  ]; # for .biz domain and .us?
    then
            DOMAINDATE=`cat ${WHOIS_TMP} | awk '/Domain Expiration Date:/ { print $6"-"$5"-"$9 }'`
    else # .com, .edu, .net and may work with others	 
	    DOMAINDATE=`cat ${WHOIS_TMP} | ${AWK} '/Expiration/ { print $NF }'`	
    fi

    #echo $DOMAINDATE # debug 
    # Whois data should be in the following format: "13-feb-2006"
    IFS="-"
    set -- ${DOMAINDATE}
    MONTH=$(getmonth ${2})
    IFS=""

    # Convert the date to seconds, and get the diff between NOW and the expiration date
    DOMAINJULIAN=$(date2julian ${MONTH} ${1#0} ${3})
    DOMAINDIFF=$(date_diff ${NOWJULIAN} ${DOMAINJULIAN})

    if [ ${DOMAINDIFF} -lt 0 ]
    then
          if [ "${ALARM}" = "TRUE" ]
          then
                echo "The domain ${DOMAIN} has expired!" \
                | /bin/mail -s "Domain ${DOMAIN} has expired!" ${ADMIN}
           fi
	if [ "${NAGIOS}" = "TRUE" ]
        then
	echo "Status Critical Domain expired. | Domain ${DOMAIN} has expired!"
	exit 2
	else

           prints ${DOMAIN} "Expired" "${DOMAINDATE}" "${DOMAINDIFF}" ${REGISTRAR}
	fi
    elif [ ${DOMAINDIFF} -lt ${WARNDAYS} ]
    then
           if [ "${ALARM}" = "TRUE" ]
           then
		    echo "The domain ${DOMAIN} will expire on ${DOMAINDATE}" \
                    | /bin/mail -s "Domain ${DOMAIN} will expire in ${WARNDAYS}-days or less" ${ADMIN}
            fi
	if [ "${NAGIOS}" = "TRUE" ]
        then
	echo "Status Warn Domain expire days=${DOMAINDIFF} | Domain ${DOMAIN} will expire in ${WARNDAYS} -days or less.  Days=${DOMAINDIFF} "
	exit 1
	else
            prints ${DOMAIN} "Expiring" "${DOMAINDATE}" "${DOMAINDIFF}" "${REGISTRAR}"
	fi
     else
	if [ "${NAGIOS}" != "TRUE" ]
	then
            prints ${DOMAIN} "Valid" "${DOMAINDATE}"  "${DOMAINDIFF}" "${REGISTRAR}"
	else
	echo "Status OK | ${DOMAIN} Valid ${DOMAINDATE} ${REGISTRAR} Days=${DOMAINDIFF}"
	fi
     fi
}

####################################################
# Purpose: Print a heading with the relevant columns
# Arguments:
#   None
####################################################
print_heading()
{
        if [ "${QUIET}" != "TRUE" ]
        then
		if [ "${NAGIOS}" != "TRUE" ]
		then
                printf "\n%-39s %-20s %-8s %-11s %-5s\n" "Domain" "Registrar" "Status" "Expires" "Days Left"
                echo "--------------------------------------- -------------------- -------- ----------- ---------"
		fi
        fi
}

#####################################################################
# Purpose: Print a line with the expiraton interval
# Arguments:
#   $1 -> Domain
#   $2 -> Status of domain (e.g., expired or valid)
#   $3 -> Date when domain will expire
#   $4 -> Days left until the domain will expire
#   $5 -> Domain registrar
#####################################################################
prints()
{
    if [ "${QUIET}" != "TRUE" ]
    then
	if [ "${NAGIOS}" != "TRUE" ]
	then
            MIN_DATE=$(echo $3 | ${AWK} '{ print $1, $2, $4 }')
            printf "%-39s %-20s %-8s %-11s %-5s\n" "$1" "$5" "$2" "$MIN_DATE" "$4"
	fi
    fi
}

##########################################
# Purpose: Describe how the script works
# Arguments:
#   None
##########################################
usage()
{
        echo "Usage: $0 [ -e email ] [ -x expir_days ] [ -q ] [ -a ] [ -h ]"
        echo "          {[ -d domain_namee ]} || { -f domainfile}"
        echo ""
        echo "  -a               : Send a warning message through email "
        echo "  -d domain        : Domain to analyze (interactive mode)"
        echo "  -e email address : Email address to send expiration notices"
        echo "  -f domain file   : File with a list of domains"
        echo "  -h               : Print this screen"
        echo "  -s whois server  : Whois sever to query for information"
        echo "  -q               : Don't print anything on the console"
        echo "  -n               : Nagios style returns and exit codes"
        echo "  -x days          : Domain expiration interval (eg. if domain_date < days)"
        echo ""
}

### Evaluate the options passed on the command line
while getopts nae:f:hd:s:qx: option
do
        case "${option}"
        in
                a) ALARM="TRUE";;
                e) ADMIN=${OPTARG};;
                d) DOMAIN=${OPTARG};;
                f) SERVERFILE=$OPTARG;;
                s) WHOIS_SERVER=$OPTARG;;
                q) QUIET="TRUE";;
                x) WARNDAYS=$OPTARG;;
		n) NAGIOS="TRUE";;
                \?) usage
                    exit 1;;
        esac
done

### Check to see if the whois binary exists
if [ ! -f ${WHOIS} ]
then
	if [ "${NAGIOS}" = "TRUE" ]
	then
		echo "Status Warning script failure | missing bunary ${WHOIS} file ."
	else
        echo "ERROR: The whois binary does not exist in ${WHOIS} ."
        echo "  FIX: Please modify the \$WHOIS variable in the program header."
	fi
        exit 1
fi

### Check to make sure a date utility is available
if [ ! -f ${DATE} ]
then
	if [ "${NAGIOS}" = "TRUE" ]
        then
	echo "Status Warning script failure | missing binary date file."
	else
        echo "ERROR: The date binary does not exist in ${DATE} ."
        echo "  FIX: Please modify the \$DATE variable in the program header."
	fi
        exit 1
fi

### Baseline the dates so we have something to compare to
MONTH=$(${DATE} "+%m")
DAY=$(${DATE} "+%d")
YEAR=$(${DATE} "+%Y")
NOWJULIAN=$(date2julian ${MONTH#0} ${DAY#0} ${YEAR})

### Touch the files prior to using them
touch ${WHOIS_TMP}

### If a HOST and PORT were passed on the cmdline, use those values
if [ "${DOMAIN}" != "" ]
then
        print_heading
        check_domain_status "${DOMAIN}"
### If a file and a "-a" are passed on the command line, check all
### of the domains in the file to see if they are about to expire
elif [ -f "${SERVERFILE}" ]
then
        print_heading
        while read DOMAIN
        do
                check_domain_status "${DOMAIN}"

        done < ${SERVERFILE}

### There was an error, so print a detailed usage message and exit
else
        usage
        exit 1
fi

# Add an extra newline
echo

### Remove the temporary files
rm -f ${WHOIS_TMP}

### Exit with a success indicator
exit 0

