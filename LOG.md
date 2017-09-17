# 100 Days Of Code - Log

### Day 0: Jan 03, 2017

**Today's Progress:** I decided the first app to work on: Google Calendar stats. I did a bit of research and there is nothing like this and it will help me with my own quantified self stuff (still need to explain what it is in its repo). I had a first glipmse of what it is like to work with Django. Also started using Python's virtualenv. 

**Thoughts:** Lots of decisions to make that make me go super slow and not settle on anything.

**Link to work:** [Google Calendar Stats App](https://github.com/Mario-LopezTelecom/gapi)

**Useful info:** 
+  How to handle virtualenv and git: use pip freeze and commit the "requirements.txt" file. [Link](http://stackoverflow.com/questions/6590688/is-it-bad-to-have-my-virtualenv-directory-inside-my-git-repository)
+ Difference between a project and apps in Django: "A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects". [Link](https://docs.djangoproject.com/en/1.10/intro/tutorial01/)


### Day 1: Jan 04, 2017

**Today's Progess:** I created a super basic view and did minimal database config (sqlite). 

**Thoughts:** I am not entirely sure if I even need models for this project. SQLite will do fine just for Django basic needs. Once a user logs in with its Google Calendar credentials, I will pull the required info from its account... why storing it anywhere? I just need to print it. Next: place a simple button in a view, and once clicked, make the request to Google Calendar API.

**Useful info:**
+ I didn't know how to run the python interpreter of the virtualenv. Now I know, I just need to source the "activate" script of the env. And once I have finished, `deactivate`. [Link](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
+ Print sqlite3 tables:
```
sqlite3 <file containing the db>
.tables 
```

### Day 2: Jan 05, 2017

**Today's progess**: I got the credentials to use the Google Calendar API and tried to adapt to Django the Python example Google provides, with no luck.

**Thoughts:** I had the feeling that putting the business logic in Django models (as Odoo forces) was not right and it turns out there are plenty of ways in order to avoid that. I will use the "services,py" approach [1]. Regarding the Google Calendar API, the example Google provides seems to be created to run from the command line and I did not see an obvious way to adapt it to run on Django. Maybe [2], and [3] can help me with that... but I had the impression that there is no clear info out there on the topic. Isn't this strange?   

**Useful info:** 
+ [1] [SO question on business logic separation](http://stackoverflow.com/questions/12578908/separation-of-business-logic-and-data-access-in-django)
+ [2] ["Using Django" on developers.google.com](https://developers.google.com/api-client-library/python/guide/django)
+ [3] [Google Analytics API on Django example from random blog](http://www.marinamele.com/use-the-google-analytics-api-with-django)


### Day 3: Jan 07, 2017

**Today's progress**: I discovered that I asked for the wrong credentials and also that the oauth2client library had changed significantly from the examples I had ([2] and [3]). But I worked my way to adapt the Google Calendar example to the Django code for oauth2client I think that I almost have a working example (now stuck in some kind of "Django user error"). 

**Thoughts:** WHY IS THIS SO DARK? I had to downgrade the version I was using of the oauth2client lib, from the latest 4.0 to 2.2.0, following advice of [4] just because I couldn't find clear examples on how to properly use it (it is not only that the directories changed, and so, almost all import statements where failing, but also they removed critical classes such as "FlowModel". Also, reading a bit more carefully [3], I saw that I had to ask for credentials again, since they are different for a webapp. Specifically, there is something that puzzled me regarding the webapp credential: there is a place where you need to specify "Authorized Javascript origins" for your webapp, which is interesting if you want to test this in a local dev (you cannot specify localhost as origin). People out there suggest to use a URL shortener for that case [5]. In any case: why this seems to be so obscure? I am wondering if I am in the wrong path... this should really be a common operation. 

**Useful info:**
+ [4] [SO question "oauth2client with django flowfield"](http://stackoverflow.com/questions/39304029/oauth2client-with-django-flowfield)
+ [5] [SO question "Oauth - how to test with local urls?"](http://stackoverflow.com/questions/10456174/oauth-how-to-test-with-local-urls) 


### Day 4: Jan 09, 2017

**Today's progress**: I got to connect with Google authorization page. Sadly, the execution always end up [here](https://github.com/Mario-LopezTelecom/gapi/blob/master/gapi_app/services.py#L57), but I have the feeling this is clearly related to me having the wrong secret (see day before). Next day: ask again for credentials and try again. 

**Thoughts:** Guess what? Django versions also made the examples I had impossible to follow. Turns out that `request.REQUEST` ceased to exist in Django 1.9 (mine is 1.10) [6]. However, inspecting the request object, in my case it was easy to see that I only needed `request.GET`as replacement. As a side note, I have to revise the "services" approach I decided to use (see "Day 2"), since I almost have no code in views.py (which makes no sense) and wrapping the return values is giving me some headaches. 

**Useful info:**
+ [6] [Github issue regarding changes in Django versions](https://github.com/tschellenbach/Django-facebook/issues/558)


### Day 5: Jan 11, 2017

**Today's progress**: **Milestone reached**. I finally have a working example of a client for the GCal API, which allows a user to authenticate using any Google account and retrieves the next 10 events of its primary calendar. Now I can move on to extract all the information I need (milestone 2), process it to extract meaningful stats (milestone 3), and display it in a nice way (milestone 4).  

**Thoughts:** I am not sure if I really needed to change the credentials I requested to Google [7] since there were something even more weird going on: the token that Google sends back to my webapp was unicode, when the decoder expected a string ([link to code](https://github.com/Mario-LopezTelecom/gapi/blob/5c5cc2b4b8d1742e6db1f407c75c400f936ef642/gapi_app/services.py#L49-L49)). Also, on that very same sentence, the SECRET_KEY from Django settings was used as the private key, when the correct thing is to use the one that Google gave me when I requested access credentials. In addition, this should NOT be put in plain text and commited to Github... [link to code](https://github.com/Mario-LopezTelecom/gapi/blob/5c5cc2b4b8d1742e6db1f407c75c400f936ef642/gapi/settings.py#L29-L29). Finally, I needed to do the hack I talked about on Day 3 [5]: I did not use a URL shorthener, instead, lvh.me already points out universally to 127.0.0.1.

Bonus: Will it be true that [this guy](https://gist.github.com/levicook/563675) is "the owner" of that domain?

**Useful info:**
+ [7] [Google Developers Console](https://console.developers.google.com/apis?project=578004625497&hl=ES) 


### Day 6: Jan 12, 2017

**Today's progress:** I decided to use the Django REST framework so that my webapp is a Django back-end API replyting to any decoupled front-end stack (will likely be backbone.js for simplicity). 

**Thoughts:** Lots of doubts and reading today, as I was going to start to modify the back-end code to retrieve the stats. I was going to start using the templating system of Django when I realized that I was planning something more like a single page app, with fancier looks. Then I even question if I needed the back-end at all, but it seems it is important for security regarding oauth (although I would need to read more on this topic [8]). Finally, I discovered that the usual thing is to turn the back-end into an REST API (which I could use with mobile apps in the future) and that is the way the front-end interacts.

**Useful info:**
+ [8] [SO question "How do I implement secure OAuth2 consumption in Javascript?"](http://stackoverflow.com/questions/11440398/how-do-i-implement-secure-oauth2-consumption-in-javascript)


### Day 7: Jan 13, 2017

**Today's progress:** Started with serializers for the Django models.

**Thoughts:** It finally seems that OAuth can be perfectly used without back-end [9]. Thus, my app could be done without Django, at least for the basic functionality. Nevertheless, I will still use Django to learn it, and, hopefully, I will need it anyway to expand the basic functionality I have in mind. 

**Useful info:**
+ [9] [Using OAuth 2.0 for Client-side Web Applications](https://developers.google.com/identity/protocols/OAuth2UserAgent)
+ [10] [Django REST Tutorial](http://www.django-rest-framework.org/tutorial/1-serialization/)

---

High peak of work at my day job

---

### Day 8: Jan 20, 2017

**Today's progress:** Built first serializer for serving the calendar events to the front-end.

**Thoughts:** I am not sure whether I will need more that the serializer for CalendarEvent... Now it is just a matter of building the view to serve all the events to the front-end, which will be the one making the graphs from the event. Or maybe I can do the computation in the back-end and serve the data as needed for the graph... I am not entirely sure about this. Next step: building the first view. But first, I will need to understand the difference between function based views and class based views [11].

**Useful info:**
+[11][Blog post about Django view types](http://programeveryday.com/post/writing-django-views-function-based-views-class-based-views-and-class-based-generic-views/)

### Day 9: Jan 28, 2017

**Today's progress:** Objects from GCal are now stored on the database.

**Thoughts:** 🤔

**Useful info:**
+ A foreign key field expects an instance of the object referenced, not the id, unless we use the name of the field + "_id" suffix.
+ Whenever I change a model in Django, I will need to run:

```
python manage.py makemigrations
python manage.py migrate
```

It seems it is interesting to also commit this files, and so I did. But I am unsure about how to use them (maybe once they are checked out, a dev only has to run "migrate"?)[12] 

+ [12][Django docs: Migration](https://docs.djangoproject.com/en/1.10/topics/migrations/)

---

Starting new job...

---

### Day 10: Apr 29, 2017

**Today's progress:** my API now returns the duration in seconds of all events of all calendars within a range of dates.

**Thoughts:** the next step should be to decide how to handle the download of events for each user that logs in (should I wipe and redownload everything everytime somebody logs in? Or can I set some kind of sync?)

**Useful info:** None

---

No good excuse for doing anything...

---
### Day 11: Aug 27, 2017

**Today's progress:** Remembering what was going on in here... and retrieving all calendars and events.

**Thoughts:** I need to gather like a small to do list of what to do from here and in which order.

**Useful info:** Regarding my previous question, Google Calendar API has support for syncronization through sync tokens. 

### Day 12: Sep 17, 2017

**Today's progress:** First scaffold of the frontend using Vue + Webpack.

**Thoughts:** Read on [13] and try to add a first hardcoded pie chart on the web. Still not commited (should I ignore node_modules?).

**Useful info:** [14] is useful to understand the project structure of Vue.

+ [13][Vue-ChartJS web](https://github.com/apertureless/vue-chartjs)
+m[14][Vue Tutorial](https://medium.com/codingthesmartway-com-blog/vue-js-2-quickstart-tutorial-2017-246195cfbdd2
