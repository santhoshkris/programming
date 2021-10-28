<?php

$in = '111101';
//echo bindec($in);
$dec = 0;
$in_arr = array_reverse(str_split($in));
$in_assoc = array_values($in_arr);
//print_r($in_assoc);
foreach ($in_assoc as $k => $v) {
    $dec += ($v * pow(2, $k));
}
echo "Binary is : $in, the Decimal equivalent is : $dec\n";
