#include <stdint.h>              // Tipos de datos enteros de tamaño fijo (uint32_t, int16_t, etc.)
#include <stdbool.h>             // Tipo booleano (bool) con valores true y false
#include "inc/hw_memmap.h"       // Mapa de memoria del hardware, define las direcciones base de los periféricos (GPIO, UART, etc.)
#include "driverlib/sysctl.h"    // Funciones de control del sistema (configuración de reloj, habilitación de periféricos)
#include "driverlib/gpio.h"      // Control de los pines GPIO (configuración de entrada/salida, lectura y escritura de pines)
#include "driverlib/pin_map.h"   // Asignación de funciones a los pines (mapeo de pines para UART, PWM, etc.)
#include "driverlib/timer.h"     // Funciones para controlar los temporizadores (configuración, inicio, interrupciones)
#include "driverlib/interrupt.h" // Manejo de interrupciones (habilitar/deshabilitar interrupciones, configurar manejadores)
#include "inc/hw_ints.h"         // Definición de las interrupciones del hardware (vectores de interrupción)
#include "driverlib/pwm.h"       // Control del módulo PWM (configuración, generación de señales PWM)
#include "driverlib/uart.h"      // Control del módulo UART (envío y recepción de datos seriales)
#include "utils/uartstdio.c"     // Funciones auxiliares para la entrada/salida por UART (UARTprintf, UARTgets)
#include <string.h>  // Para usar strcmp()
#define MAX_BUFFER_SIZE 100  // Tamaño máximo del buffer para almacenar la frase

// Definir pines para el sensor ULTRASONICO Trig y Echo
#define TRIG_PIN GPIO_PIN_4
#define ECHO_PIN GPIO_PIN_5
#define TRIG_PORT GPIO_PORTA_BASE
#define ECHO_PORT GPIO_PORTA_BASE
// Definir pines para los motores
#define MOTOR1DER GPIO_PIN_0
#define MOTOR1IZQ GPIO_PIN_1
#define MOTOR2DER GPIO_PIN_2
#define MOTOR2IZQ GPIO_PIN_3
#define PUERTOMOTRORES GPIO_PORTE_BASE
// Definir pines para los leds internos
#define LED1I GPIO_PIN_1
#define LED2I GPIO_PIN_0
#define LED3I GPIO_PIN_4
#define LED4I GPIO_PIN_0
#define PUERTOLEDSIN1 GPIO_PORTN_BASE
#define PUERTOLEDSIN2 GPIO_PORTF_BASE
// Definir pines para los leds externos
#define LED1 GPIO_PIN_0
#define LED2 GPIO_PIN_1
#define LED3 GPIO_PIN_2
#define LED4 GPIO_PIN_3
#define PUERTOLEDS GPIO_PORTK_BASE
// Denfinir pin del buzzer
#define BUZZER GPIO_PIN_4
#define PUERTOBUZZER GPIO_PORTB_BASE
// Definicion del motor de la garra 

uint32_t distance;
uint32_t contador = 0;
uint32_t startTime, endTime, duration;

uint32_t ui32SysClock;           // Variable para almacenar la frecuencia del reloj del sistema
char uartBuffer[MAX_BUFFER_SIZE]; // Buffer para almacenar la frase recibida
volatile uint8_t bufferIndex = 0; // Índice del buffer

#define duty 255 // ciclo de trabajo maximo del pwm en este caso debe de ser el tamaño de la resolucion de bist del adc 12bits
uint32_t ui32SysClock;  // Variable para almacenar la frecuencia del reloj del sistema
uint8_t estado;         //variable para cambiar el estado del led en la interrupcion
uint8_t estado1;  
uint8_t estado2;
uint8_t estado3;
uint8_t estado4;
uint8_t state ;
static void configureSysClock(void);
static void config_timer(void);
static void config_timer1(void);
static void config_timer2(void);
static void config_timer3(void);
static void config_timer4(void);
static void config_timer5(void);
static void config_timer6(void);
static void configureUART0(void);
static void config_pwm(void);           // Inicializar PWM
static void config_gpio(void);
static void config_ultrasonico(void);
void medir_distancia(void);
void girar(void);
void luces(void);
void apagado(void);
void apagado_avance(void);
void apagado_ledin(void);
void avance(void);
void buzzer(void);
void lucestraseras(void);

//
int main(void) {
    configureSysClock();  // Configurar el sistema a 120 MHz
    config_timer();       // configuracion del temporizador con interrupción
    configureUART0();        // configuracion del UART
    config_pwm();         // configuracion del PWM
    config_gpio();        // configuracion de los GPIOs
    config_timer1();      // configuracion del timer1
    config_timer2();
    config_timer3();
    config_timer4();
    config_timer5();
    config_timer6();
    config_ultrasonico(); // configuracion del sensor ultrasonico 
    apagado();

    // Bucle principal (no se necesita hacer nada aquí ya que la interrupción maneja el LED)
    while (1) {
        
        //PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, width);
    }
}
void lucestraseras(void){
    estado3 = GPIOPinRead(PUERTOLEDS, LED3);
    GPIOPinWrite(PUERTOLEDS, LED3, estado3 ^ LED3);  // Alternar el LED
    estado4 = GPIOPinRead(PUERTOLEDS, LED4);
    GPIOPinWrite(PUERTOLEDS, LED4, estado4 ^ LED4);  // Alternar el LED
}
void avance(void){
    if(distance > 8 && distance < 25){
        GPIOPinWrite(PUERTOMOTRORES, MOTOR1DER, MOTOR1DER);
        GPIOPinWrite(PUERTOMOTRORES, MOTOR2IZQ, MOTOR2IZQ);
        GPIOPinWrite(PUERTOMOTRORES, MOTOR1IZQ, 0x00);
        GPIOPinWrite(PUERTOMOTRORES, MOTOR2DER, 0x00);
        // Imprimir la distancia
        UARTprintf("%d\r\n", (int)distance);
        state=1;
    }
    else if (distance <=8)
    {
        UARTprintf("adelante\n");
        apagado_avance();
        state = 1;

    }
    else{
        // Imprimir la distancia
        UARTprintf("%d\r\n", (int)distance);
        apagado_ledin();
    }
    

}
void girar(void){
    GPIOPinWrite(PUERTOMOTRORES, MOTOR2IZQ, MOTOR2IZQ);
    GPIOPinWrite(PUERTOMOTRORES, MOTOR1IZQ, MOTOR1IZQ);
    GPIOPinWrite(PUERTOMOTRORES, MOTOR2DER, 0x00);
    GPIOPinWrite(PUERTOMOTRORES, MOTOR1DER, 0x00);
    state =0;
}
void luces(void){
    estado = GPIOPinRead(PUERTOLEDSIN1, LED1I);
    GPIOPinWrite(PUERTOLEDSIN1, LED1I, estado ^ LED1I);  // Alternar el LED
    estado1 = GPIOPinRead(PUERTOLEDSIN2, LED3I);
    GPIOPinWrite(PUERTOLEDSIN2, LED3I, estado1 ^ LED3I);  // Alternar el LED
}
void apagado(void){

    GPIOPinWrite(PUERTOBUZZER, BUZZER, 0x00);  //
    GPIOPinWrite(PUERTOLEDS, LED3, 0x00); 
    GPIOPinWrite(PUERTOLEDS, LED4, 0x00);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, 2);
}
void apagado_avance(void){
    GPIOPinWrite(PUERTOMOTRORES, MOTOR2IZQ, 0x00);
    GPIOPinWrite(PUERTOMOTRORES, MOTOR1IZQ, 0x00);
    GPIOPinWrite(PUERTOMOTRORES, MOTOR2DER, 0x00);
    GPIOPinWrite(PUERTOMOTRORES, MOTOR1DER, 0x00);
    state =1;
}
void apagado_ledin(void){
    GPIOPinWrite(PUERTOLEDSIN1, LED1I, 0x00);  // Alternar el LED
    GPIOPinWrite(PUERTOLEDSIN2, LED3I, 0x00);  // Alternar el LED
}
void buzzer(void){
    estado2 = GPIOPinRead(PUERTOBUZZER, BUZZER);
    GPIOPinWrite(PUERTOBUZZER, BUZZER, estado2 ^ BUZZER);  //
}
// Manejador de la interrupción de UART0 (cuando se recibe un dato)
void UART0IntHandler(void){
    uint32_t ui32Status;
    char receivedChar;

    // Obtener y limpiar el estado de la interrupción
    ui32Status = UARTIntStatus(UART0_BASE, true);
    UARTIntClear(UART0_BASE, ui32Status);

    // Procesar los datos mientras haya en el FIFO
    while (UARTCharsAvail(UART0_BASE)) {
        // Leer el carácter recibido
        receivedChar = UARTCharGetNonBlocking(UART0_BASE);

        // Si es un retorno de carro o salto de línea, la frase está completa
        if (receivedChar == '\r' || receivedChar == '\n') {
            uartBuffer[bufferIndex] = '\0'; // Terminar la cadena con el carácter nulo
            UARTprintf("Datos recibidos: %s\r\n", uartBuffer);  // Imprimir la frase recibida
            bufferIndex = 0; // Reiniciar el buffer para la siguiente frase
        }
        else {
            if (bufferIndex < MAX_BUFFER_SIZE - 1) {
                uartBuffer[bufferIndex++] = receivedChar; // Agregar el carácter al buffer
            }
            else {
                UARTprintf("Buffer lleno, frase demasiado larga.\r\n");
                bufferIndex = 0; // Reiniciar el buffer
            }
        }
    }
}
// Función de manejo de la interrupción del temporizador
void Timer0IntHandler(void){
    // Limpiar la interrupción del temporizador para poder seguir generando interrupciones
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    medir_distancia();
}
void Timer1IntHandler(void){
    // Limpiar la interrupción del temporizador para poder seguir generando interrupciones
    TimerIntClear(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
}
void Timer2IntHandler(void){
    // Limpiar la interrupción del temporizador para poder seguir generando interrupciones
    TimerIntClear(TIMER2_BASE, TIMER_TIMA_TIMEOUT);
    if (strcmp(uartBuffer, "girar" ) == 0  ) {
        // Imprimir la distancia
        UARTprintf("%d\r\n", (int)distance);
        girar(); 
    }
    else{
        apagado_ledin();
    }

}
void Timer3IntHandler(void){
    TimerIntClear(TIMER3_BASE, TIMER_TIMA_TIMEOUT);
    avance();

 }
void Timer4IntHandler(void){
    TimerIntClear(TIMER4_BASE, TIMER_TIMA_TIMEOUT);
    if(distance<=8){
        buzzer();
        lucestraseras();
    }
    else{
        apagado();
    }
 }
 void Timer5IntHandler(void){
    TimerIntClear(TIMER5_BASE, TIMER_TIMA_TIMEOUT);
    if(distance<=8){
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, contador);
        contador=contador+5;
        if(contador == 255){
            contador=0;
        }
    }
    else{
            PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, 2);
    }
 }
void Timer6IntHandler(void){
    TimerIntClear(TIMER6_BASE, TIMER_TIMA_TIMEOUT);
    if (state == 0  ) {
        luces(); 
    }
}
//Funcion para medir distancia
void medir_distancia(void){ 
    // Enviar pulso de 10 us en el pin Trig
    GPIOPinWrite(TRIG_PORT, TRIG_PIN, TRIG_PIN);
    SysCtlDelay(400);  // Ajustar el valor para 10 us aproximadamente

    GPIOPinWrite(TRIG_PORT, TRIG_PIN, 0);

    // Esperar a que el Echo se ponga en alto (indicando que ha recibido el pulso)
    while (GPIOPinRead(ECHO_PORT, ECHO_PIN) == 0);
    startTime = TimerValueGet(TIMER1_BASE, TIMER_A);  // Captura el inicio del eco

    // Esperar a que el Echo vuelva a 0 (fin del eco)
    while (GPIOPinRead(ECHO_PORT, ECHO_PIN) != 0);
    endTime = TimerValueGet(TIMER1_BASE, TIMER_A);  // Captura el final del eco

    // Calcular la duración del eco en ticks del temporizador
    duration = startTime - endTime;  // La diferencia de tiempo en ticks

    // Convertir la duración a tiempo en microsegundos
    // La frecuencia del temporizador es de 120 MHz, por lo que cada tick equivale a (1/120000000) segundos, o 8.33 nanosegundos
    // Para obtener microsegundos, multiplicamos los ticks por 0.00833
    float time_us = (float)duration * 0.00833f;

    // Convertir el tiempo a distancia en cm (dividimos por 58 para obtener cm directamente)
    distance = time_us / 58.0f;
}

//configuracion sensor ultrasonico
static void config_ultrasonico(void){
            // Habilitar el puerto A para los pines del sensor
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOA));

    // Configurar PA2 como salida para el pin Trig y PA3 como entrada para Echo
    GPIOPinTypeGPIOOutput(TRIG_PORT, TRIG_PIN);
    GPIOPinTypeGPIOInput(ECHO_PORT, ECHO_PIN);

    // Asegurarse de que el Trig esté en LOW al inicio
    GPIOPinWrite(TRIG_PORT, TRIG_PIN, 0);
}
static void config_timer6(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER6);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    TimerConfigure(TIMER6_BASE, TIMER_CFG_PERIODIC);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER6_BASE, TIMER_A, (ui32SysClock - 1)*1);  // 120 millones de ciclos = 1 segundo

    // Habilitar la interrupción del temporizador en el procesador
    IntEnable(INT_TIMER6A);
    TimerIntEnable(TIMER6_BASE, TIMER_TIMA_TIMEOUT);  // Habilitar la interrupción por timeout

    // Habilitar las interrupciones globales
    IntMasterEnable();

    // Iniciar el temporizador
    TimerEnable(TIMER6_BASE, TIMER_A);
}
static void config_timer5(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER5);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    TimerConfigure(TIMER5_BASE, TIMER_CFG_PERIODIC);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER5_BASE, TIMER_A, (ui32SysClock - 1)*0.1);  // 120 millones de ciclos = 1 segundo

    // Habilitar la interrupción del temporizador en el procesador
    IntEnable(INT_TIMER5A);
    TimerIntEnable(TIMER5_BASE, TIMER_TIMA_TIMEOUT);  // Habilitar la interrupción por timeout

    // Habilitar las interrupciones globales
    IntMasterEnable();

    // Iniciar el temporizador
    TimerEnable(TIMER5_BASE, TIMER_A);
}
static void config_timer4(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER4);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    TimerConfigure(TIMER4_BASE, TIMER_CFG_PERIODIC);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER4_BASE, TIMER_A, (ui32SysClock - 1)*2);  // 120 millones de ciclos = 1 segundo

    // Habilitar la interrupción del temporizador en el procesador
    IntEnable(INT_TIMER4A);
    TimerIntEnable(TIMER4_BASE, TIMER_TIMA_TIMEOUT);  // Habilitar la interrupción por timeout

    // Habilitar las interrupciones globales
    IntMasterEnable();

    // Iniciar el temporizador
    TimerEnable(TIMER4_BASE, TIMER_A);
}
static void config_timer3(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER3);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    TimerConfigure(TIMER3_BASE, TIMER_CFG_PERIODIC);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER3_BASE, TIMER_A, (ui32SysClock - 1)*0.05);  // 120 millones de ciclos = 1 segundo

    // Habilitar la interrupción del temporizador en el procesador
    IntEnable(INT_TIMER3A);
    TimerIntEnable(TIMER3_BASE, TIMER_TIMA_TIMEOUT);  // Habilitar la interrupción por timeout

    // Habilitar las interrupciones globales
    IntMasterEnable();

    // Iniciar el temporizador
    TimerEnable(TIMER3_BASE, TIMER_A);
}
static void config_timer2(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER2);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    TimerConfigure(TIMER2_BASE, TIMER_CFG_PERIODIC);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER2_BASE, TIMER_A, (ui32SysClock - 1)*1);  // 120 millones de ciclos = 1 segundo

    // Habilitar la interrupción del temporizador en el procesador
    IntEnable(INT_TIMER2A);
    TimerIntEnable(TIMER2_BASE, TIMER_TIMA_TIMEOUT);  // Habilitar la interrupción por timeout

    // Habilitar las interrupciones globales
    IntMasterEnable();

    // Iniciar el temporizador
    TimerEnable(TIMER2_BASE, TIMER_A);
}
static void config_timer1(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    //TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    TimerConfigure(TIMER1_BASE, TIMER_CFG_A_PERIODIC | TIMER_CFG_B_ONE_SHOT);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER1_BASE, TIMER_A, ui32SysClock - 1);  // 120 millones de ciclos = 1 segundo

    // Habilitar la interrupción del temporizador en el procesador
    IntEnable(INT_TIMER1A);
    TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);  // Habilitar la interrupción por timeout
    // Habilitar las interrupciones globales
    IntMasterEnable();
    // Iniciar el temporizador
    TimerEnable(TIMER1_BASE, TIMER_A);
}
// Configurar el Timer0 para generar una interrupción periódica
static void config_timer(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER0_BASE, TIMER_A, (ui32SysClock - 1)*0.1);  // 120 millones de ciclos = 0.1 segundo

    // Habilitar la interrupción del temporizador en el procesador
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);  // Habilitar la interrupción por timeout

    // Habilitar las interrupciones globales
    IntMasterEnable();

    // Iniciar el temporizador
    TimerEnable(TIMER0_BASE, TIMER_A);
}
// Configurar UART0
static void configureUART0(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);  // Habilitar el reloj para el puerto GPIO A
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);  // Habilitar el reloj para UART0
    
    // Configurar los pines PA0 (RX) y PA1 (TX) para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    // Configurar UART0: 115200 baudios, 8 bits de datos, sin paridad, 1 bit de parada
    UARTConfigSetExpClk(UART0_BASE, ui32SysClock, 115200,
                        (UART_CONFIG_WLEN_8 |
                         UART_CONFIG_STOP_ONE |
                         UART_CONFIG_PAR_NONE));

    // Habilitar interrupciones de recepción en UART
    IntEnable(INT_UART0);                          // Habilitar la interrupción en el procesador
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);  // Habilitar interrupciones RX y de timeout
    IntMasterEnable();                             // Habilitar interrupciones globales

    // Inicializar la UART estándar para printf
    UARTStdioConfig(0, 115200, ui32SysClock);
}
// Inicializar PWM
static void config_pwm(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF); // Habilitar el reloj para GPIO F
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);   // Habilitar el reloj para el módulo PWM0

    // Configurar PF1 como salida de PWM
    GPIOPinConfigure(GPIO_PF1_M0PWM1); 
    GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_1); // Configurar PF1 como PWM

    // Configurar el generador PWM0
    PWMGenConfigure(PWM0_BASE, PWM_GEN_0, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_0, duty); // Establecer el período del PWM (frecuencia de 250 Hz)

    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, 1); // Establecer el ciclo de trabajo inicial
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0))
    {

    }
    PWMGenEnable(PWM0_BASE, PWM_GEN_0); // Habilitar el generador PWM
    PWMOutputState(PWM0_BASE, PWM_OUT_1_BIT, true); // Habilitar la salida PWM
}

// Configurar GPIO para un LED
static void config_gpio(void){
    //todo los perifericos que tienen gpio
    //habilitacion de perifericos
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB); 
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOG);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOH);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOM);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOP);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOQ);
    //MOTORES
    GPIOPinTypeGPIOOutput(PUERTOMOTRORES, MOTOR1DER);
    GPIOPinTypeGPIOOutput(PUERTOMOTRORES, MOTOR1IZQ);
    GPIOPinTypeGPIOOutput(PUERTOMOTRORES, MOTOR2DER);
    GPIOPinTypeGPIOOutput(PUERTOMOTRORES, MOTOR2IZQ);
    //BUZZER
    GPIOPinTypeGPIOOutput(PUERTOBUZZER, BUZZER);
    //LEDS EXTERNOS
    GPIOPinTypeGPIOOutput(PUERTOLEDS, LED1);
    GPIOPinTypeGPIOOutput(PUERTOLEDS, LED2);
    GPIOPinTypeGPIOOutput(PUERTOLEDS, LED3);
    GPIOPinTypeGPIOOutput(PUERTOLEDS, LED4);
    //LEDS INTERNOS
    GPIOPinTypeGPIOOutput(PUERTOLEDSIN1, LED1I);
    GPIOPinTypeGPIOOutput(PUERTOLEDSIN1, LED2I);
    GPIOPinTypeGPIOOutput(PUERTOLEDSIN2, LED3I);
    GPIOPinTypeGPIOOutput(PUERTOLEDSIN2, LED4I); 
}
//
static void configureSysClock(void) {
    // Configurar el sistema a 120 MHz usando PLL
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_240), 120000000);
}
