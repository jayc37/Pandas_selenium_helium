ECHO OFF
echo --------------------------------------------	PUSH DATA BY SO KHUNG----------------------------------------
echo   ****************************************************************************
echo -*									-*
echo -*				 				-*
echo -*								-*
echo -*									-*
echo  ****************************************************************************
cd src
cd setting
pip install -r requirements.txt
echo -- Runing ......
cd ..
python run.py
pause
