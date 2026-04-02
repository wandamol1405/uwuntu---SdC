unsigned long startTime;
unsigned long endTime;

void setup()
{
  Serial.begin(115200);

  delay(3000);

  int frequency = 240;
  setCpuFrequencyMhz(frequency);

  Serial.println("Inicio prueba...");
  Serial.print("Frecuencia seteada a: ");
  Serial.print(frequency);
  Serial.println(" MHz");

  // -------- INT --------
  Serial.println("Calculando suma de enteros...");
  volatile int32_t sumaInt = 0;

  startTime = millis();

  for (long i = 0; i < 50000000; i++)
  {
    sumaInt += i;
  }

  endTime = millis();
  Serial.print("Tiempo enteros: ");
  Serial.print(endTime - startTime);
  Serial.println(" ms");

  // -------- FLOAT --------
  Serial.println("Calculando suma de flotantes...");
  volatile float sumaFloat = 0;

  startTime = millis();

  for (long i = 0; i < 50000000; i++)
  {
    sumaFloat += (float)i * 0.1f;
  }

  endTime = millis();
  Serial.print("Tiempo float: ");
  Serial.print(endTime - startTime);
  Serial.println(" ms");
}

void loop() {}