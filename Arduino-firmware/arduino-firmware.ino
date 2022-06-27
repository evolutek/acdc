#include <Adafruit_SleepyDog.h>

#define SERIAL_SPEED 115200
#define SERIAL_TIMEOUT 100
char frame[32];
unsigned short frame_index = 0;
unsigned long last_byte_received;

#define FRAME_START_FLAG 0x42

enum index_e {
  flag = 0,
  command = 1,
  size = 2,
  data = 3
};

enum command_e {
  reset = 0x00,
  _setup = 0x01,
  ping = 0x02,
  set_prop_speed = 0x03,
  set_direct_angle = 0x04,
  set_color = 0x05,
  set_max_speed = 0x06,
  get_batt_voltage = 0x07
};

#define STATUS_PIN 2
#define STATUS_TOGGLE_DELAY_BEFORE_RESET 250
#define STATUS_TOGGLE_DELAY 500
bool status_pin_state = false;
unsigned long last_status_pin_toggle;

#define PDT_GAIN (510.0 / (150.0 + 510.0))

#define PMW2_DIRECT 5
#define PMW1_DIRECT 6
#define LIMIT_PORT_DIRECT A1
#define RRS_DIRECT 0.15
#define CURRENT_LIMIT_DIRECT 2.5

#define PMW2_PROP 9
#define PMW1_PROP 10
#define LIMIT_PORT_PROP A0
#define RRS_PROP 0.15
#define CURRENT_LIMIT_PROP 2.5
uint8_t propulsionMaxSpeed = 100; 

#define BATT_PIN A2
#define BATT_COEFF 2

bool wasSetup = false;

void setMotorCurrentLimit(bool isDirection, float current)
{
  float vRef = current * 10 * (isDirection ? RRS_DIRECT : RRS_PROP);
  // FIXME : No analog out
  analogWrite((isDirection ? LIMIT_PORT_DIRECT : LIMIT_PORT_PROP), min((vRef / PDT_GAIN) * 51, 255));
}

void setPropulsionSpeed(uint8_t reverse, uint8_t speed)
{
  uint8_t newSpeed = speed / 100.0f * propulsionMaxSpeed;
  analogWrite((reverse ? PMW2_PROP : PMW1_PROP), map(newSpeed, 0, 100, 0, 255));
  analogWrite((reverse ? PMW1_PROP : PMW2_PROP), 0);
}

void setup()
{
  Serial.begin(SERIAL_SPEED);
  Serial.println("Hello world");

  pinMode(STATUS_PIN, OUTPUT);
  digitalWrite(STATUS_PIN, status_pin_state);
  last_status_pin_toggle = millis();

  pinMode(PMW2_DIRECT, OUTPUT);
  pinMode(PMW1_DIRECT, OUTPUT);
  pinMode(LIMIT_PORT_DIRECT, OUTPUT);
  digitalWrite(LIMIT_PORT_DIRECT, HIGH);
  //setMotorCurrentLimit(false, 2.5);

  pinMode(PMW2_PROP, OUTPUT);
  pinMode(PMW1_PROP, OUTPUT);
  pinMode(LIMIT_PORT_PROP, OUTPUT);
  digitalWrite(LIMIT_PORT_PROP, HIGH);
  //setMotorCurrentLimit(false, 2.5);
  setPropulsionSpeed(true, 0);
  
  //Watchdog.enable(4000);
}

void process_command(void)
{
  if (frame[flag] != FRAME_START_FLAG || frame[command] > set_max_speed)
    return;

  Watchdog.reset();

  if (frame[command] == reset)
  {
    Watchdog.disable();
    Watchdog.enable(15);
    while (true);;
  }

  if (frame[command] == _setup)
  {
    wasSetup = true;
    propulsionMaxSpeed = frame[data + 3] & 0x64;

    Serial.print(FRAME_START_FLAG);
    Serial.print(_setup);
    Serial.println(0x00);
  }

  if (!wasSetup)
    return;

  if (frame[command] == set_prop_speed)
  {
    uint8_t reverse = (frame[data] >> 8) & 0x01;
    uint8_t speed = frame[data] & 0x7F;
    setPropulsionSpeed(reverse, speed);    
  }

  // TODO :
  // - set direction angle
  // - set color

  if (frame[command] == set_max_speed)
  {
    propulsionMaxSpeed = frame[data + 3] & 0x64;
  }

  if (frame[command] == get_batt_voltage)
  {
    uint8_t voltage = min(map(analogRead(BATT_PIN), 0, 4095, 0, 5) * BATT_COEFF, 20);
    Serial.print(FRAME_START_FLAG);
    Serial.print(_setup);
    Serial.print(0x01);
    Serial.println(voltage);
  }
}

void loop()
{
  
  if (millis() - last_status_pin_toggle > (wasSetup ? STATUS_TOGGLE_DELAY : STATUS_TOGGLE_DELAY_BEFORE_RESET))
  {
    status_pin_state = !status_pin_state;
    digitalWrite(STATUS_PIN, status_pin_state);
    last_status_pin_toggle = millis();
  }

  if (frame_index != 0 && millis() - last_byte_received > SERIAL_TIMEOUT)
    frame_index = 0;

  if (Serial.available() > 0)
  {
    frame[frame_index] = Serial.read();

    frame_index++;
    last_byte_received = millis();
  }

  if (frame_index > size && frame_index + size > frame[size])
  {
    process_command();
    frame_index = 0;
  }
}
