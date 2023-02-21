declare -A map=([hello]='world' [long]='long long long string' [what is it]=123)

for i in "${!map[@]}"; 
do
    echo "${i}"
done