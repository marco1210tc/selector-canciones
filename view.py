import webview


class View:
  def __init__(self, api):
    webview.create_window('Organizador de Culto', "webui/app.html", text_select=True, js_api=api)
    webview.start(debug=True)