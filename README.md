SamePage
========
![SamePage logo icon](/static/assets/icons/logo-88.png)

### Summary
SamePage provides lightweight kanban project management through simple, virtual pinboards. A user can be a member of several teams, navigating between team boards through a Dashboard. Users can “opt in” and claim action items as if grabbing a post-it "action item" off of a board. Teammates can also post new ideas for their colleagues or friends to upvote. Teammates see all pending tasks at a glance, as well as click into any of their pending action items to update notes or mark as completed.

Email API integration allows users to invite new contributors, and data visualizations provide user and team data insights. Using drag and drop kinetics, the app is intuitive and easy to use for personal projects, planning events with friends, or keeping a professional team on the same page.

![SamePage landing screen](/static/assets/demo/homepage-screenshot.png)

### Technologies

Python   //   PostgresQL  //  SQLAlchemy  //  Flask  //  Jinja  //  Javascript (AJAX, JSON)  //  JQuery  //  JQuery UI  //  HTML  //  CSS  //  Bootstrap (JS and CSS) // MailGun API  //  Chart.js  //  Coverage.py

![Navigating Boards and Claiming an Idea or Action Item](/static/assets/demo/nav-boards-claim-item.gif)
*Navigating Boards and Claiming an Idea or Action*

### Features
  - Create teams (such as Work or Home)
  - Invite team members via email invitation
  - Accept or ignore team invitations
  - Create team boards (such as Administration or DIY Projects)
  - Create action items or ideas
  - Claim items through button click or drag and drop
  - View all items that the user has claimed for a team, from any team board, in the in-progress dock
  - Store notes in items
  - Mark items as completed with a double click into a claimed item
  - View team data insights after login
 
![Completing an item, viewing permissions Item](/static/assets/demo/completing-items-permissions.gif)
*Completing an item, viewing an item's permissions*

### 2.0 Under Development
  - Delete or edit items and ideas without completion
  - Drag and Drop into Backlog to put items on hold or Done repository to complete
  - Un-claim an item to return to group pot if partially completed
  - Completion of upvote tracking and optional auto-action-item setting
  - Toggle tutorial that enables hover for tooltips
  - View ignored team invitations
  - View all user-claimed action items for all teams on a User Action Board; toggle which teams are viewed
  - Add/open/edit/hide the resources panel for each team, also toggle-able and accessible from User Action Board
  - Editing a profile page, where settings and user email/displayname can be edited
  - Add/edit team icon or photo
  - Search past and current items/ideas for keywords for project milestones viewing
  - Expand email API permissions package to support all user email invitations (non-registered endpoints)
  - Addition of About page
  - Increased user feedback through animation/page updates, and auto-navigation on team creation
 
![Email invitations and registration](/static/assets/demo/register-accept-email-invite.gif)
*Email invitations and registration*

### Plans Beyond 2.0
- Integration with Slack API for team login, team chat, item comment threads, and file sharing
- Person-to-person sending of items and ideas via feedback request
- Visual redesign with fun, non-skeuomorphic, geometric visuals and transition animations, with lean toward board-game birds-eye setup
- Optional gamification for personal productivity, earning points to gain avatar upgrades or unlocking special animations.
- Team board templates
- Task "aging" through visual feedback, when left in group grabbable pot
- Max volume settings to encourage re-prioritization to backlog or back to the group pool

![Insights page](/static/assets/demo/insights-screenshot.png)
*Insites page with productivity information and data visualization with Chart.js*

### Installation

See *requirements.txt* for installation packages for virtual environment.

### Running Samepage
After environment setup, for running in a bash terminal on localhost:
*From within the the repo*
```sh
$ createdb project
$ python seed.py      
$ python server.py
```
Email invitation feature is currently limited to endpoints pre-approved in MailGun API for author. Current version requires setup of MailGun API account and API key, creating a secrets.sh file, and assigning variable names:
- MAILGUN_API_SANDBOX_DOMAIN 
- MAILGUN_API_KEY
- MAILGUN_API_POSTMASTER_ADDRESS. 
See helper.py in section SENDING EMAILS (MAILGUN API).

*Data in seed.py contains example data with a Game of Thrones theme as an example.*

### About

SamePage was created as an exercise for confirmation learning about end-to-end web development in a 4 week sprint. Therefore, code will continue to be refactored and improved for modularity, clarity, testing, and runtime considerations. 

Samepage's design choices reflect the author's view that some project management tools are not intuitive for non-technical teams, and allow too many discouraging "deadline" metrics that can be set by another teammate. Ideally in Samepage, everyone knows what everyone is working on, and can support each other in meeting team goals.

Samepage logo icon was created by a friend of the author, and all photos and videos were sourced from https://www.pexels.com or https://unsplash.com. All credit information is recorded and will be added to the About page in 2.0.
