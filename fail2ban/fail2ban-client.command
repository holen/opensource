Commands
Jump to: navigation, search

The commands presented above can be executed using:

$ fail2ban-client <COMMAND>

or by typing them in the interactive console available with:

$ fail2ban-client -i

BASIC
Command        Description
start      starts the server and the jails
reload         reloads the configuration
reload <JAIL>      reloads the jail <JAIL>
stop       stops all jails and terminate the server
status         gets the current status of the server
ping       tests if the server is alive
help       return this output

LOGGING
Command        Description
set loglevel <LEVEL>       sets logging level to <LEVEL>. 0 is minimal, 4 is debug
get loglevel       gets the logging level
set logtarget <TARGET>         sets logging target to <TARGET>. Can be STDOUT, STDERR, SYSLOG or a file
get logtarget      gets logging target
JAIL CONTROL
Command        Description
add <JAIL> <BACKEND>       creates <JAIL> using <BACKEND>
start <JAIL>       starts the jail <JAIL>
stop <JAIL>        stops the jail <JAIL>. The jail is removed
status <JAIL>      gets the current status of <JAIL>

JAIL CONFIGURATION
Command        Description
off        sets the idle state of <JAIL>
set <JAIL> addignoreip <IP>        adds <IP> to the ignore list of <JAIL>
set <JAIL> delignoreip <IP>        removes <IP> from the ignore list of <JAIL>
set <JAIL> addlogpath <FILE>       adds <FILE> to the monitoring list of <JAIL>
set <JAIL> dellogpath <FILE>       removes <FILE> from the monitoring list of <JAIL>
set <JAIL> addfailregex <REGEX>        adds the regular expression <REGEX> which must match failures for <JAIL>
set <JAIL> delfailregex <INDEX>        removes the regular expression at <INDEX> for failregex
set <JAIL> addignoreregex <REGEX>      adds the regular expression <REGEX> which should match pattern to exclude for <JAIL>
set <JAIL> delignoreregex <INDEX>      removes the regular expression at <INDEX> for ignoreregex
set <JAIL> findtime <TIME>         sets the number of seconds <TIME> for which the filter will look back for <JAIL>
set <JAIL> bantime <TIME>      sets the number of seconds <TIME> a host will be banned for <JAIL>
set <JAIL> usedns <VALUE>      sets the usedns mode for <JAIL>
set <JAIL> banip <IP>      manually Ban <IP> for <JAIL>
set <JAIL> unbanip <IP>        manually Unban <IP> in <JAIL>
set <JAIL> maxretry <RETRY>        sets the number of failures <RETRY> before banning the host for <JAIL>
set <JAIL> addaction <ACT>         adds a new action named <NAME> for <JAIL>
set <JAIL> delaction <ACT>         removes the action <NAME> from <JAIL>
set <JAIL> setcinfo <ACT> <KEY> <VALUE>        sets <VALUE> for <KEY> of the action <NAME> for <JAIL>
set <JAIL> delcinfo <ACT> <KEY>        removes <KEY> for the action <NAME> for <JAIL>
set <JAIL> actionstart <ACT> <CMD>         sets the start command <CMD> of the action <ACT> for <JAIL>
set <JAIL> actionstop <ACT> <CMD>      sets the stop command <CMD> of the action <ACT> for <JAIL>
set <JAIL> actioncheck <ACT> <CMD>         sets the check command <CMD> of the action <ACT> for <JAIL>
set <JAIL> actionban <ACT> <CMD>       sets the ban command <CMD> of the action <ACT> for <JAIL>
set <JAIL> actionunban <ACT> <CMD>         sets the unban command <CMD> of the action <ACT> for <JAIL>

JAIL INFORMATION
Command        Description
get <JAIL> logpath         gets the list of the monitored files for <JAIL>
get <JAIL> ignoreip        gets the list of ignored IP addresses for <JAIL>
get <JAIL> failregex       gets the list of regular expressions which matches the failures for <JAIL>
get <JAIL> ignoreregex         gets the list of regular expressions which matches patterns to ignore for <JAIL>
get <JAIL> findtime        gets the time for which the filter will look back for failures for <JAIL>
get <JAIL> bantime         gets the time a host is banned for <JAIL>
get <JAIL> usedns      gets the usedns setting for <JAIL>
get <JAIL> maxretry        gets the number of failures allowed for <JAIL>
get <JAIL> addaction       gets the last action which has been added for <JAIL>
get <JAIL> actionstart <ACT>       gets the start command for the action <ACT> for <JAIL>
get <JAIL> actionstop <ACT>        gets the stop command for the action <ACT> for <JAIL>
get <JAIL> actioncheck <ACT>       gets the check command for the action <ACT> for <JAIL>
get <JAIL> actionban <ACT>         gets the ban command for the action <ACT> for <JAIL>
get <JAIL> actionunban <ACT>       gets the unban command for the action <ACT> for <JAIL>
get <JAIL> cinfo <ACT> <KEY>       gets the value for <KEY> for the action <ACT> for <JAIL> 
