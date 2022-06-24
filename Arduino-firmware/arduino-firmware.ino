#define SERIAL_SPEED 115200
#define SERIAL_TIMEOUT 100
char frame[32];
unsigned short frame_index = 0;
unsigned long last_byte_received;

enum command {
  reset = 0x01,
  _setup = 0x02,
  ping = 0x03,
  set_prop_speed = 0x04,
  set_direct_angle = 0x05,
  set_color = 0x06,
  set_max_speed = 0x07
};

#define STATUS_PIN 2
#define STATUS_TOGGLE_DELAY_BEFORE_RESET 250
#define STATUS_TOGGLE_DELAY 500
bool status_pin_state = false;
unsigned long last_status_pin_toggle;

#define PMW2_DIRECT 5
#define PMW1_DIRECT 6

#define PMW2_PROP 9
#define PMW1_PROP 10
uint8_t propulsionMaxSpeed = 100; 

bool wasSetup = false;

void setPropulsionSpeed(uint8_t reverse, uint8_t speed)
{
  uint8_t newSpeed = speed / 100.0f * propulsionMaxSpeed;
  analogWrite((reverse ? PMW2_PROP : PMW1_PROP), map(newSpeed, 0, 100, 0, 255));
  analogWrite((reverse ? PMW1_PROP : PMW2_PROP), map(newSpeed, 0, 100, 0, 255));
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(SERIAL_SPEED);

  pinMode(STATUS_PIN, OUTPUT);
  digitalWrite(STATUS_PIN, status_pin_state);
  last_status_pin_toggle = millis();

  pinMode(PMW2_DIRECT, OUTPUT);
  pinMode(PMW1_DIRECT, OUTPUT);

  pinMode(PMW2_PROP, OUTPUT);
  pinMode(PMW1_PROP, OUTPUT);
  setPropulsionSpeed(false, 0);
  
}

void loop() {
  // put your main code here, to run repeatedly:

  if (millis() - last_status_pin_toggle > (wasSetup ? STATUS_TOGGLE_DELAY : STATUS_TOGGLE_DELAY_BEFORE_RESET))
  {
    status_pin_state != status_pin_state;
    last_status_pin_toggle = millis();
  }

  if (frame_index != 0 && millis() - last_byte_received > SERIAL_TIMEOUT)
    frame_index = 0;

  if (Serial.available() > 0)
  {
    frame[frame_index] = Serial.read();

    // FIXME

    frame_index++;
    last_byte_received = millis();
  }

}
