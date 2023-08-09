# Mapper
Mapper is a python script which generates Enigma mappings from MCP's old and recent mapping

## Requirements
* Python 3
* A copy of MCP
* A copy of the target minecraft.jar and minecraft_server.jar

## Installation
Clone the repository using the following command :
```
git clone --recurse-submodules https://github.com/computerspieler/Mapper.git
```
Then copy minecraft.jar and minecraft_server.jar in the same directory as the script, as well as the content of the conf directory of MCP.
And finally configure and run the script, you should obtain two files : "client.deobf" and "server.deobf", those files are your mappings !

## Tested version
| Client | Server | MCP |
| ------ | ------ | --- |
| Alpha 1.2.6 | 0.2.8 | 2.5 |
| ------ | ------ | --- |
| Alpha 1.1.2_01 | 0.2.0_01 | 1.6 |
| ------ | ------ | --- |
| 1.5.1 | 1.5.1 | 7.4.4 |
| ------ | ------ | --- |

