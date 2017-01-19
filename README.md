# Google Calendar Statistics Webapp. Codename: "gapi".

I am quite obsessed with the [quantified self](https://www.ted.com/talks/gary_wolf_the_quantified_self) concept and productivity. I really like to get weekly stats on the use of my time, and gaining some insights on how I spend it:

![stats](https://cloud.githubusercontent.com/assets/8227377/22119765/21f3fc36-de7d-11e6-9f4c-bc82c2d426bf.png)

There is no shortage of apps to track time, such as [Toggl](https://toggl.com/), [Rescue Time](https://www.rescuetime.com/), spreadsheets, etc. However, I ended up tracking my time with Google Calendar, specially because it allows me to drag&drop activities, and there is no duplication in logging them (I already put most of them in the calendar. Nevertheless, when using any other tracking app, I needed to insert them in the app too). 

While there are some time-tracking apps that offer some kind of import from Google Calendar (e.g., [Timeneye](https://www.timeneye.com/en/integrations/google-calendar-time-tracking), they do not really suit my use case, where I have a calendar per life area/project, color coded activities without dependency on their names, etc.

Because of this, and as a learning web project (Django back-end + front-end), I will create my own web dashboard with statistics from Google Calendar. 
