<?php
$a = [1, 2, 3, 4, 5, 6, 7, 8];
$b = array_filter($a, function ($i) {
    return $i % 2 === 0;
});
print_r($b);
