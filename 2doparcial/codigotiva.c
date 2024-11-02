#include <stdint.h>              // Tipos de datos enteros de tamaño fijo (uint32_t, int16_t, etc.)
#include <stdbool.h>             // Tipo booleano (bool) con valores true y false
#include "inc/hw_memmap.h"       // Mapa de memoria del hardware, define las direcciones base de los periféricos (GPIO, UART, etc.)
#include "driverlib/sysctl.h"    // Funciones de control del sistema (configuración de reloj, habilitación de periféricos)
#include "driverlib/gpio.h"      // Control de los pines GPIO (configuración de entrada/salida, lectura y escritura de pines)
#include "driverlib/pin_map.h"   // Asignación de funciones a los pines (mapeo de pines para UART, PWM, etc.)
#include "driverlib/interrupt.h" // Manejo de interrupciones (habilitar/deshabilitar interrupciones, configurar manejadores)
#include "driverlib/timer.h"     // Funciones para controlar los temporizadores (configuración, inicio, interrupciones)
#include "inc/hw_ints.h"         // Definición de las interrupciones del hardware (vectores de interrupción)
#include "driverlib/uart.h"      // Control del módulo UART (envío y recepción de datos seriales)
#include "utils/uartstdio.h"     //par usar uart printf
#include <string.h>              // Para usar strcmp()
#define BAUDIOS 9600            //Velocidad de transferencia para el UART
#define MAX_BUFFER_SIZE 100  // Tamaño máximo del buffer para almacenar la frase

// Definir pines para los leds internos
#define LED1I GPIO_PIN_1
#define LED2I GPIO_PIN_0
#define LED3I GPIO_PIN_4
#define LED4I GPIO_PIN_0
#define PUERTOLEDSIN1 GPIO_PORTN_BASE
#define PUERTOLEDSIN2 GPIO_PORTF_BASE
#define LED1 GPIO_PIN_1
#define LED2 GPIO_PIN_2
#define LED3 GPIO_PIN_3
#define PUERTOLEDS GPIO_PORTE_BASE
char uartBuffer[MAX_BUFFER_SIZE]; // Buffer para almacenar la frase recibida
volatile uint8_t bufferIndex = 0; // Índice del buffer
uint32_t ui32SysClock;  // Variable para almacenar la frecuencia del reloj del sistema
uint32_t contador = 0;
// Prototipos de funciones
static void configureSysClock(void);
static void configureUART0(void);
static void config_gpio(void);
static void config_timer0(void);
// Función principal
int main(void) {
    configureSysClock();  // Configurar el sistema a 120 MHz
    config_timer0();       // configuracion del temporizador con interrupción
    configureUART0();      // Configuración del UART0
    config_gpio();        // Configuración de los GPIOs

    // Bucle principal
    while (1) {
        
    }
}
// Función de manejo de la interrupción del temporizador
void Timer0IntHandler(void) {
    // Limpiar la interrupción del temporizador para poder seguir generando interrupciones
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    contador++;
    
    // Ciclo de LEDs en 3 estados: rojo, amarillo y verde
    if(contador == 1){
        GPIOPinWrite(PUERTOLEDSIN1, LED1I, LED1I);  
        GPIOPinWrite(PUERTOLEDSIN1, LED2I, 0x00);
        GPIOPinWrite(PUERTOLEDSIN2, LED3I, 0x00);

        GPIOPinWrite(PUERTOLEDS, LED1, LED1);
        GPIOPinWrite(PUERTOLEDS, LED2, 0x00);
        GPIOPinWrite(PUERTOLEDS, LED3, 0x00);
        UARTprintf("rojo\n");
    }
    else if(contador == 2){
        GPIOPinWrite(PUERTOLEDSIN1, LED1I, 0x00);  
        GPIOPinWrite(PUERTOLEDSIN1, LED2I, LED2I);
        GPIOPinWrite(PUERTOLEDSIN2, LED3I, 0x00);

        GPIOPinWrite(PUERTOLEDS, LED1, 0x00);
        GPIOPinWrite(PUERTOLEDS, LED2, LED2);
        GPIOPinWrite(PUERTOLEDS, LED3, 0x00);
        UARTprintf("amarillo\n");
    }
    else if(contador == 3){
        GPIOPinWrite(PUERTOLEDSIN1, LED1I, 0x00);  
        GPIOPinWrite(PUERTOLEDSIN1, LED2I, 0x00);
        GPIOPinWrite(PUERTOLEDSIN2, LED3I, LED3I);

        GPIOPinWrite(PUERTOLEDS, LED1, 0x00);
        GPIOPinWrite(PUERTOLEDS, LED2, 0x00);
        GPIOPinWrite(PUERTOLEDS, LED3, LED3);
        UARTprintf("verde\n");
    }    

    // Reiniciar contador cuando alcance 3
    if (contador >= 3) {
        contador = 0;
    }
}

// Manejador de la interrupción de UART3 (cuando se recibe un dato)
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
            uartBuffer[bufferIndex] = '\0';  // Terminar la cadena con el carácter nulo
            //para imprimir en el UART0
            UARTprintf("Datos recibidos UART0: ");
            UARTprintf(uartBuffer);  // Enviar la frase recibida a través del UART0
            UARTprintf("\r\n");
            bufferIndex = 0;  // Reiniciar el buffer para la siguiente frase
        }
        else {
            if (bufferIndex < MAX_BUFFER_SIZE - 1) {
                uartBuffer[bufferIndex++] = receivedChar;  // Agregar el carácter al buffer
            }
            else {
                UARTprintf("Buffer lleno, frase demasiado larga.\r\n");
                bufferIndex = 0;  // Reiniciar el buffer
            }
        }
    }
}
// Configurar el Timer0 para generar una interrupción periódica
static void config_timer0(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

    // Establecer el valor del temporizador para que genere una interrupción cada 1 segundo
    TimerLoadSet(TIMER0_BASE, TIMER_A, (ui32SysClock - 1)*2);  // 120 millones de ciclos = 1 segundo

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
    // Habilitar los periféricos necesarios
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);  // Habilitar el reloj para el puerto GPIO A
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);  // Habilitar el reloj para UART0
    
    // Configurar los pines PA0 (RX) y PA1 (TX) para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX);  // Configura PA0 como RX de UART0
    GPIOPinConfigure(GPIO_PA1_U0TX);  // Configura PA1 como TX de UART0
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);  // Configura los pines como UART

    // Configurar UART0: 9600 baudios, 8 bits de datos, sin paridad, 1 bit de parada
    UARTConfigSetExpClk(UART0_BASE, ui32SysClock, BAUDIOS,
                        (UART_CONFIG_WLEN_8 |
                         UART_CONFIG_STOP_ONE |
                         UART_CONFIG_PAR_NONE));

    // Habilitar interrupciones de recepción en UART0
    IntEnable(INT_UART0);  // Habilitar la interrupción en el procesador
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);  // Habilitar interrupciones RX y de timeout
    IntMasterEnable();     // Habilitar interrupciones globales
        // Inicializar la UART estándar para printf
    UARTStdioConfig(0, BAUDIOS, ui32SysClock);  // Configuración de UART0 para printf
}

// Configurar GPIO para los LEDs internos
static void config_gpio(void) {
    // Habilitar los periféricos de los puertos GPIO
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

    // Configuración de los LEDs internos
    GPIOPinTypeGPIOOutput(PUERTOLEDS, LED1);
    GPIOPinTypeGPIOOutput(PUERTOLEDS, LED2);
    GPIOPinTypeGPIOOutput(PUERTOLEDS, LED3);

    GPIOPinTypeGPIOOutput(PUERTOLEDSIN1, LED1I);
    GPIOPinTypeGPIOOutput(PUERTOLEDSIN1, LED2I);
    GPIOPinTypeGPIOOutput(PUERTOLEDSIN2, LED3I);
    GPIOPinTypeGPIOOutput(PUERTOLEDSIN2, LED4I);
}

// Configurar el reloj del sistema a 120 MHz
static void configureSysClock(void) {
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_480), 120000000);  // Configuración a 120 MHz
}