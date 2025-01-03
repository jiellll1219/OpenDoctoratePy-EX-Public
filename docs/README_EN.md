# DoctoratePy-EX-Public

[中文](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/tree/main/README.md) | [EN](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/tree/main/docs/README_EN.md) |

[Update Log](https://github.com/jiellll1219/OpenDoctoratePy-EX-Public/tree/main/docs/updata_log.md)

This project serves as a branch of OpenDoctoratePy, aiming to expand and improve its functionality. The short-term goal is to prevent being kicked back to the login interface due to 404 or unknown errors as much as possible, while the long-term goal is to achieve a single-player local service similar to the SPT-AKI project.

The code and data structure for some features of this repository are based on [LocalArknight](https://github.com/jiellll1219/LocalArknight).

Development is purely driven by personal interest, and updates are made sporadically due to limited skills. If you encounter issues, please raise an issue, but I cannot guarantee prompt bug fixes (as a student, I only have free time during vacations or after school to write code).

This repository welcomes developers to propose pull requests. Collaborating on DoctoratePy is the original intention behind creating this repository.

If you need to contact me, please raise an issue or send an email to jiege0019@gmail.com.

This project has no community groups and prohibits any profit-driven redistribution or secondary development.

If you want to contribute code but lack data, you can refer to this [il2cpp file](https://drive.google.com/file/d/1q7I_cAFzMtyZ2EYqd1IlZLez1uRElgTv/view?usp=sharing).

## Expansion Progress

| Target Feature | Progress | Status | Notes |
|:---:|:---:|:---:|:---:|
| Public Recruitment | Coding Complete | Basic Completion | Needs Testing |
| Directed Recruitment | Coding Complete | Complete | Basically Usable |
| Infrastructure | Coding Complete | Basic Completion | Needs Testing |
| Shop | Coding Complete | Basic Completion | Needs Testing |
| Top-up System | Coding Complete | Basic Completion | Not Yet Tested |
| Interface Scheme | Coding Complete | Basic Completion | Minor Bugs |
| Integrated Simulation | Paused |  |  |
| Friends | Halted |  | No Functionality |

## Declaration for Top-up System Code

# **The top-up system in this repository is completely unusable in a real payment environment. Please do not attempt to port this part of the code to your private repository. I will not upload the implementation code for this part to the public repository, as I do not want this repository to be subject to a DMCA Takedown.**

## Usage Guide Example

1. Clone/Download another DoctoratePy repository from GitHub to your local machine.  
2. Clone/Download this repository to your local machine.  
3. Overwrite all files from this repository into the local DoctoratePy repository.  
4. Update the data/excel files to match your game version.  
5. Launch `local_server` and complete the missing JSON content.

Supplementary: Due to differences in data structures between DoctoratePy repositories, the contents to be completed or modified will vary. Please review the code in this repository for necessary adjustments. If you still have doubts, raise an issue here and attach the full log when you launch `local_server`. I will try to help during my free time.

If you find this troublesome, you can also connect to my public server to experience it. The server address is http://8.138.148.178:8443/. My function development progress will also be synchronized to this server in real time. Note! This server version is still a single-player version and does not support multi-user play. This server is located in China.

## Data Structure Explanation

The storage structure for some data in this project is based on [LocalArknight](https://github.com/jiellll1219/LocalArknight).

For detailed file structures and related files, please refer to this repository: [LocalArknight-res](https://github.com/jiellll1219/LocalArknight-res).

Tips: If your `user.json` data is missing, you can refer to the user data (e.g., shop, skin) in the [LocalArknight](https://github.com/jiellll1219/LocalArknight) project.

## EX_Config Parameter Explanation

### virtualtime

Used for enabling old gacha pools. When the value is less than 0, real-time is returned.

It may cause issues with infrastructure. Avoid reducing the value unnecessarily once set.

Compatible with more time formats. You can directly input timestamps or formats like `"2024/02/02 12:12:12"` or `"2024-02-02 12:12:12"`. Ensure to use English double quotes `""`, include a space between date and time, and ensure the entered time is complete and reasonable.

## Values in user.json and syncData.json

In the `user` dictionary of these two files, the following entries exist:

```json
"dungeon": {},
"activity": {},
"status": {},
"troop": {},
"npcAudio": {},
"pushFlags": {},
"equipment": {},
"skin": {},
"shop": {},
"mission": {},
"social": {},
"building": {},
"dexNav": {},
"crisis": {},
"crisisV2": {},
"nameCardStyle": {},
"tshop": {},
"gacha": {},
"backflow": {},
"mainline": {},
"avatar": {},
"background": {},
"homeTheme": {},
"rlv2": {},
"deepSea": {},
"tower": {},
"siracusaMap": {},
"sandboxPerm": {},
"openServer": {},
"trainingGround": {},
"storyreview": {},
"medal": {},
"inventory": {},
"limitedBuff": {},
"carousel": {},
"car": {},
"collectionReward": {},
"consumable": {},
"ticket": {},
"aprilFool": {},
"retro": {},
"campaignsV2": {},
"recruit": {},
"checkIn": {},
"share": {},
"charRotation": {},
"charm": {},
"firework": {},
"event": {}
