#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/debug.h"
#include "driverlib/fpu.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"

//****************************************************************************
//
// Frecuencia del reloj del sistema en Hz.
//
//****************************************************************************
uint32_t g_ui32SysClock;

//****************************************************************************
//
// Contador que indica cuántos LEDs están encendidos.
//
//****************************************************************************
uint32_t g_ui32LedIndex = 0;

//****************************************************************************
//
// Estado del temporizador (0 = 0.5 segundos, 1 = 1 segundo)
//
//****************************************************************************
uint32_t g_ui32TimerState = 0;

//****************************************************************************
//
// Variable para almacenar el estado anterior del botón.
//
//****************************************************************************
bool g_bLastButtonState = false;

//*****************************************************************************
//
// Rutina de error que se llama si la biblioteca del controlador encuentra un error.
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
}
#endif

//*****************************************************************************
//
// Manejador de la interrupción del temporizador 0.
//
//*****************************************************************************
void
Timer0IntHandler(void)
{
    // Limpia la interrupción del temporizador 0.
    MAP_TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Si g_ui32LedIndex llega a 4, apaga todos los LEDs y reinicia el ciclo.
    if (g_ui32LedIndex >=16)
    {
        // Apaga todos los LEDs.
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);

        // Reinicia el índice.
        g_ui32LedIndex = 0;
    }
    else
    {
        // Acumula los LEDs encendidos:
        // Encendemos el LED correspondiente sin apagar los anteriores.

        if (g_ui32LedIndex == 1){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
        }
        else if (g_ui32LedIndex == 2){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
        }
        else if (g_ui32LedIndex == 3){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
        }
        else if (g_ui32LedIndex == 4){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
        }
        else if (g_ui32LedIndex == 5){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
        }
        else if (g_ui32LedIndex == 6){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
        }
        else if (g_ui32LedIndex == 7){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
        }
        else if (g_ui32LedIndex == 8){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        }
        else if (g_ui32LedIndex == 9){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        }
        else if (g_ui32LedIndex == 10){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        }
        else if (g_ui32LedIndex == 11){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        }
        else if (g_ui32LedIndex == 12){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        }
        else if (g_ui32LedIndex == 13){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        }
        else if (g_ui32LedIndex == 14){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        }
        else if (g_ui32LedIndex == 15){
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        }
        // Incrementa el índice del LED.
        g_ui32LedIndex++;
    }
}

//*****************************************************************************
//
// Esta aplicación de ejemplo demuestra el uso de un temporizador para alternar
// los 4 LEDs en los puertos N y F de forma acumulativa.
//
//*****************************************************************************
int
main(void)
{
    // Configura el sistema para que corra a 120 MHz usando el PLL.
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    // Habilita los puertos GPIO que se usan para los LEDs y el botón.
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);  // Habilita el puerto GPIO para el botón (PJ0).

    // Habilita los pines GPIO para los LEDs (PN0, PN1 y PF4, PF0).
    MAP_GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    MAP_GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0);

    // Configura el pin PJ0 como entrada para el botón.
    MAP_GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    MAP_GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);  // Configura resistencia pull-up.

    // Habilita el periférico utilizado por el temporizador.
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    // Habilita las interrupciones del procesador.
    MAP_IntMasterEnable();

    // Configura el temporizador 0 en modo periódico.
    MAP_TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*1.5);  // Temporizador a 0.5 segundos inicialmente.

    // Configura la interrupción para el timeout del temporizador 0.
    MAP_IntEnable(INT_TIMER0A);
    MAP_TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Habilita el temporizador.
    MAP_TimerEnable(TIMER0_BASE, TIMER_A);

    // Bucle infinito mientras el temporizador corre.
    while(1)
    {
        // Lee el estado actual del botón.
        bool bButtonState = MAP_GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0;

        // Si el botón está presionado y no estaba presionado en la iteración anterior.
        if (bButtonState && !g_bLastButtonState)
        {
            // Alterna entre los dos tiempos del temporizador.
            g_ui32TimerState = !g_ui32TimerState;

            // Cambia el periodo del temporizador según el estado.
            if (g_ui32TimerState == 0)
            {
                // Ajusta el temporizador a 0.1 segundos.
                MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*1.5);
            }
            else
            {
                // Ajusta el temporizador a 1 segundo.
                MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*3);
            }
        }

        // Guarda el estado del botón para la próxima iteración.
        g_bLastButtonState = bButtonState;
    }
}
