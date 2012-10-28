#include <LiquidCrystal.h>

#define TEST_LED_PIN 11
#define PASS_LED_PIN 10
#define FAIL_LED_PIN  9

#define BUTTON_PIN    8

#define ENCODER_A_PIN 2
#define ENCODER_B_PIN 3
#define ENCODER_INTERRUPT_A 0
#define ENCODER_INTERRUPT_B 1

#define LCD_RS_PIN    14
#define LCD_E_PIN     12
#define LCD_DB4_PIN    7
#define LCD_DB5_PIN    6
#define LCD_DB6_PIN    5
#define LCD_DB7_PIN    4

LiquidCrystal lcd(LCD_RS_PIN, LCD_E_PIN, LCD_DB4_PIN, LCD_DB5_PIN, LCD_DB6_PIN, LCD_DB7_PIN);

#define STEP_PIN      16
#define DIR_PIN       15
#define ENABLE_PIN    21
#define RESET_PIN     18
#define TQ1_PIN       20
#define TQ2_PIN       19
#define M1_PIN        17
#define M2_PIN        22
#define DCY1_PIN      23
#define DCY2_PIN      24
#define MO_PIN        25
#define PROTECT_PIN   26

#define PPR 1600

void setup()
{
  //setup our LEDS
  pinMode(TEST_LED_PIN, OUTPUT);
  pinMode(PASS_LED_PIN, OUTPUT);
  pinMode(FAIL_LED_PIN, OUTPUT);
  digitalWrite(TEST_LED_PIN, LOW);
  digitalWrite(PASS_LED_PIN, LOW);
  digitalWrite(FAIL_LED_PIN, LOW);

  //setup our button
  pinMode(BUTTON_PIN, INPUT);
  
  //setup our encoder pins
  pinMode(ENCODER_A_PIN, INPUT);
  pinMode(ENCODER_B_PIN, INPUT);
  attachInterrupt(ENCODER_INTERRUPT_A, read_quadrature_a, CHANGE);
  attachInterrupt(ENCODER_INTERRUPT_B, read_quadrature_b, CHANGE);  
  
  //initialize our serial port
  Serial.begin(115200);
  Serial.println("HoekDrive23 Test Fixture v1.0");
  
  //initialize our stepper driver
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(RESET_PIN, OUTPUT);
  pinMode(TQ1_PIN, OUTPUT);
  pinMode(TQ2_PIN, OUTPUT);
  pinMode(M1_PIN, OUTPUT);
  pinMode(M2_PIN, OUTPUT);
  pinMode(DCY1_PIN, OUTPUT);
  pinMode(DCY2_PIN, OUTPUT);
  pinMode(MO_PIB, INPUT);
  pinMode(PROTECT_PIN, INPUT);
  
  //setup our basic pins.
  digitalWrite(ENABLE_PIN, LOW); //default to disabled
  digitalWrite(RESET_PIN, HIGH); //default to not reset
  digitalWrite(STEP_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);

  //100% full torque (current)
  digitalWrite(TQ1_PIN, LOW);
  digitalWrite(TQ2_PIN, LOW);
  
  //normal 0% decay
  digitalWrite(DCY1_PIN, LOW);
  digitalWrite(DCY2_PIN, LOW);
}

volatile int encoder_position = 0;

void read_quadrature_a()
{  
  // found a low-to-high on channel A
  if (digitalRead(ENCODER_A_PIN) == HIGH)
  {   
    // check channel B to see which way
    if (digitalRead(ENCODER_B_PIN) == LOW)
        encoder_position++;
    else
        encoder_position--;
  }
  // found a high-to-low on channel A
  else                                        
  {
    // check channel B to see which way
    if (digitalRead(ENCODER_B_PIN) == LOW)
        encoder_position--;
    else
        encoder_position++;
  }
}

void read_quadrature_b()
{  
  // found a low-to-high on channel B
  if (digitalRead(ENCODER_B_PIN) == HIGH)
  {   
    // check channel A to see which way
    if (digitalRead(ENCODER_A_PIN) == LOW)
        encoder_position++;
    else
        encoder_position--;
  }
  // found a high-to-low on channel B
  else                                        
  {
    // check channel A to see which way
    if (digitalRead(ENCODER_A_PIN) == LOW)
        encoder_position--;
    else
        encoder_position++;
  }
}

void loop()
{
  lcd.print("Press start\nto begin test.");
  
  //wait until we get a button press.
  while (digitalRead(BUTTON_PIN))
    delay(1);
    
  //let em know.
  Serial.println("NEW TEST START.");
  
  //setup our leds.
  digitalWrite(TEST_LED_PIN, HIGH);
  digitalWrite(PASS_LED_PIN, LOW);
  digitalWrite(FAIL_LED_PIN, LOW);
    
  //run all our tests.
  boolean pass = false;
  while (true)
  {
    pass = test_full_fwd();
    if (!pass)
      break;

    pass = test_full_rev();
    if (!pass)
      break;

    pass = test_half_fwd();
    if (!pass)
      break;

    pass = test_half_rev();
    if (!pass)
      break;

    pass = test_1_8_fwd();
    if (!pass)
      break;

    pass = test_1_8_rev();
    if (!pass)
      break;

    pass = test_1_16_fwd();
    if (!pass)
      break;

    pass = test_1_16_rev();
    if (!pass)
      break;
      
    //okay, we're done.
    break;
  }
  
  //turn off our driver
  digitalWrite(RESET_PIN, LOW); //reset our board
  digitalWrite(RESET_PIN, HIGH); //reset our board
  digitalWrite(ENABLE_PIN, LOW); //default to disabled
  
  //setup our leds.
  digitalWrite(TEST_LED_PIN, LOW);
  digitalWrite(PASS_LED_PIN, pass);
  digitalWrite(FAIL_LED_PIN, !pass);
  
  //show the result.
  if (pass)
    Serial.println("BOARD PASSED.");
  else
    Serial.println("BOARD FAILED.");
  
  //wait until we get a button press.
  while (digitalRead(BUTTON_PIN))
    delay(1);
}

boolean measure_steps(int steps, int expected, int tolerance, int delay_time)
{
  //reset our position counter!
  encoder_position = 0;
  
  //do our steps
  for (int i=0; i<steps; i++)
  {
    digitalWrite(STEP_PIN, HIGH);
    delay(delay_time);
    digitalWrite(STEP_PIN, LOW);
    delay(1);
  }

  //log our results.
  Serial.print("EXPECTED: ");
  Serial.print(expected, DEC);
  Serial.print("TOLERANCE: ");
  Serial.print(tolerance, DEC);
  Serial.print("ACTUAL: ");
  Serial.print(encoder_position, DEC);
  Serial.println();
  
  //did it pass?
  return (encoder_position >= (expected - tolerance) && encoder_position <= (expected + tolerance));
}

boolean test_full_fwd()
{
  //configure all our pins.
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(M1_PIN, LOW);
  digitalWrite(M2_PIN, LOW);
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(DIR_PIN, HIGH);
  
  //okay, do our test.
  if (measure_steps(200, 1600, 10, 16))
  {
    lcd.print("FULL STEP FWD: PASS");
    Serial.println("FULL STEP FORWARD MODE: PASS");
    return true;
  }
  else
  {
    lcd.print("FULL STEP FWD: FAIL");
    Serial.println("FULL STEP FORWARD MODE: FAIL");
    return false;
  } 
}

boolean test_full_rev()
{
  //configure all our pins.
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(M1_PIN, LOW);
  digitalWrite(M2_PIN, LOW);
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);
  
  //okay, do our test.
  if (measure_steps(200, -1600, 10, 16))
  {
    lcd.print("FULL STEP REV: PASS");
    Serial.println("FULL STEP REVERSE MODE: PASS");
    return true;
  }
  else
  {
    lcd.print("FULL STEP REV: FAIL");
    Serial.println("FULL STEP REVERSE MODE: FAIL");
    return false;
  }
}

boolean test_half_fwd()
{
  //configure all our pins.
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(M1_PIN, HIGH);
  digitalWrite(M2_PIN, LOW);
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(DIR_PIN, HIGH);
  
  //okay, do our test.
  if (measure_steps(400, 1600, 10, 8))
  {
    lcd.print("HALF STEP FWD: PASS");
    Serial.println("HALF STEP FORWARD MODE: PASS");
    return true;
  }
  else
  {
    lcd.print("HALF STEP FWD: FAIL");
    Serial.println("HALF STEP FORWARD MODE: FAIL");
    return false;
  }
}

boolean test_half_rev()
{
  //configure all our pins.
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(M1_PIN, HIGH);
  digitalWrite(M2_PIN, LOW);
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);
  
  //okay, do our test.
  if (measure_steps(400, -1600, 10, 8))
  {
    lcd.print("HALF STEP REV: PASS");
    Serial.println("HALF STEP REVERSE MODE: PASS");
    return true;
  }
  else
  {
    lcd.print("HALF STEP REV: FAIL");
    Serial.println("HALF STEP REVERSE MODE: FAIL");
    return false;
  }
}

boolean test_1_8_fwd()
{
  //configure all our pins.
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(M1_PIN, HIGH);
  digitalWrite(M2_PIN, HIGH);
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(DIR_PIN, HIGH);
  
  //okay, do our test.
  if (measure_steps(800, 1600, 10, 4))
  {
    lcd.print("1/8 STEP FWD: PASS");
    Serial.println("1/8 STEP FORWARD MODE: PASS");
    return true;
  }
  else
  {
    lcd.print("1/8 STEP FWD: FAIL");
    Serial.println("1/8 STEP FORWARD MODE: FAIL");
    return false;
  } 
}

boolean test_1_8_rev()
{
  //configure all our pins.
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(M1_PIN, HIGH);
  digitalWrite(M2_PIN, HIGH);
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);
  
  //okay, do our test.
  if (measure_steps(800, -1600, 10, 4))
  {
    lcd.print("1/8 STEP REV: PASS");
    Serial.println("1/8 STEP REVERSE MODE: PASS");
    return true;
  }
  else
  {
    lcd.print("1/8 STEP REV: FAIL");
    Serial.println("1/8 STEP REVERSE MODE: FAIL");
    return false;
  } 
}

boolean test_1_16_fwd()
{
  //configure all our pins.
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(M1_PIN, LOW);
  digitalWrite(M2_PIN, HIGH);
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(DIR_PIN, HIGH);
  
  //okay, do our test.
  if (measure_steps(3200, 1600, 10, 1))
  {
    lcd.print("1/16 STEP FWD: PASS");
    Serial.println("1/16 STEP FORWARD MODE: PASS");
    return true;
  }
  else
  {
    lcd.print("1/16 STEP FWD: FAIL");
    Serial.println("1/16 STEP FORWARD MODE: FAIL");
    return false;
  }
}

boolean test_1_16_rev()
{
  //configure all our pins.
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(M1_PIN, LOW);
  digitalWrite(M2_PIN, HIGH);
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);
  
  //okay, do our test.
  if (measure_steps(3200, -1600, 10, 1))
  {
    lcd.print("1/16 STEP REV: PASS");
    Serial.println("1/16 STEP REVERSE MODE: PASS");
    return true;
  }
  else
  {
    lcd.print("1/16 STEP REV: FAIL");
    Serial.println("1/16 STEP REVERSE MODE: FAIL");
    return false;
  }
}
