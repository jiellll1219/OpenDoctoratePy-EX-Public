# DoctoratePy-EX-Public

[简中](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/tree/main/README.md) | [EN](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/blob/main/docs/README_EN.md)

[Update Log (CN Only)](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/tree/main/docs/updata_log.md)

This project aims to serve as a branch of OpenDoctoratePy, extending and improving its functionality.  
The short-term goal is to prevent being kicked back to the login screen due to 404 or unknown errors as much as possible.  
The long-term goal is to implement a single-player local server similar to the SPT-AKI project.

Part of the code and data structures in this repository reference [LocalArknight](https://github.com/jiellll1219/LocalArknight).

Development is purely for personal interest. My technical ability is limited, and updates are irregular. If you encounter issues, please open an issue, but I cannot guarantee bugs will be fixed immediately (as a student, I only have free time during holidays and after classes to ~~pile up code~~ write).

This repository welcomes PRs from developers. Co-developing DoctoratePy is the reason I created this repository.

If you need to contact me, please open an issue or send me an email: jiege0019@gmail.com

There is no discussion group for this project, and I (the repository owner) do not support any reselling behavior. Such actions are detrimental to the project’s development. If I (the repository owner) discover that reselling has become widespread and unstoppable, this repository will be archived.

If you wish to contribute code but lack data, you can download il2cpp files at [this link](https://tptpmmpc.ap-southeast-1.clawcloudrun.com/). I will periodically upload il2cpp files for each version.

## Expansion Progress

| Target Feature | Progress | Completion Status | Remarks |
|:---:|:---:|:---:|:---:|
| Public Recruitment | Paused | Phantom bug |  |
| Targeted Search | Completed | Done | Tested |
| Building | Needs Improvement | Needs Improvement |  |
| Shop | Completed | Mostly Done | Can't Buy Anything |
| Recharge | Completed | Done |  |
| Interface Design | Completed | Done | Tested |
| CheckIn | Completed | Done | Tested |
| Activity CheckIn | Continuous updates | Mostly Done |  |
| Limited-time event | Continuous updates |  |  |
| Roguelike Mode | In Progress | Playable Only |  |
| Missions | In Progress |  |  |
| SandBox | Paused |  |  |
| Friends | Completed | Done | Tested |

## Recharge System Code Statement

# **The recharge system in this repository is completely unusable in real payment environments. Do not attempt to port this part of the code into your private repository. I will not upload this part of the implementation code to the public repository. I do not want this repository to be DMCA’d.**

## Usage Guide

Before using:  
Please ensure your Python version is **>= 3.11.0**. Versions below 3.11.0 may lack certain built-in functions.  
If you configure the environment using `steup_poetry.cmd` in the following steps, you must also use `start_server_poetry.cmd` to start the server. The pip configuration method is retained only as a fallback and is **not recommended**.

1. Find GameData or dump game resources to obtain the `excel` folder and its contents, then place the `excel` folder into the `data` directory.  
2. Run `steup_poetry.cmd` or `steup_pip.cmd` to configure the environment.  
3. Run `start_server_poetry.cmd` or `start_local_server.cmd` to start the server.  
4. Find your own way to route the game to the server. This repository does not provide a solution.  

## Config Parameters Explanation

These parameters are located in the `server` dictionary of `config.json`.

### virtualtime

Used for enabling old banners.  
If the value is less than 0, it returns the real-time system clock.

May cause issues with Infrastructure. Do not arbitrarily reduce this value after confirmation.

Supports more time formats. You can input a timestamp directly, or strings like `"2024/02/02 12:12:12"` or `"2024-02-02 12:12:12"`.  
Note: When using such strings, enclose them in double quotes `""`. A space is required between the date and time. Ensure the input is complete and reasonable.

### useMemoryCache

Controls whether to use memory caching. Default is `false` (disabled).  
When enabled (`true`), the server will occupy at least **0.4GB memory** at startup, but it will slightly reduce CPU usage, `syncdata` function time, and other table-reading function times.  
When disabled, memory usage is about **80MB** at startup, peaking at around **0.2GB**. Enable based on your needs.

The optimized `syncdata` function already has acceptable performance.  
- On a 3.1GHz CPU, `syncData` takes about **1.667709s**.  
- On a 1.5GHz CPU, `syncData` takes about **3.695747s**.  
(Test version: 2.4.61)

## GPLv3 License Statement

This project is licensed under the **GNU General Public License v3 (GPLv3)**.

This license only applies to **distribution** and imposes no restrictions on **internal use**.

According to GPLv3, anyone who **distributes** programs based on this repository’s code (whether modified or not) **must** provide the complete corresponding source code.

In addition to the GPLv3 terms, as the repository holder, **we require** that any **distributed** version of this repository (whether source code, compiled, or packaged) must clearly:

1.  **Provide the source repository link**:  
    `https://github.com/jiellll1219/OpenDoctoratePy-EX-Public`

2.  **Include this copyright statement and the full GPLv3 license text**.

According to GPLv3 Section 8, if you fail to comply with the license terms during **distribution**, your rights under this license are automatically terminated.  
However, if you cease all violations and remedy them within **30 days** of becoming aware or being notified, your rights will be automatically reinstated.

For entities engaging in **willful or repeated violations**, all rights granted under GPLv3 will be **permanently terminated**, with no automatic reinstatement. This decision is at the sole discretion of the repository holder.

This statement is an interpretation and emphasis of the GPLv3 terms and does not replace them. Please read and fully understand the [full GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.html) before proceeding.