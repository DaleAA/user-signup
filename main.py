#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        User Signup
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

import webapp2
import cgi
import re

def escape_html(s):
    return cgi.escape(s, quote = True)

    ## basic layout

form = """
<form method="post">
    <br>
    <label> <div>Username <input type="text" name="username" value = "%(username)s" required></label><span style = "color:red">%(name_error)s</span></div>

    <label><div> Password <input type="password" name="password" value = "%(password)s" required></label><span style = "color:red">%(pass_error)s</span></div>

    <label><div> Verify Password <input type="password" name="verify" value = "%(verify)s" required></label><span style = "color:red">%(verify_error)s</span></div>

    <label><div> Email (optional) <input = "text" name = "email" value = "%(email)s"></label><span style = "color:red">%(email_error)s</span></div>

    <br>
  <input type="submit">
</form>
"""

def verify_password(verify, password):
    if verify != password:
        return (False)
    else:
        return(True)

def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)

def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)

def valid_email(email):
    if email and email.strip():
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        return EMAIL_RE.match(email)
    else:
        return True

class Index(webapp2.RequestHandler):

    def write_form(self, username = "", password = "", verify = "", email = "", name_error="",pass_error="",verify_error="",email_error=""):
        self.response.write(page_header + form %{
                                    "username": escape_html(username),
                                    "password": escape_html(password),
                                    "verify": escape_html(verify),
                                    "email": escape_html(email),
                                    "name_error":name_error,
                                    "pass_error":pass_error,
                                    "verify_error":verify_error,
                                    "email_error":email_error,
                                    } +
                                    page_footer)

    def get(self):
        self.write_form()

    def post(self):
        user_name = self.request.get('username')
        pass_word = self.request.get('password')
        ver_ify = self.request.get('verify')
        e_mail = self.request.get('email')

        username = valid_username(user_name)
        password = valid_password(pass_word)
        email = valid_email(e_mail)
        verify = verify_password(ver_ify, pass_word)

        n_error = "That's not a valid username"
        e_error = "That's not a valid e-mail"
        p_error = "That's not a valid password"
        v_error = "Passwords don't match"

        if (username and password and verify):
            if not email:
                self.write_form(username = user_name, email = e_mail, email_error = e_error)
            else:
                self.redirect("/welcome?username=" + user_name)

        elif (username) and not (password or verify):
            if not email:
                self.write_form(username = user_name, email = e_mail, email_error = e_error, pass_error = p_error, verify_error = v_error )
            else:
                self.write_form(username = user_name, email = e_mail, pass_error = p_error, verify_error = v_error )

        elif not (username) and (password and verify):
            if not email:
                self.write_form(username = user_name, email = e_mail, email_error = e_error, name_error = n_error)
            else:
                self.write_form(username = user_name, email = e_mail, name_error = n_error )

        elif (username and password) and not (verify):
            if not email:
                self.write_form(username = user_name, email = e_mail, email_error = e_error, verify_error = v_error )
            else:
                self.write_form(username = user_name, email = e_mail, verify_error = v_error )

        elif not (username and password and verify):
            if not email:
                self.write_form(username = user_name, email = e_mail, email_error = e_error, verify_error = v_error, pass_error = p_error, name_error = n_error )
            else:
                self.write_form(username = user_name, email = e_mail, verify_error = v_error, pass_error = p_error, name_error = n_error )




class WelcomeHandler(Index):
    def get(self):
        username = self.request.get('username')
        response = "<h1>"+"Welcome, " + username + "! "+ "</h1>"
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', WelcomeHandler),
], debug=True)
