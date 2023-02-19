#!/bin/bash
python ./update_bentoml_model.py

write_bentoml_yaml()
{
cat << __END__
service: "service:svc"
include:
  - "src/service.py"
  - "src/config.py"
python:
  requirements_txt: "requirements.txt"
__END__
}

BENTO_YAML_FILE="./bentoml.yaml"

## check to exist a file 'bentoml.yaml'
if [ -f "$BENTO_YAML_FILE" ]; then
    echo "'$BENTO_YAML_FILE' is exists."
else
    write_bentoml_yaml > $BENTO_YAML_FILE
    echo "''$BENTO_YAML_FILE' created"
fi