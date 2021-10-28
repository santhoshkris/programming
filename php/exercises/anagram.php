<?php
$s1 = "abcd";
$s2 = "dabc";

$a = str_split($s1);
$b = str_split($s2);
sort($a);
sort($b);
echo count(array_intersect($a, $b)) . "\n";
print_r(array_diff($a, $b));
