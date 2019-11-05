'''Cube puzzles - five typical 3x3x3 3D puzzles.

(c) Peter Ulbrich, 2019

a demo script for the sceneKit wrapper package for Pythonista

See the README.md for details.

'''

from objc_util import *
import ui
from markdown2 import markdown

from data import *
import main
import selector

TEMPLATE = '''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>Preview</title>
<style type="text/css">
body {
        font-family: helvetica;
        font-size: 15px;
        margin: 10px;
}
</style>
</head>
<body>{{CONTENT}}</body>
</html>
'''

class Hud:
  def __init__(self):
    self.views = []

    _, _, w, h = data.main_view.frame

    self.close_button = ui.Button()
    self.close_button.action = self.closeClick
    self.close_button.image = ui.Image.named('iob:close_round_24')
    data.main_view.add_subview(self.close_button)
    self.views.append(self.close_button)

    self.back_button = ui.Button()
    self.back_button.action = self.backClick
    self.back_button.image = ui.Image.named('iob:arrow_left_a_24')
    self.back_button.hidden = True
    data.main_view.add_subview(self.back_button)
    self.views.append(self.back_button)

    self.restart_button = ui.Button()
    self.restart_button.action = self.restartClick
    self.restart_button.image = ui.Image.named('iob:refresh_24')
    self.restart_button.hidden = True
    data.main_view.add_subview(self.restart_button)
    self.views.append(self.restart_button)

    self.hint_button = ui.Button()
    self.hint_button.action = self.hintClick
    self.hint_button.image = ui.Image.named('iob:help_24')
    data.main_view.add_subview(self.hint_button)
    self.views.append(self.hint_button)

    self.alert_label = ui.Label()
    self.alert_label.background_color = 'transparent'
    self.alert_label.text = ''
    self.alert_label.font = ('<system-bold>', 96)
    self.alert_label.alignment = ui.ALIGN_CENTER
    self.alert_label.hidden = True
    self.alert_label.alpha = 0.0
    data.main_view.add_subview(self.alert_label)
    self.views.append(self.alert_label)

    self.status_label = ui.Label()
    self.status_label.background_color = 'transparent'
    self.status_label.alignment = ui.ALIGN_CENTER
    self.status_label.line_break_mode = ui.LB_CHAR_WRAP
    self.status_label.number_of_lines = 2
    self.status_label.text = ''
    self.status_label.font = ('<system-bold>', 8)
    data.main_view.add_subview(self.status_label)
    self.views.append(self.status_label)
    
    self.title_label = ui.Label()
    self.title_label.background_color = 'transparent'
    self.title_label.alignment = ui.ALIGN_CENTER
    self.title_label.number_of_lines = 1
    self.title_label.text = ''
    self.title_label.font = ('<system-bold>', 22)
    data.main_view.add_subview(self.title_label)
    self.views.append(self.title_label)

  @on_main_thread
  def show_alert(self, message_symbol):
    def animation_fade_in():
      self.alert_label.alpha = 1.0
    def animation_fade_out():
      self.alert_label.alpha = 0.0
    def animate_fade_out():
      ui.animate(animation_fade_out, duration=2.0)
    def hide_alert():
      self.alert_label.hidden = True

    ui.cancel_delays()
    self.alert_label.text = message_symbol
    self.alert_label.hidden = False
    ui.animate(animation_fade_in, duration=0.8)
    ui.delay(animate_fade_out, 2)
    ui.delay(hide_alert, 5)

  def set_status(self, text):
    self.status_label.text = text
    
  def set_title(self, text):
    self.title_label.text = text

  def bring_to_front(self):
    for aView in self.views:
      aView.bring_to_front()

  @on_main_thread
  def hintClick(self, sender):
    data.active_stage.hint()

  @on_main_thread
  def restartClick(self, sender):
    data.active_stage.restart()

  @on_main_thread
  def backClick(self, sender):
    data.hud_layer.set_title('')
    main.MainViewController.next_stage(selector.SelectorStage())

  @on_main_thread
  def closeClick(self, sender):
    data.main_view.close()
    ui.delay(self.exit, 2.0)

  def exit(self):
    raise SystemExit()
    
  def show_generic_help(self):
    with open('README.md', 'r') as fp:
      text = fp.read()
    converted = markdown(text)
    html = TEMPLATE.replace('{{CONTENT}}', converted)
    webview = ui.WebView(name='Read me')
    webview.load_html(html)
    webview.present()

  def layout(self):
    _, _, w, h = data.main_view.frame
    self.close_button.frame = (0, 12, 40, 40)
    self.back_button.frame = (w - 40, 12, 40, 40)
    self.restart_button.frame = (0, h - 12 - 40, 40, 40)
    self.hint_button.frame = (w - 40, h - 12 - 40, 40, 40)
    self.title_label.frame = ((w - w // 2) // 2, 12, w // 2, 40)
    self.status_label.frame = ((w - w // 2) // 2, h - 12 - 40, w // 2, 40)
    self.alert_label.frame = ((w - 160) / 2, (h - 160) / 2, 160, 160)


if __name__ == '__main__':
  main.MainViewController.run()

