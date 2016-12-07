#! env bash

rm *.html
rm -rf lit

for i in cinemasqlpy cinemasqlpy.a
do 
pydoc $i > $i.md
markdown_py $i.md > $i.html
rm $i.md
done

for i in ../cinemasqlpy/*.py 
do 
pycco $i
done

mv docs lit

