# DoctoratePy-EX-Public

[简中](../README.md) | [EN](README_EN.md)  
[更新日志(UpdateLog)](docs/updata_log.md)


This project aims to serve as a branch of OpenDoctoratePy, extending and improving its functionality.  
The short-term goal is to prevent being kicked back to the login screen due to 404 or unknown errors as much as possible.  
The long-term goal is to implement a single-player local server similar to the SPT-AKI project.

Part of the code and data structures in this repository reference [LocalArknight](https://github.com/jiellll1219/LocalArknight).

Development is purely for personal interest. My technical ability is limited, and updates are irregular. If you encounter issues, please open an issue, but I cannot guarantee bugs will be fixed immediately (as a student, I only have free time during holidays and after classes to ~~pile up code~~ write).

This repository welcomes PRs from developers. Co-developing DoctoratePy is the reason I created this repository.

If you need to contact me, please open an issue or send me an email: jiege0019@gmail.com

There is no discussion group for this project, and I (the repository owner) do not support any reselling behavior. Such actions are detrimental to the project’s development. If I (the repository owner) discover that reselling has become widespread and unstoppable, this repository will be archived.

If you wish to contribute code but lack data, you can download il2cpp files at [this link](https://dhjuisgf.ap-northeast-1.clawcloudrun.com/). I will periodically upload il2cpp files for each version.

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
| Roguelike | In Progress | Playable Only | Slowly under development |
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

This project is licensed and distributed under the **GNU General Public License, Version 3 (GPLv3)**.

This license applies **only to the act of “conveying” (distribution)** and does not impose obligations on internal use or other non-distribution activities.

---

### 1. Legal Obligations of Distributors

Under the GPLv3, any individual or organization that **distributes** this project or any derivative work (whether modified or unmodified) must comply with the following obligations:

#### 1.1 Preservation of Notices
- Distributors must retain all **copyright notices, license notices, and other relevant notices** included in this project (including README.md and similar files).
- Distributors may not remove or obscure copyright information, license information, or official statements contained in the source code.

#### 1.2 Copyleft Requirement (Infectious Nature of GPLv3)
- GPLv3 is a **strong copyleft license**.  
- Any modified version, derivative work, or secondary project **based on this project**, if distributed, **must also be licensed under GPLv3**.  
- Distributors **may not** relicense derivative works under a proprietary or incompatible license.

In other words, **all redistributed or published derivative works must remain free and open-source under GPLv3**.

#### 1.3 Source Code Provision Obligation (GPLv3 Section 6)
- When distributing object code (such as binaries), distributors must provide the **Complete Corresponding Source Code** for free and with convenience equal to or greater than that of obtaining the object code.
- When distribution is performed over a network, distributors must comply with **GPLv3 Section 6(d)** by ensuring that the complete corresponding source code is accessible through a publicly available and free server.

Below is the official text of **GPLv3 Section 6(d)**:

    > Convey the object code by offering access from a designated place (gratis or for a charge), and offer equivalent access to the Corresponding Source in the same way through the same place at no further charge. You need not require recipients to copy the Corresponding Source along with the object code. If the place to copy the object code is a network server, the Corresponding Source may be on a different server (operated by you or a third party) that supports equivalent copying facilities, provided you maintain clear directions next to the object code saying where to find the Corresponding Source. Regardless of what server hosts the Corresponding Source, you remain obligated to ensure that it is available for as long as needed to satisfy these requirements.

---

### 2. Termination and Restoration of License Rights (GPLv3 Section 8)

According to GPLv3 Section 8:

- If a distributor fails to comply with the terms of the GPLv3, the license rights granted to them are **automatically terminated**.
- If the distributor ceases all violations and corrects the issue within **30 days** of discovery or notification, the rights are **automatically restored**.
- For **intentional** or **repeated** violations, the relevant rights are permanently terminated and **cannot** be automatically restored.

---

### 3. Notes

This statement aims to clarify and emphasize the key obligations under the GPLv3 for easier understanding and compliance.  
It does **not** replace, modify, or override any provisions of the GPLv3. In the event of any conflict, the **official GPLv3 license text** shall prevail.

**Please read the full GPLv3 license before distribution:**  
<https://www.gnu.org/licenses/gpl-3.0.html>

## Violation-message