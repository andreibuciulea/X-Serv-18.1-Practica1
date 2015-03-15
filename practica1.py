#!/usr/bin/python
# -*- coding: utf-8 -*-
import webapp
import socket


usuario = socket.gethostname()


class miweb(webapp.webApp):
    dic = {}
    dic1 = {}
    form = "<html><body><form method=post>\
            URL: <input type=text name=fname><br>\
            <input type=submit value=Submit>\
            </form></body></html>"
    error = "<html><body><h1>Error</h1></body></html>"

    def parse(self, request):
        operacion = request.split()[0]
        recurso = request.split()[1]
        cuerpo = request.split("\r\n\r\n")[1]
        url = cuerpo.split("=")[-1]
        url = url.replace("%2F", "/").replace("%3A", ":")
        return (operacion, recurso, url)

    def process(self, parsedRequest):
        (operacion, recurso, url) = parsedRequest
        if operacion == "GET" and recurso == "/":
            return ("200 OK", self.form)
        elif operacion == "GET":
            recurso = recurso.split("/")[1]
            if recurso in self.dic1:
                direccion = self.dic1[recurso]
                return ("200 OK", "<html><head><META http-equiv=refresh\
                        content=2;URL=" + direccion + "></head></html>\r\n")
            else:
                return ("404 Not found", error)

        elif operacion == "POST":
            if url in self.dic:
                return ("200 OK", self.form)
            else:
                comienzo = url.split("//")[0]
                if comienzo == "http:" or comienzo == "https:":
                    self.dic[url] = str(len(self.dic))
                    self.dic1[str(len(self.dic1))] = url
                    return ("200 OK", self.form)
                else:
                    url = "http://" + url
                    self.dic[url] = str(len(self.dic))
                    self.dic1[str(len(self.dic1))] = url
                    return ("200 OK", self.form)

if __name__ == "__main__":
    acortador = miweb(usuario, 1234)
