#!/usr/bin/php

<?php

function showHelp()
{
    echo "Usage: php test_con.php <command>
    
    command can be:
    - i: info - gets relay status info
    - o: on - turn on the relay
    - s: stop - turn off the relay
    - r: read: read temperature info\n";
    return;
}
    
// We need exactely one parameter
if(count($argv) != 2) {
    showHelp();
    return;
}

// And the parameter must be a regular command
if(! in_array($argv[1], ['i', 'o', 's', 'r'])) {
    showHelp();
    return;
} 

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
$result = socket_connect($socket, '127.0.0.1', '7999');

socket_write($socket, $argv[1]);

# Read the response length
$responseLength = ord(socket_read($socket, 1));
#var_dump(ord($responseLength));
#socket_close($socket);

$response = socket_read($socket, $responseLength);

socket_close($socket);

echo "$response\n";
