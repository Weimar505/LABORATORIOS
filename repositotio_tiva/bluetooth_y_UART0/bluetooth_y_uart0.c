#include <stdint.h>              // Tipos de datos enteros de tamaño fijo (uint32_t, int16_t, etc.)
#include <stdbool.h>             // Tipo booleano (bool) con valores true y false
#include "inc/hw_memmap.h"       // Mapa de memoria del hardware, define las direcciones base de los periféricos (GPIO, UART, etc.)
#include "driverlib/sysctl.h"    // Funciones de control del sistema (configuración de reloj, habilitación de periféricos)
#include "driverlib/gpio.h"      // Control de los pines GPIO (configuración de entrada/salida, lectura y escritura de pines)
#include "driverlib/pin_map.h"   // Asignación de funciones a los pines (mapeo de pines para UART, PWM, etc.)
#include "driverlib/interrupt.h" // Manejo de interrupciones (habilitar/deshabilitar interrupciones, configurar manejadores)
#include "inc/hw_ints.h"         // Definición de las interrupciones del hardware (vectores de interrupción)
#include "driverlib/uart.h"      // Control del módulo UART (envío y recepción de datos seriales)
#include "utils/uartstdio.h"     //par usar uart printf
#include <string.h>              // Para usar strcmp()
#define BAUDIOS 9600            // Velocidad de transferencia para los UART
#define MAX_BUFFER_SIZE 100  // Tamaño máximo del buffer para almacenar la frase

// Definir pines para los leds internos
#define LED1I GPIO_PIN_1
#define LED2I GPIO_PIN_0
#define LED3I GPIO_PIN_4
#define LED4I GPIO_PIN_0
#define PUERTOLEDSIN1 GPIO_PORTN_BASE
#define PUERTOLEDSIN2 GPIO_PORTF_BASE

char uartBuffer[MAX_BUFFER_SIZE]; // Buffer para almacenar la frase recibida
volatile uint8_t bufferIndex = 0; // Índice del buffer
uint32_t ui32SysClock;  // Variable para almacenar la frecuencia del reloj del sistema

// Prototipos de funciones
static void configureSysClock(void);
static void configureUART3(void);
static void configureUART0(void);  // Nueva función para configurar UART0
static void config_gpio(void);
static void uartprintf(const char *str);// esto se utiliza cuando se quiere enviar a dos uarts a la vez 

// Función principal
int main(void) {
    configureSysClock();  // Configurar el sistema a 120 MHz
    configureUART3();     // Configuración del UART3
    configureUART0();     // Configuración del UART0
    config_gpio();        // Configuración de los GPIOs

    // Bucle principal
    while (1) {
        //UARTprintf("hola desde UART3\n");  // Enviar mensaje a través del UART3
        //UARTprintf("hola desde UART0\n");  // Enviar mensaje a través del UART0
        uartprintf("holaa desde la tiva\r\n");//Para enviar en diferentes uart menos en el 0
        UARTprintf("holaa desde la tiva\r\n");//para enviar en el uart0
        SysCtlDelay(ui32SysClock*0.2);  // Retraso
    }
}

// Manejador de la interrupción de UART3 (cuando se recibe un dato)
void UART3IntHandler(void) {
    uint32_t ui32Status;
    char receivedChar;

    // Obtener y limpiar el estado de la interrupción
    ui32Status = UARTIntStatus(UART3_BASE, true);
    UARTIntClear(UART3_BASE, ui32Status);

    // Procesar los datos mientras haya en el FIFO
    while (UARTCharsAvail(UART3_BASE)) {
        // Leer el carácter recibido
        receivedChar = UARTCharGetNonBlocking(UART3_BASE);

        // Si es un retorno de carro o salto de línea, la frase está completa
        if (receivedChar == '\r' || receivedChar == '\n') {
            uartBuffer[bufferIndex] = '\0';  // Terminar la cadena con el carácter nulo
            //para imprimir en el UART3
            uartprintf("Datos recibidos UART3: ");
            uartprintf(uartBuffer);  // Enviar la frase recibida a través del UART3
            uartprintf("\r\n");
            //para imprimir en el UART0
            UARTprintf("Datos recibidos UART3: ");
            UARTprintf(uartBuffer);  // Enviar la frase recibida a través del UART3
            UARTprintf("\r\n");
            //------------
            bufferIndex = 0;  // Reiniciar el buffer para la siguiente frase
        }
        else {
            if (bufferIndex < MAX_BUFFER_SIZE - 1) {
                uartBuffer[bufferIndex++] = receivedChar;  // Agregar el carácter al buffer
            }
            else {
                uartprintf("Buffer lleno, frase demasiado larga.\r\n");
                bufferIndex = 0;  // Reiniciar el buffer
            }
        }
    }
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
            uartBuffer[bufferIndex] = '\0';  // Terminar la cadena con el carácter nulo
            //para imprimir en el UART0
            UARTprintf("Datos recibidos UART0: ");
            UARTprintf(uartBuffer);  // Enviar la frase recibida a través del UART0
            UARTprintf("\r\n");
            //para imprimir en el UART3
            uartprintf("Datos recibidos UART0: ");
            uartprintf(uartBuffer);  // Enviar la frase recibida a través del UART3
            uartprintf("\r\n");
            //--------------------------
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

// Configurar UART3
static void configureUART3(void) {
    // Habilitar los periféricos necesarios
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);  // Habilitar el reloj para el puerto GPIO A
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART3);  // Habilitar el reloj para UART3
    
    // Configurar los pines PA4 (RX) y PA5 (TX) para UART3
    GPIOPinConfigure(GPIO_PA4_U3RX);  // Configura PA4 como RX de UART3
    GPIOPinConfigure(GPIO_PA5_U3TX);  // Configura PA5 como TX de UART3
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_4 | GPIO_PIN_5);  // Configura los pines como UART

    // Configurar UART3: 9600 baudios, 8 bits de datos, sin paridad, 1 bit de parada
    UARTConfigSetExpClk(UART3_BASE, ui32SysClock, BAUDIOS,
                        (UART_CONFIG_WLEN_8 |
                         UART_CONFIG_STOP_ONE |
                         UART_CONFIG_PAR_NONE));

    // Habilitar interrupciones de recepción en UART3
    IntEnable(INT_UART3);  // Habilitar la interrupción en el procesador
    UARTIntEnable(UART3_BASE, UART_INT_RX | UART_INT_RT);  // Habilitar interrupciones RX y de timeout
    UARTStdioConfig(3, BAUDIOS, ui32SysClock);  // Configuración de UART3 para printf
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
}

// Función para enviar una cadena por UART
static void uartprintf(const char *str) {//esta funcion es para imprimir en el uart pero en diferentes uarts que no sea el UART0
    while (*str) {
        UARTCharPut(UART3_BASE, *str++);  // Enviar cada carácter de la cadena a través de UART3
    }
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
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOP);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOQ);
}
// Configurar el reloj del sistema a 120 MHz
static void configureSysClock(void) {
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_480), 120000000);  // Configuración a 120 MHz
}