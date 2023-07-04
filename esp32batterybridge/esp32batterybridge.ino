#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "TP-Link_3logytech";
const char* password =  "3logytech1928";

const int mqttPort = 8883;
const char* mqttServer = "192.168.0.104";
const char* mqttTopic = "battery/telemetry";
const char* mqttClientId = "esp32-gateway";

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// TODO: create a mqtt server inside azure iot edge module
// esp32gateway -> mqttServer module -routethru-> battery module

void setupWifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("connecting to wifi...");
  }
  Serial.print("Wifi connected to ");
  Serial.println(WiFi.localIP());
}

void MQTTConnect() {
  
  while (!mqttClient.connected()) {
    Serial.print("MQTT : Attempting MQTT connection...");
    if (mqttClient.connect(mqttClientId)) {
      Serial.println("MQTT connected");

      // Once connected, publish an announcement...
      // mqttClient.publish("esp32/","hello");

      // Subscribe to topics, one topic per line.
      mqttClient.subscribe(mqttTopic);
    } else {
      Serial.print("MQTT : Failed to connect to MQTT , rc=");
      Serial.print(mqttClient.state());
      Serial.println("MQTT : Trying again to connect to MQTT in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.println(topic);
  Serial.print("received message: ");
  //when message is received forward it to server TODO
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  randomSeed(analogRead(0));
  setupWifi();

  mqttClient.setServer(mqttServer, mqttPort);
  mqttClient.setCallback(callback);
}

void loop() {
  //Connect to MQTT and reconnect if connection drops
  if (!mqttClient.connected()) {
    MQTTConnect();
  }
  mqttClient.loop();

  int battery_id = random(0,20);
  String ble_uuid = "abcdeg";
  float humidity = random(0,1000) / 100.0;
  float temperature = random(0,1000) / 100.0;
  float internal_series_resistance = random(0,1000) / 100.0;
  float internal_impedance = random(0,1000) / 100.0;
  String message = "{'battery_id':"+String(battery_id) + ", 'ble_uuid': '"+ble_uuid + "', 'humidity': "+String(humidity) + ", 'temperature': "+String(temperature) +
    ", 'internal_series_resistance': "+String(internal_series_resistance) + ", 'internal_impedance': "+String(internal_impedance) + ", ";

  mqttClient.publish(mqttTopic, message.c_str());
  delay(100);
}
