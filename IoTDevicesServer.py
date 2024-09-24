import time
import RPi.GPIO as GPIO
import OneWire
from OneWire import DS18B20

from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_json_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _set_html_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/status'
        try:
            self.htmlDoc = ""
            print('path: ' + self.path)
            if self.path == '/setOn': 
                GPIO.output(21, GPIO.HIGH)
                self._set_html_headers()
                self.htmlDoc = "On"
            elif self.path == '/setOff': 
                GPIO.output(21, GPIO.LOW)
                self._set_html_headers()
                self.htmlDoc = "Off"
            if self.path == '/status': 
                self.htmlDoc = self.build_StatusPage()
                self._set_html_headers()
            elif self.path == '/statusjson':
                temps = DS18B20.readTemps()
                temps["relayStatus"] = GPIO.input(21)
                self.htmlDoc = temps
                self._set_json_headers()
            self.wfile.write(bytes(str(self.htmlDoc), 'utf-8')) 
        except Exception as e:
            print(str(e))
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def build_StatusPage(self):
        relayPin = GPIO.input(21)
        relayStatus = ("On" if relayPin else "Off")
        setRelay = ("Off" if relayPin else "On")

        htmlDoc = "<!DOCTYPE html>" \
        "<html>" \
        "<body>" \
        "<h1><a href='/set" + setRelay + "'>" + "Relay " + relayStatus + "</a></h1><br>"

        try:
            tempJson = DS18B20.readTemps()
#            htmlDoc += "<br>" + str(tempJson)
            temperatureSensors = tempJson["temperatureSensors"]
            print(str(temperatureSensors))
            for sensor in temperatureSensors:
                try:
                    print(str(sensor))
                    print(sensor['id'])
                    t = sensor['temperature_C']
                    print("t")
                    print(t)
                    htmlDoc += "id: " + sensor["id"] + ": " + str(sensor["temperature_C"]) + "<br>"
                except Exception as e:
                    print("fel")
                    print(str(e))
        except Exception as e:
            print(str(e))
        
        htmlDoc += "</body></html>"

        return htmlDoc

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()