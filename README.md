# Twilio Hackpack for Heroku and Flask

An easy-to-use repo to kickstart your Twilio app using Flask and deploy onto
Heroku.  Easy to clone, easy to tweak, easy to deploy.


## Features

Look at all these crazy features!

* [Twilio Client](http://www.twilio.com/api/client) - This hackpack ships 
  with a base Jinja2 template for Twilio Client.  Just plug in your AppSid,
  and your browser becomes a phone.
* Plug-and-Play - Procfile and requirements.txt preconfigured for Foreman.
* Easy configuration - Use environment variables or local_settings.py file.
* Boilerplate - All the Flask app boilerplate with example Voice and SMS 
  Request URLs ready for use on Twilio.
* Testing - Easy base class for unit testing with example tests, nose ready.
* PEP8 - It's good for you!


## Installation

1) Grab latest source
<pre>
git clone git@github.com:RobSpectre/Twilio-Hackpack-for-Heroku-and-Flask.git 
</pre>

2) Navigate to folder and create new Heroku Cedar app
<pre>
heroku create --stack cedar
</pre>

3) Configure app for your Twilio account 
<pre>
heroku config:add TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxx
heroku config:add TWILIO_AUTH_TOKEN=yyyyyyyyyyyyyyyyy
heroku config:add TWILIO_APP_SID=APzzzzzzzzzzzzzzzzzz
heroku config:add TWILIO_CALLER_ID=+15556667777
</pre>

4) Deploy to Heroku
<pre>
git push heroku master
</pre>

5) Scale your dynos
<pre>
heroku scale web=1
</pre>

6) Visit the home page of your new Heroku app to see your newly configured app!


## Testing

This hackpack comes with a full testing suite ready for nose.

<pre>
nosetests -v tests/
</pre>

Check out the TwiMLTest base class in test_twilio.py for some utilities to help
test your Twilio apps.


## Meta 

* No warranty expressed or implied.  Software is as is.
* MIT License
* Lovingly crafted by [Twilio New
 York](http://www.meetup.com/Twilio/New-York-NY/) 
