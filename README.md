downhill miner
=======

try to group [downhill pictures](http://www.wiriehorn.ch/sommer/bikepark/live-jump) by rider.

```
pip install -r requirements.txt
python download.py
python crop.py
python cluster.py
```

You may want to configure the number of clusters ```K``` in ```cluster.py``` before clustering. 
