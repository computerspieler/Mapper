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
|---|---|---|
| Alpha 1.2.6 | 0.2.8 | 2.5 |
| Alpha 1.1.2_01 | 0.2.0_01 | 1.6 |
| 1.5.1 | 1.5.1 | 7.4.4 |

## Where can I download MCP?

This list comes from the [Minecraft wiki page for MCP](https://minecraft.fandom.com/wiki/Tutorials/Programs_and_editors/Mod_Coder_Pack) and includes download links and brief changelogs for various versions of the Mod Coder Pack (MCP).

| MCP Version | Targeted Minecraft Version | Download Link | Change Log |
|-------------|----------------------------|---------------|------------|
| 9.40 | 1.12 | [Download link](http://www.modcoderpack.com/files/mcp940.zip) | Updated to support Minecraft Client 1.12 and Minecraft Server 1.12; updated fernflower for Java 8 |
| 9.37 | 1.11.2 | [Download link](http://www.modcoderpack.com/files/mcp937.zip) | Updated to support Minecraft Client 1.11.2 and Minecraft Server 1.11.2 |
| 9.31 | 1.10 | [Download link](http://www.modcoderpack.com/files/mcp931.zip) | Updated to support Minecraft Client 1.10 and Minecraft Server 1.10 |
| 9.28 | 1.9.4 | [Download link](http://www.modcoderpack.com/files/mcp928.zip) | Updated to support Minecraft Client 1.9.4 and Minecraft Server 1.9.4 |
| 9.24 | 1.9 | [Download link](https://www.mediafire.com/file/3ww1inazlkamkcc/) | Updated to support Minecraft Client 1.9 and Minecraft Server 1.9 |
| 9.18 | 1.8.8 | [Download link](http://www.modcoderpack.com/files/mcp918.zip) | Updated to support Minecraft Client 1.8.8 and Minecraft Server 1.8.8 |
| 9.10 | 1.8 | [Download link](https://www.mediafire.com/file/56xoalz89957n7o) | Updated to support Minecraft Client 1.8 and Minecraft Server 1.8 |
| 9.08 | 1.7.10 | [Download link](http://www.mediafire.com/download/2czafa60rh4ajhj/mcp908.zip) | Updated to support Minecraft Client 1.7.10 and Minecraft Server 1.7.10 |
| 9.03 | 1.7.2 | [Download link](http://www.mediafire.com/download/q97ptg3ng85tpra/mcp903.zip) | Release Candidate to support Minecraft Client 1.7.2 and Minecraft Server 1.7.2 |
| 8.11 | 1.6.4 | [Download link](http://www.mediafire.com/?96mrmeo57cdf6zv) | Updated to support Minecraft Client 1.6.4 and Minecraft Server 1.6.4 |
| 8.05 | 1.6.2 | [Download link](http://www.mediafire.com/?xcjy2o2zsdol7cu) | Updated MD5 checksum, fixed the "missing library" bug and removed an undiscovered bug. |
| 8.04 | 1.6.2 | [Download link](http://www.mediafire.com/?zddk7n54o8jgihz) | Updated to support Minecraft 1.6.2 and Minecraft Server 1.6.2. |
| 8.03 | 1.6.1 | [Download link](http://www.mediafire.com/?fu9b8voz4xeu29n) | Updated to support Minecraft 1.6.1 and Minecraft Server 1.6.1 / important fix for 8.02 |
| 7.51 | 1.5.2 | [Download link](http://www.mediafire.com/?95vlzp1a4n4wjqw) | Updated to support Minecraft 1.5.2 and Minecraft Server 1.5.2. |
| 7.44 | 1.5.1 | [Download link](http://www.mediafire.com/?2s29h4469m2ysao) | Updated to support Minecraft 1.5.1 and Minecraft Server 1.5.1. |
| 7.42 | 1.5 | [Download link](http://www.mediafire.com/?bbgk21dw4mp02sp) | Updated to support Minecraft 1.5 and Minecraft Server 1.5. |
| 7.39 | 13w09c | [Download link](http://www.mediafire.com/?t23e247mudahtam) | Updated to support Minecraft 13w09c and Minecraft Server 13w09c. Renamed from 'Minecraft Coder Pack' to 'Mod Coder Pack'. |
| 7.34 | 13w05b | [Download link](http://www.mediafire.com/?690vfbejvfe8q0m) | Updated to support Minecraft 13w05b and Minecraft Server 13w05b. |
| 7.30c | 13w02b | [Download link](http://www.mediafire.com/?8amwnl6gt6p6gc5) | Updated to support Minecraft 13w02b and Minecraft Server 13w02b. |
| 7.26a | 1.4.7 | [Download link](http://www.mediafire.com/?07d59w314ewjfth) | Updated to support Minecraft 1.4.7 and Minecraft Server 1.4.7. |
| 7.25 | 1.4.6 | [Download link](http://www.mediafire.com/?4kzs5swcm5ypqo6) | Updated to support Minecraft 1.4.6 and Minecraft Server 1.4.6. |
| 7.23 | 1.4.5 | [Download link](http://www.mediafire.com/?spaiyzpccxkx6cg) | Updated to support Minecraft 1.4.5 and Minecraft Server 1.4.5. |
| 7.21 | 1.4.4 | [Download link](http://www.mediafire.com/?i27oi6miadssyp9) | Updated to support Minecraft 1.4.4 and Minecraft Server 1.4.4. |
| 7.19 | 1.4.2 | [Download link](http://www.mediafire.com/?rz8dnqj1bxrz85q) | Updated to support Minecraft 1.4.2 and Minecraft Server 1.4.2. |
| 7.2 | 1.3.2 | [Download link](http://www.mediafire.com/?38vjh7hrpprrw1b) | Updated to support Minecraft 1.3.2 and Minecraft Server 1.3.2. |
| 7.0a | 1.3.1 | [Download link](http://www.mediafire.com/?hxui27dv5q4k8v4) | Added fernflower decompiler due to new permission to distribute it. |
| 7.0 | 1.3.1 | [Download link](http://www.mediafire.com/?chw6hym6lu974xn) | Updated to support Minecraft 1.3.1 and Minecraft Server 1.3.1.<br>Extended patches to remove herobrine code from decompiled classes. |
| 6.15 | 12w26a | [Download link](http://www.mediafire.com/?dhhvhzezje6zx59) | Updated to support Minecraft 12w26a and Minecraft Server 12w26a. |
| 6.5 | 12w17a | [Download link](http://www.mediafire.com/?0nxeeitb1s54x1e) | Updated to support Minecraft 12w17a and Minecraft Server 12w17a. |
| 6.2 | 1.2.5 | [Download link](http://www.mediafire.com/?c6liau295225253) | Updated to support Minecraft 1.2.5 and Minecraft Server 1.2.5.<br>Update patches to work around worldgen crash in vanilla minecraft client and server.<br>Update patches to work around and a client crash when clicking on chat history. |
| 6.1 | 1.2.4 | [Download link](http://www.mediafire.com/?hl1t281w442wfxf) | Updated to support Minecraft 1.2.4 and Minecraft Server 1.2.4.<br>Disabled rounding of float and double constants due to issues with getting stuck on respawn.<br>Updated client patches to work around OpenGL issues with main window on OSX and Linux. |
| 6.0 | 1.2.3 | [Download link](http://www.mediafire.com/?emz17agmzr3ed7e) | Updated to support Minecraft 1.2.3 and Minecraft Server 1.2.3.<br>Added javadoc comments to the decompiled sourcecode. |
| 5.6 | 1.1.0 | [Download link](http://www.mediafire.com/?wu9gfhy73m4k6a4) | Updated to support Minecraft 1.1.0 and Minecraft Server 1.1.0.<br>Run Artistic Style source beautifier on decompiled source code. |
| 5.0 | 1.0.0 | [Download link](http://www.mediafire.com/?s7dyeugk867no9j) | Updated to support Minecraft 1.0.0 and Minecraft Server 1.0.1. |
| 4.5 | 1.9-pre5 | [Download link](http://www.mediafire.com/?rf5tothc5h7au3f) | Updated to support Minecraft Beta 1.9-pre5 and Minecraft Beta Server 1.9-pre5.<br>Improved Retroguard and Exceptor tools. |
| 4.4 | Beta 1.8.1 | [Download link](http://www.mediafire.com/?g09as6o73ls77c6) | Updated to support Minecraft Beta 1.8.1 and Minecraft Beta Server 1.8.1.<br>Improved Retroguard and Exceptor tools.<br>Fixes to mapping of methods in EntityLiving.<br>Bugfix for crashes when playing sounds due to issue in Block.java. |
| 4.3 | Beta 1.7.3 | [Download link](http://www.mediafire.com/?03d94f13c9ulj5a) | Updated to support Minecraft Beta 1.7.3 and Minecraft Beta Server 1.7.3. |
| 4.2 | Beta 1.7.2 | [Download link](http://www.mediafire.com/?1gtxx92yrrbt2cx) | Updated to support Minecraft Beta 1.7.2 and Minecraft Beta Server 1.7.2. |
| 4.1 | Beta 1.6.6 | [Download link](http://www.mediafire.com/?tgftx5b6u43lcpm) | Added an Eclipse workspace.<br>Included a reobfuscation bugfix. |
| 4.0 | Beta 1.6.6 | [Download link](http://www.mediafire.com/?5pn4dawl1f7b55d) | Added new tool Exceptor.<br>Added alternative support for fernflower decompiler. |
| 3.4 | Beta 1.6.6 | [Download link](http://www.mediafire.com/?gbciib2sgukgtb7) | Updated to support Minecraft Beta 1.6.6 and Minecraft Beta Server 1.6.6. |
| 3.3 | Beta 1.6.5 | [Download link](http://www.mediafire.com/?kwkk3l008g6bft1) | Updated to support Minecraft Beta 1.6.5 and Minecraft Beta Server 1.6.5. |
| 3.2 | Beta 1.6.4 | [Download link](http://www.mediafire.com/?x2otccwnqbmusjg) | Updated to support Minecraft Beta 1.6.4 and Minecraft Beta Server 1.6.4.<br>Added support for external jar files in recompile and reobfuscation.<br>Updated the readme files.<br>Small bugfix for using mcp offline. |
| 3.1 | Beta 1.5_01 | [Download link](http://www.mediafire.com/?2gskj39vdafepri) | Some more bugfixes in the python scripts. |
| 3.0 | Beta 1.4_01 | [Download link](http://www.mediafire.com/?793j36x8r1an3bz) | Updated to support Minecraft Beta 1.4_01 and Minecraft Beta Server 1.4_01.<br>Complete rewrite of the scripts in python.<br>RetroGuard used both for deof and reobf.<br>Automatic detection of modified classes during reobfuscation.<br>Protection on cleanup.bat/sh.<br>Advanced logging system (logs/mcp.log, logs/mcperr.log).<br>Removed repackager.exe and mono dependancy on Linux.<br>Cleaner directory structure.<br>Out of the box decompilation compatibility with modded jars.<br>Rolling update model on top of the usual full package distrib.<br>Custom files in bin directory are preserved during recompilation.<br>Custom files are automatically copied to reobf directory during reobf. |
| 2.12 | Beta 1.5_01 | [Download link](http://www.mediafire.com/?p5ptl7epbuk5emy) | Updated to support Minecraft Beta 1.5_01 and Minecraft Beta Server 1.5_02. |
| 2.11 | Beta 1.4_01 | [Download link](http://www.mediafire.com/?skko90kp657q6kb) | Updated to support Minecraft Beta 1.4_01 and Minecraft Beta Server 1.4_01. |
| 2.10 | Beta 1.4 | [Download link](http://www.mediafire.com/?v8jr2vo524yaqnn) | Updated to support Minecraft Beta 1.4 and Minecraft Beta Server 1.4. |
| 2.9a | Beta 1.3_01 | [Download link](http://www.mediafire.com/?idlmki22diklhf3) | Added support for mod loader 1.3_01v3.<br>Added MCP Mod System SDK updated for 1.3_01.<br>Updated name mappings. |
| 2.9 | Beta 1.3_01 | [Download link](http://www.mediafire.com/?5coxcq54s9qn6m9) | Updated to support Minecraft Beta 1.3_01 and Minecraft Beta Server 1.3. |
| 2.8 | Beta 1.2_02 | [Download link](http://www.mediafire.com/?0d6iby6se4h7aam) | Added alpha version of OSX support.<br>Added alpha version of the MCP mod system.<br>Updated mapping with a lot more method and field names. |
| 2.7 | Beta 1.2_02 | [Download link](http://www.mediafire.com/?k3sev7pdlreou4j) | Updated to support Minecraft Beta 1.2_02 and Minecraft Beta Server 1.2_01. |
| 2.6 | Beta 1.1_02 | [Download link](http://www.mediafire.com/?cjrw785u9e857yh) | Updated to support Minecraft Beta 1.1_02 and Minecraft Beta Server 1.1_02. |
| 2.5 | Alpha v1.2.6 | [Download link](http://www.mediafire.com/?7422b88qu650547) | Updated to support Minecraft Alpha 1.2.6 and Minecraft Alpha Server 0.2.8, <a target="_blank" rel="nofollow noreferrer noopener" class="external text" href="https://files.pymcl.net/archive/mcp/patches/reobf-fix-mcp2.5.zip">reobf-fix</a> recommended. |
| 2.4 | Alpha v1.2.5 | [Download link](http://www.mediafire.com/?o7ddvw1o65g3wj3) | Updated to support Minecraft Alpha 1.2.5 and Minecraft Alpha Server 0.2.7. |
| 2.3 | Alpha v1.2.3_04 | [Download link](http://www.mediafire.com/?12jdmiqkd5gy977) | Updated to support Minecraft Alpha 1.2.3_04 and Minecraft Server Alpha 0.2.5_02.<br>Linux version is now available.<br>Renamer now includes the OpenGL constant annotater from MissLil.<br>Renamer output the proper reobfuscation table for Obfuscathon_v2.<br>Name collision has been turned off, removing all the _00 tails on many variables.<br>Obfuscathon is now context aware. This should remove a lot of prb with the reobfuscation.<br>Various updates on the scripts.<br>The location of the CSVs have been moved to MCP server. Related tools have been updated.<br>.Many modifications on the spreadsheets.<br>Started porting the whole CSV hell to a cleaner database. |
| 2.2a | Alpha v1.2.2 | [Download link](http://www.mediafire.com/?vwgj80p8n1plrlq) | Bugfixes for the re-obfuscation tools. |
| 2.2 | Alpha v1.2.2 | [Download link](http://www.mediafire.com/?fp1xw3u9i9yo0bl) | Re-obfuscation beta test starting to make mods compatible with original jar files. |
| 2.1 | Alpha v1.2.2 | [Download link](http://www.mediafire.com/?ym16233j5901bo4) | Updated to support Minecraft Alpha 1.2.2. |
| 2.0a | Alpha v1.2.1_01 | [Download link](http://www.mediafire.com/?xmllq6u6zsgc0k8) | A minor bugfix. Some scripts did not work properly if there were space in the path. |
| 2.0 | Alpha v1.2.1_01 | [Download link](http://www.mediafire.com/?0bmbq333sobp44h) | First release for post-Halloween Minecraft versions. |
| 1.6 | Alpha v1.1.2_01 | [Download link](http://www.mediafire.com/?7gq62gydrb12c2a) | All classes have meaningful names now; the class name mappings and the field name mappings are applied. |
| 1.5 | Alpha v1.1.2_01 | [Download link](http://www.mediafire.com/?777ifteu05j2m6b) | Extend the scripts to also support decompiling, recompiling and testing the minecraft_server.jar file. |
| 1.4 | Alpha v1.1.2_01 | [Download link](http://www.mediafire.com/?i44y3sp66e6ag62) | Using a deobfuscator to rename all fields and methods and jadretro to fix some decompile bugs. |
| 1.3 | Alpha v1.1.2_01 | [Download link](http://www.mediafire.com/?44s3710ah5f078j) | Added upgrade scripts to decompile and recompile Minecraft.class, MinecraftApplet.class and MinecraftServer.class. |
| 1.2 | Alpha v1.1.2_01 | [Download link](http://www.mediafire.com/?sumc56jz5su8546) | Redirect output of all tools to a logfile. |
| 1.1 | Alpha v1.1.2_01 | [Download link](http://www.mediafire.com/?4ygvy942rsecjw7) | Fixed TNT bug. |
| 1.0 | Alpha v1.1.2_01 | [Download link](http://www.mediafire.com/?nukc5jh5yu83cdp) | First release. |
