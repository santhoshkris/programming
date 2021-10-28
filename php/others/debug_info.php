
<?php
/**
* Printing some DEBUG INFO
*/

$myVar = "hello world!";
// var_dump($myVar);

// $flowers = array("daisy", "marigold", "sunflower");
// var_dump($flowers);

// $grades = array("Jim" => 8.0, "John" => 8.5, "Clara" => 9.0);
// // var_dump($grades);
// print_r($grades);

// print_r($flowers);

// $allVars = get_defined_vars();
// print_r($allVars);

function sayHello($hello) {
    echo $hello . "<br/>";
    debug_print_backtrace();
}

sayHello($myVar);

?>
