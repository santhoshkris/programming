<?php
//Iterative way
$num = 4;
$fact = 1;
for ($i = $num; $i >= 1; $i--) {
    $fact *= $i;
}
echo "Factorial of $num is $fact \n";

// Recursive way
function fact($num)
{
    if ($num == 1) {
        return $num;
    } else {
        return $num * fact($num - 1);
    }
}
echo FACT(6) . "\n";

//Using array_reduce
$n = 6;
$a = range(1, $n);
print_r($a);
$p = array_reduce($a, function ($c, $i) {
    return $c *= $i;
}, 1);
echo "factorial of {$n} is {$p}\n";
