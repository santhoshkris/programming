<?php

$input = "isogram";
$input_arr = str_split($input);
$input_count = array_count_values($input_arr);
//print_r($input_count);
foreach($input_count as $count){
    if ($count > 1){
        echo "Not an Isogram\n";
        exit();
    }
}
echo "Valid Isogram \n";
