<?php

/* Largest series */

$input = '1027839564';
$len = 5;
// $input = '73167176531330624919225119674426574742355349194934';
// $len=6;
$prod = 0;
$substr = "";
$i = 0;
while ($i < strlen($input) - $len) {
    $val = array_product(str_split(substr($input, $i, $len)));
    if ($val > $prod) {
        $prod = $val;
        $substr = substr($input, $i, $len);
    }
    $i++;
}
$substr_arr = str_split($substr);
$substr_arr_joined = implode('*', $substr_arr);
echo "The largest series of $len is : $substr_arr_joined = $prod \n";
