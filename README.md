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


## Usage

This hackpack ships with two ready-to-go endpoints for your Twilio Voice and SMS
apps.  The two routes /voice and /sms contain two examples you can modify
easily.

For example, here is a quick Twilio Voice app that plays some Ramones.

```python
@app.route('/voice', methods=['POST'])
def voice():
    response = twiml.Response()
    response.play("http://example.com/music/ramones.mp3")
    return str(response)
```

SMS apps are similarly easy.

```python
@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    response.sms("The Ramones are great!")
    return str(response)
```

These apps can get interactive pretty quickly.  For example, let's make an SMS
app that responds with "Best band ever" when you text RAMONES.

```python
@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    body = request.form['Body']
    if "RAMONES" in body:
        response.sms("Best band ever.")
    else:
        response.sms("Not the best band ever.")
    return str(response)
```

You can apply this same concept to
[Gathering](http://www.twilio.com/docs/api/twiml/gather) user input on Twilio
Voice.  Here we will Gather the user input with one route and then handle the
user input with another.

```python
@app.route('/voice', methods=['POST'])
def voice():
    response = twiml.Response()
    with response.gather(numDigits=1, action="/gather") as gather:
        gather.say("Press 1 to indicate The Ramones are the best band ever.")
    return str(response)

@app.route('/gather', methods=['POST'])
def gather():
    response = twiml.Response()
    digits = request.form['Digits']
    if digits == "1":
        response.say("You are correct.  The Ramones are the best.")
    else:
        response.say("You are wrong.  Never call me again.")
    return str(response)
```

## Installation

1) Grab latest source
<pre>
git clone git://github.com/RobSpectre/Twilio-Hackpack-for-Heroku-and-Flask.git 
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
nosetests -v tests
</pre>

It also ships with an easy-to-use base class for testing your
[TwiML](http://www.twilio.com/docs/api/twiml).  For example, testing a basic SMS
response is only two lines of code:

```python
class ExampleTest(TwiMLTest):
    response = self.sms("Test")
    self.assertTwiML(response)
```

You can also test your [Gather
verbs](http://www.twilio.com/docs/api/twiml/gather) for voice apps very easily.

```python
class ExampleTest(TwiMLTest):
    response = self.call(digits="1")
    self.assertTwiML(response)
```


## Meta 

* No warranty expressed or implied.  Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by [Twilio New
 York](http://www.meetup.com/Twilio/New-York-NY/) 
