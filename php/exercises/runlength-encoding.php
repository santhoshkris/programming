<?php
echo "RUN LENGTH ENCODING";
$input = "hheellllowwworlllddg";
echo "The input string is : $input \n";
$output = "";
$input_arr = str_split($input);
$output_arr = [];
$i = 1;
$count = 1;
while ($i < count($input_arr)) {
    // echo $i . ' ' . $input_arr[$i-1] . ' ' . $input_arr[$i] . "\n";
    if ($input_arr[$i] !== $input_arr[$i - 1]) {
        if ($count > 1) {
            $output = $output . $count . $input_arr[$i - 1];
            $count = 1;
        } else {
            $output = $output . $input_arr[$i - 1];
        }
        if (($i + 1) == count($input_arr)) {
            $output = $output . $input_arr[$i];
        }
    } else {
        $count++;
        //echo $i+1 . ' ' . "\n";
        if (($i + 1) == count($input_arr)) {
            $output = $output . $count . $input_arr[$i - 1];
        }
    }
    $i++;
}
echo "The encoded string is : $output \n";
