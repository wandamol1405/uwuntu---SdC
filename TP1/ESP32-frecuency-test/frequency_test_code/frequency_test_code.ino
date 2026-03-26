unsigned long startTime;
unsigned long endTime;

void setup() {
  Serial.begin(115200);

  int frequency = 240;

  setCpuFrequencyMhz(frequency); 

  delay(2000); // tiempo para abrir el monitor serie

  Serial.println("Inicio prueba...");
  Serial.print("Frecuencia seteada a: ");
  Serial.print(frequency);
  Serial.println("MHz");
  
  // -------- INT --------
  Serial.println("Calculando suma de enteros...");
  volatile int sumaInt = 0;
  startTime = millis();

  for (long i = 0; i < 50000000; i++) {
    sumaInt += i;
  }

  endTime = millis();
  Serial.print("Tiempo enteros: ");
  Serial.print(endTime - startTime);
  Serial.println(" milisegundos");

  // -------- FLOAT --------
  Serial.println("Calculando suma de flotantes...");
  volatile float sumaFloat = 0;
  startTime = millis();

  for (long i = 0; i < 50000000; i++) {
    sumaFloat += i * 0.1;
  }

  endTime = millis();
  Serial.print("Tiempo float: ");
  Serial.print(endTime - startTime);
  Serial.println(" milisegundos");
}

void loop() {}