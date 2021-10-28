<?php
$a = [1, 2, 3, 4, 5, 6];
// $b = array_map(function ($i) {
//     return $i * $i;
// }, $a);
// print_r($b);

array_walk($a, function (&$i) {
    $i *= $i;
});
print_r($a);
