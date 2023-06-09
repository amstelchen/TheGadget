#!/bin/bash

if [[ -z $1 || -z $2 ]]; then
    echo "parameters missing."
    exit
fi
echo $1
P=$1
#L=$1:l
L=${P@L}
LNG=$2

echo "Creating system-wide startup script..."
sudo cp -v ~/.local/bin/$L /usr/bin/$L
echo "Creating system-wide icon..."
sudo cp -v $1.png /usr/share/pixmaps/$1.png
echo "Creating system-wide desktop entry..."
sudo cp -v $1.desktop /usr/share/applications/$1.desktop
echo "Creating local desktop entry..."
cp -v $1.desktop ~/Desktop/$1.desktop

echo "Creating translations..."
#xgettext -d $1 -o $1/locales/$1.pot $1/*.py

#L="nl"; LC="LC_MESSAGES"; mkdir -p $L/$LC ; msginit -l $L -o $L/$LC/windmin.po && msgfmt -o $L/$LC/windmin.mo $L/$LC/windmin.po
#for L in nl hu uk fr es; do
#    LC="LC_MESSAGES"
#    mkdir -p $1/locales/$L/$LC
#    msginit -l $L -i $1/locales/$1.pot -o $1/locales/$L/$LC/$1.po
#    msgfmt -o $1/locales/$L/$LC/$1.mo $1/locales/$L/$LC/$1.po
#done

#poedit 2>/dev/null
#sudo cp -v $1/locales/de/LC_MESSAGES/*.mo /usr/share/locale/de/LC_MESSAGES/
echo "Syntax check..."
flake8 . --count --exit-zero --max-complexity=22 --max-line-length=127 --ignore=E116,E128,E265,E401,F40,F841,W291,E402
if [ $? -eq 0 ]; then
    echo "No errors."
else
    echo "Failed!"
fi
poetry build
pip install dist/$L-0.1.0-py3-none-any.whl --force-reinstall
exec /usr/bin/$L

#python setup.py sdist
#python -m build --wheel --no-isolation
#updpkgsums
#makepkg -fci