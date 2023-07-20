#!/bin/bash

python3 pxldis.py pattern.pxl > pattern.dis
python3 pxlasm.py pattern.dis > pattern2.pxl
diff -y <(xxd pattern.pxl) <(xxd pattern2.pxl)


python3 pxldis.py pattern2.pxl > pattern2.dis
diff pattern.dis pattern2.dis
