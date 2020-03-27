  #!/bin/bash
  i=$1
  
  cp /data/bsbm/bsbm$i/*.csv /data/
  echo "EVALUATING bsbm-$i" > /results/log.txt