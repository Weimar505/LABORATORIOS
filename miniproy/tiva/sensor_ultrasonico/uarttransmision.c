#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/uart.h"
#include "driverlib/pin_map.h"
#include "utils/uartstdio.c"
#include "driverlib/timer.h"     // Funciones para controlar los temporizadores (configuración, inicio, interrupciones)
#include "driverlib/interrupt.h" // Manejo de interrupciones (habilitar/deshabilitar interrupciones, configurar manejadores)
#include "inc/hw_ints.h"         // Definición de las interrupciones del hardware (vectores de interrupción)
#define MAX_BUFFER_SIZE 100  // Tamaño máximo del buffer para almacenar la frase

// Definir pines para Trig y Echo
#define TRIG_PIN GPIO_PIN_4
#define ECHO_PIN GPIO_PIN_5
#define TRIG_PORT GPIO_PORTA_BASE
#define ECHO_PORT GPIO_PORTA_BASE
uint32_t distance;
uint32_t startTime, endTime, duration;

uint32_t ui32SysClock;           // Variable para almacenar la frecuencia del reloj del sistema
char uartBuffer[MAX_BUFFER_SIZE]; // Buffer para almacenar la frase recibida
volatile uint8_t bufferIndex = 0; // Índice del buffer

static void configureSysClock(void);  // Configurar el sistema a 120 MHz
static void configureUART0(void);     // Configurar UART0
static void config_timer(void);
static void config_timer1(void);
static void config_ultrasonico(void);

void medir_distancia(void);
int main(void) {
    configureSysClock();  // Configurar el sistema a 120 MHz
    configureUART0();     // Configurar UART0
    config_timer();
    config_timer1();
    config_ultrasonico();
    ///------------------------------------------------
    // Bucle principal
    while (1) {
        medir_distancia();
    }
}
void Timer1IntHandler(void) {
    // Limpiar la interrupción del temporizador para poder seguir generando interrupciones
    TimerIntClear(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
}
// Función de manejo de la interrupción del temporizador
void Timer0IntHandler(void) {
    // Limpiar la interrupción del temporizador para poder seguir generando interrupciones
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
}
// Manejador de la interrupción de UART0 (cuando se recibe un dato)
void UART0IntHandler(void) {
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
            UARTprintf("Datos recibidos %s\r\n", uartBuffer);  // Imprimir la frase recibida

            // Reiniciar el buffer para la siguiente frase
            bufferIndex = 0;
        }
        else {
            // Agregar el carácter al buffer si no se ha alcanzado el tamaño máximo
            if (bufferIndex < MAX_BUFFER_SIZE - 1) {
                uartBuffer[bufferIndex++] = receivedChar;
            }
            else {
                // Si el buffer está lleno, reiniciar (puedes manejar esto de otra manera)
                UARTprintf("Buffer lleno, frase demasiado larga.\r\n");
                bufferIndex = 0;
            }
        }
    }
}
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

    // Imprimir la distancia
    UARTprintf("Distancia: %d cm\r\n", (int)distance);

    // Pequeña espera antes de la siguiente lectura
    SysCtlDelay(120000000 * 0.1);

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
static void configureSysClock(void) {
    // Configurar el sistema a 120 MHz usando PLL
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_240), 120000000);
}
// Configurar el Timer0 para generar una interrupción periódica
static void config_timer(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    //TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    TimerConfigure(TIMER0_BASE, TIMER_CFG_A_PERIODIC | TIMER_CFG_B_ONE_SHOT);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER0_BASE, TIMER_A, ui32SysClock - 1);  // 120 millones de ciclos = 1 segundo

    // Habilitar la interrupción del temporizador en el procesador
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);  // Habilitar la interrupción por timeout
    // Habilitar las interrupciones globales
    IntMasterEnable();
    // Iniciar el temporizador
    TimerEnable(TIMER0_BASE, TIMER_A);
}
//
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
