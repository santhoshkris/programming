<?php

$num = $argv[1];
for ($i = 2; $i <= ($num / 2); $i++) {
    if (($num % $i) == 0) {
        echo "Number $num is not prime \n";
        exit();
    }
}
echo "Number $num is a prime number\n";
