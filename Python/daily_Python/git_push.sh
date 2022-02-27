Y=$(date + %Y)
M=$(date + %m)
D=$(date + %d)

Ym=$Y-$M
Ymd=%Y-%M-%d
GitRep="TIL"

HomeDir="/Users/heojaehun/gitRepo"
GitDir="$HomeDir/$GitRep"

echo "push git from $GitDir --> $GitRep"

cd $GitDir
git init
git add .
git commit -m "commit $Ymd"
git push origin master
