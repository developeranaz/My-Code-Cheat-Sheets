GNU nano 7.2                       a.sh
#!/bin/bash

# Set numvar1 as a constant
numvar1=1

# Read numvar2 from the file "pnum"
if [ -f "pnum" ]; then
  # Read numvar2 from the file "pnum"
  numvar2=$(<pnum)
else
  # If "pnum" doesn't exist, create it with an initial value of 0
  echo 0 > pnum
  numvar2=0
fi


# Add numvar1 and numvar2 and save the result in numvar3
numvar3=$((numvar1 + numvar2))
echo $numvar3 >pnum
# Check if numvar3 is greater than 5
if [ $numvar3 -gt 5 ]; then
  echo "Number is greater than five"
  echo 0 >pnum
fi

echo $numvar3
