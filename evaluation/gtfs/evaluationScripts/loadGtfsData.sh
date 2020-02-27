  #!/bin/bash
  i=$1
  
  cp /data/gtfs/gtfs$i/* /data/
  echo "EVALUATING GTFS-$i" > /results/log.txt