import tornado.ioloop
import tornado.template
import tornado.web

flag = open('flag.txt').read()
secret = open('secret.txt').read()

TEMPLATE = '''
<html>
 <head><title> Hello User</title></head>
 <body style="background: #F5F5DC;text-align:center;">
 <h1 style="font-size:5rem;"> Usual Student Food </h1>
 <br />
 <p style="font-size:2rem;"> 
 <p>What type of food do you like?</p>
 <form method="GET"  action='/'>
  <select id="food" name="food">
      <option value="{{!pizza}}">pizza</option>
      <option value="{{!hotcakes}}">hotcakes</option>
      <option value="{{!pancakes}}">pancakes</option>
  </select>
  <input type="submit"></input>
 </form>
 <p>FOO</p>
 </p>
 <br/> <br/>
 <p style="text-align:center; font-size:2rem;">
 Oh I heard you're finding my secret. <br>
 <b>{{secret}}</b>
 </p>
 </body>
</html>
'''


class MainHandler(tornado.web.RequestHandler):

    def get(self):

        pizza = "pizza"
        hotcakes = 'hotcakes'
        pancakes = 'pancakes'

        template_data = TEMPLATE.replace("FOO", self.get_argument('food', ''))
        t = tornado.template.Template(template_data)
        secret = "Unfortunately, you aren't lucky"
        if self.get_secure_cookie("admin") == b"true":
            secret = flag
        else:
            self.set_secure_cookie("admin", "false")
        self.write(t.generate(pizza=pizza, hotcakes=hotcakes, pancakes=pancakes, application=application,
                              secret=secret))


application = tornado.web.Application([
    (r"/", MainHandler)
], debug=True, static_path=None, template_path=None, cookie_secret=secret)

if __name__ == '__main__':
    application.listen(1111)
    print("Listening :)")
    tornado.ioloop.IOLoop.instance().start()
