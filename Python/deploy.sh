# posFARMlrn package 화 해주는 shell script.
# '1. remove posFARMlrn  
# '2. remove ./build file
# '3. execute createDlInitFile.py file
# ;4. setup.py install.

rm -rf /opt/anaconda3/lib/python3.5/site-package/posFARMlrn
rm -rf ./build
/opt/anaconda3/bin/python3 /model_data/p/cm/src/python/dl/createDlInitFile.py
/opt/anaconda3/bin/python3 /model_data/p/cm/src/python/dl/setup.py install
