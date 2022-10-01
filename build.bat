python -m nuitka --standalone  --enable-plugin=numpy estarter.py
md estarter.dist\s
copy  s estarter.dist\s
copy config_default.ini estarter.dist\config_default.ini
copy null estarter.dist/np.cf
pause