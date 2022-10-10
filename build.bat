python -m nuitka --standalone --include-package=estarter  estarter.py
md estarter.dist\s
copy  s estarter.dist\s
copy config_default.ini estarter.dist\config_default.ini
type nul>> estarter.dist\np.cf
pause