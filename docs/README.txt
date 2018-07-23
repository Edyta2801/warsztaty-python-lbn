[Linux]
Środowisko wirtualenv Python 3.6.5 znajduje się w katalogu amelia-env.
Uruchomienie:
    source amelia-env/bin/activate
    python src/app.py

[Windows]
W systemie powinien być zainstalowany Python 3.6.5 w wersji 64bit
z uprawnieniami administratora.
Środowisko i biblioteki znajdują się w archiwum amelia-env-win.zip.
Po rozpakowaniu archiwum:
   .\amelia-env-win\Scripts\activate (w cmd)
   source amelia-env-win\Scripts\activate (w git bash)
   python src/app.py

W przypadku niezgodności środowiska należy stworzyć je samodzielnie
https://docs.python.org/3.6/library/venv.html

Instalacja modułów zależnych: pip install -r /path/to/requirements.txt
