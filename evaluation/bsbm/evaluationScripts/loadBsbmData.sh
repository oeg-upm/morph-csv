  #!/bin/bash
  i=$1
  
  cp /data/bsbm/bsbm$i/* /data/
  echo "EVALUATING bsbm-$i" > /results/log.txt