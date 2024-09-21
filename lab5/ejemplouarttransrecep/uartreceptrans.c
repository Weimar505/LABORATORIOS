#include <stdint.h>
#include <stdbool.h>
#include <string.h>  // Incluye la biblioteca para memset
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/uart.h"
#include "driverlib/interrupt.h"
#include "utils/uartstdio.c"  // Incluye el archivo de cabecera correcto
#include "inc/hw_ints.h"

#define BUFFER_SIZE 100

uint32_t ui32SysClock;
int counter = 0;
char data[BUFFER_SIZE];  // Buffer para almacenar la frase completa
bool newDataAvailable = false;  // Bandera para indicar que hay datos nuevos

// Configurar el reloj del sistema
void configureSysClock(void)
{
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_240), 120000000);
}

// Configurar UART0 usando UARTStdio
void configureUART0(void)
{
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);  // Habilita el puerto A para UART0
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);  // Habilita UART0
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);  // Habilita el puerto para el botón

    // Configurar los pines PA0 (RX) y PA1 (TX) para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    // Configurar UART0 a 115200 baudios
    UARTStdioConfig(0, 115200, ui32SysClock);
   
    // Configurar el pin PN1 como salida para un LED
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_2);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);

    // Configurar el pin PJ0 como entrada para el botón con resistencia pull-up
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);  // Botón en pin PJ0
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    // Habilitar interrupciones UART
    UARTIntClear(UART0_BASE, UART_INT_RX | UART_INT_RT);
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);
    IntEnable(INT_UART0);
}

// Manejador de interrupciones de UART0
void UART0IntHandler(void)
{
    uint32_t ui32Status;
    static uint32_t dataIndex = 0;  // Índice actual en el buffer de datos

    // Obtener el estado de las interrupciones
    ui32Status = UARTIntStatus(UART0_BASE, true);
    UARTIntClear(UART0_BASE, ui32Status);

    // Verificar si la interrupción es de recepción de datos
    if (ui32Status & (UART_INT_RX | UART_INT_RT))
    {
        // Leer todos los datos disponibles
        while (UARTCharsAvail(UART0_BASE) && dataIndex < BUFFER_SIZE - 1)
        {
            char received = UARTCharGet(UART0_BASE);
            
            // Almacenar el carácter en el buffer
            if (received == '\n' || received == '\r')
            {
                // Terminación de la cadena
                data[dataIndex] = '\0';
                newDataAvailable = true;  // Señalar que hay datos nuevos disponibles
                dataIndex = 0;  // Reiniciar el índice
                break;  // Salir del bucle de lectura
            }
            else
            {
                data[dataIndex++] = received;
            }
        }
        if (dataIndex >= BUFFER_SIZE - 1)
        {
            // Si el buffer está lleno, reiniciar el índice
            dataIndex = 0;
        }

        //UARTprintf("Datos recibidos: %s\r\n", data);  // Enviar mensaje con los datos recibidos
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1); // Indicar recepción de dato
        SysCtlDelay(1000000);
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x00);
        // Procesar la frase recibida si está disponible

        if (strcmp(data, "buzzer") == 0)
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_2, GPIO_PIN_2); 
            SysCtlDelay(120000000*2);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_2, 0x00);
        } 
        else 
        {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_2, 0x00);
        }
    }
}

int main(void)
{
    configureSysClock();  // Configura el sistema a 120 MHz
    configureUART0();     // Configura UART0
    IntMasterEnable();    // Habilita las interrupciones globales

    // Inicializar el buffer de datos
    memset(data, 0, sizeof(data));

    while (1)
    {
        // Leer el estado del botón (en PJ0)
        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)  // Botón presionado (activo bajo)
        {
            counter++;
            // Espera hasta que el botón sea liberado
            while (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)
            {
                // Espera activa para detectar la liberación del botón
            }
            // Esperar un pequeño tiempo para evitar rebotes del botón y encender un LED indicador
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            SysCtlDelay(1000000);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x00);

            // Reiniciar el contador si llega a 3
            if (counter >= 3)
            {
                counter = 0;
            }

            // Dependiendo del valor de counter, mostrar diferentes mensajes
            if (counter == 1)
            {
                UARTprintf("motor %d\n", counter);
            }
            else if (counter == 2)
            {
                UARTprintf("motor %d\n", counter);
            }
            else if (counter == 0)
            {
                UARTprintf("apagado\n");  // Motor apagado cuando counter es 0
            }
            if (newDataAvailable)
            {
            // Mostrar los datos recibidos
            UARTprintf("\n",data);//"mensaje recibido %s\r\n", 
            newDataAvailable = false;  // Limpiar la bandera
            memset(data, 0, sizeof(data));  // Limpiar el buffer de datos
            }
        }

    }
}
