# Twilio Hackpack for Heroku and Flask

An easy-to-use repo to kickstart your Twilio app using Flask and deploy onto
Heroku.  Easy to clone, easy to tweak, easy to deploy.

[![Build
Status](https://secure.travis-ci.org/RobSpectre/Twilio-Hackpack-for-Heroku-and-Flask.png)]
(http://travis-ci.org/RobSpectre/Twilio-Hackpack-for-Heroku-and-Flask)


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

Step-by-step on how to install and configure this hackpack.

### Basic Install

1) Grab latest source
<pre>
git clone git://github.com/RobSpectre/Twilio-Hackpack-for-Heroku-and-Flask.git 
</pre>

2) Navigate to folder and create new Heroku Cedar app
<pre>
heroku create --stack cedar
</pre>

3) Deploy to Heroku
<pre>
git push heroku master
</pre>

4) Scale your dynos
<pre>
heroku scale web=1
</pre>

5) Visit the home page of your new Heroku app to see your newly configured app!
<pre>
heroku open
</pre>

### Configuration

Want to use the built-in Twilio Client template?  Configure your app with two
easy options.

#### local_settings.py

local_settings.py is a file available in the hackpack route for you to configure
your twilio account credentials manually.  Be sure not to expose your Twilio
account to a public repo, however.

```python
ACCOUNT_SID = "ACxxxxxxxxxxxxx" 
AUTH_TOKEN = "yyyyyyyyyyyyyyyy"
TWILIO_APP_SID = "APzzzzzzzzz"
TWILIO_CALLER_ID = "+17778889999"
```

#### Environment Variables

The canonical approach for Heroku apps. This method is slightly more complex
than configuring in local_settings.py, but better for you, and therefore (of
course) the world.

1) Set environment variables locally.
<pre>
export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxx
export TWILIO_AUTH_TOKEN=yyyyyyyyyyyyyyyyy
export TWILIO_APP_SID=APzzzzzzzzzzzzzzzzzz
export TWILIO_CALLER_ID=+15556667777
</pre>

2) Set environment variables for Heroku app.
<pre>
heroku config:add TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxx
heroku config:add TWILIO_AUTH_TOKEN=yyyyyyyyyyyyyyyyy
heroku config:add TWILIO_APP_SID=APzzzzzzzzzzzzzzzzzz
heroku config:add TWILIO_CALLER_ID=+15556667777
</pre>


## Testing

This hackpack comes with a full testing suite ready for nose.

<pre>
nosetests -v tests
</pre>

It also ships with an easy-to-use base class for testing your
[TwiML](http://www.twilio.com/docs/api/twiml).  For example, testing a basic SMS
response is only two lines of code:

```python
import test_twilio

class ExampleTest(test_twilio.TwiMLTest):
    response = self.sms("Test")
    self.assertTwiML(response)
```

You can also test your [Gather
verbs](http://www.twilio.com/docs/api/twiml/gather) for voice apps very easily.

```python
import test_twilio

class ExampleTest(test_twilio.TwiMLTest):
    response = self.call(digits="1")
    self.assertTwiML(response)
```


## Branches

Two configurations are available in different branches:

* master - Default dev mode with minimum possible code to get going.
* production - Intended for live use with more code and dependencies appropriate
  to a production environment. To deploy this branch instead, adjust your
  procedure for the production branch:

<pre>
git checkout production
git push heroku production:master
</pre>


## Meta 

* No warranty expressed or implied.  Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by [Twilio New
 York](http://www.meetup.com/Twilio/New-York-NY/) 


## Community Contributors

Here we recognize crack members of the Twilio community who worked on this
hackpack.

* [Timothée Boucher](http://www.timotheeboucher.com/) - idea for production
  branch
