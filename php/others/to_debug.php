<?php

function step_over() {
    echo 'stepping over';
}

function step_into() {
    step_over();
}

for ($i=0; $i < 100; $i++) {
    step_into();
}

?>
