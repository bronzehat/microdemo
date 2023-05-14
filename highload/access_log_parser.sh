!/bin/bash
# Примеры команд для подсчёта статистики

# Количество запросов с сортировкой по часам
cat access.log | cut -d[ -f2 | cut -d] -f1 | awk -F: '{print $2":00"}' | sort -n | uniq -c

# request per second with method and return code
cat access.log | awk '{print $4" "$7" "$8" "$9" "$10}'| tr -d \"\[\]| sort -n | uniq -c

# request per minute with method and return code
cat access.log | awk '{$4=substr($4,2,17);print}' | awk '{print $4" "$7" "$8" "$9" "$10}'| tr -d \"\[\]| sort -n | uniq -c

# request per hour by date
grep "23/Jan" access.log | cut -d[ -f2 | cut -d] -f1 | awk -F: '{print $2":00"}' | sort -n | uniq -c

# request per hour by IP
grep "XX.XX.XX.XX" access.log | cut -d[ -f2 | cut -d] -f1 | awk -F: '{print $2":00"}' | sort -n | uniq -c

# requests per minute:
cat access.log | cut -d[ -f2 | cut -d] -f1 | awk -F: '{print $2":"$3}' | sort -nk1 -nk2 | uniq -c

# requests per minute for date:
grep "02/Nov/2017" access.log | cut -d[ -f2 | cut -d] -f1 | awk -F: '{print $2":"$3}' | sort -nk1 -nk2 | uniq -c

# requests per minute for url:
grep "[url]" access.log | cut -d[ -f2 | cut -d] -f1 | awk -F: '{print $2":"$3}' | sort -nk1 -nk2 | uniq -c

# per IP per minute
grep "XX.XX.XX.XX" access.log | cut -d[ -f2 | cut -d] -f1 | awk -F: '{print $2":"$3}' | sort -nk1 -nk2 | uniq -c