<?php

/* Luhn's Algorithm */

//$input = '4539 3195 0343 6467';
//$input = '8273 1232 7352 0569';
$input = $argv[1];
$input_arr = str_split($input);
$trimmed_arr=[];
// print_r($input_arr);
foreach($input_arr as $num){
    if ($num !== ' ')
        $trimmed_arr[]=$num;
}
//print_r($trimmed_arr);
for($i=count($trimmed_arr)-2;$i>=0;$i=$i-2){
   if (($trimmed_arr[$i]*2) > 9){
       $trimmed_arr[$i]=($trimmed_arr[$i]*2)-9;
   }else{
      $trimmed_arr[$i]=$trimmed_arr[$i]*2;
   }
}
echo (array_sum($trimmed_arr)%10 == 0)? "A valid number\n" : "Not a valid number\n";
