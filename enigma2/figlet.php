<?php
if(isset($_GET['string'])) {
  echo shell_exec('figlet -f slant '.$_GET['string']);
}
?>
