<?php
$orig_num = 371;
$num = 371;
$sum = 0;
while ($num > 0) {
    // echo $num%10;
    $sum += pow(($num % 10), 3);
    $num = floor($num / 10);
}
if ($sum == $num) echo "Hello";
echo ($sum == $orig_num) ? "$orig_num is an Armstrong number\n" : "$orig_num is not an Armstrong number\n";
