<?php

$array = [];

for ($i = 1; $i <= 10; $i++) {
    if ($i < 4) {
        $array[] = "a";
    }elseif ($i >=4 or $i <= 7) {
        $array[] = "b";
    }elseif ($i >= 8) {
        $array[] = "c";
    }
}
var_dump($array);
?>
