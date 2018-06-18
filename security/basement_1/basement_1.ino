//basement 1
//pin 1,2,3,4,5 are reed switches
/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#define PIN0 16
#define PIN1 5
#define PIN2 4
#define PIN3 0
#define PIN4 2
#define PIN5 14

#include <ESP8266WiFi.h>

#define NUMPINS 4

int pins[] = {16, 5, 4, 0 , 2, 14};

const char* ssid     = "sectwo";
const char* password = "prantropic11";

const char* host = "192.168.1.10";

void setup() {
  Serial.begin(115200);
  delay(10);
  for (int a = 0; a < NUMPINS; a++)
    pinMode(a, INPUT_PULLUP);
 
  // We start by connecting to a WiFi network

  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

int value = 0;

void loop() {
  delay(5000);
  ++value;

  Serial.print("connecting to ");
  Serial.println(host);
  
  // Use WiFiClient class to create TCP connections
  
  WiFiClient client;
  const int ourport = 8080;
  if (!client.connect(host, ourport)) {
    Serial.println("connection failed");
    return;
  }
  

  Serial.print("Sending Data");
  //Serial.println(url);
  
  // This will send the request to the server
  
  while (1) { 
    
    for (int a=0; a < NUMPINS; a++){
      int sensorVal = digitalRead(pins[a]);
      client.print(String(WiFi.localIP()) + " " + String(a) + String(" Pin Status:") + sensorVal+'.');
    }
    unsigned long timeout = millis();
  //  while (client.available() == 0) {
    //  if (millis() - timeout > 100) {
      //  Serial.println(">>> Client Timeout !");
     //   client.stop();
     //   return;
    //  }
   // }
  
    // Read all the lines of the reply from server and print them to Serial
    while(client.available()){
      String line = client.readStringUntil('\r');
      Serial.print(line);
   }
    delay(500);
  }
  
}

