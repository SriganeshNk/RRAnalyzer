cp message.txt temp.txt
cat temp.txt | sed '1,7d' | head -n -15 > message.txt
rm temp.txt *.pdf
python diagnose.py
