fileToRemove="./bentoml_update.sh"
rm "$fileToRemove" 2> /dev/null

if [ $? -eq 0 ]; then
    echo "Success removing file: $fileToRemove"
else
    echo "File is not exist : $fileToRemove"
fi