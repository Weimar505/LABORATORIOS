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
    if (g_ui32LedIndex >= 4)
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
        if (g_ui32LedIndex == 0)
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  // Enciende LED 1 (PN1)
        else if (g_ui32LedIndex == 1)
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);  // Enciende LED 2 (PN0)
        else if (g_ui32LedIndex == 2)
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);  // Enciende LED 3 (PF4)
        else if (g_ui32LedIndex == 3)
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);  // Enciende LED 4 (PF0)

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

    // Habilita los puertos GPIO que se usan para los LEDs.
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    // Habilita los pines GPIO para los LEDs (PN0, PN1 y PF4, PF0).
    MAP_GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    MAP_GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0);

    // Habilita el periférico utilizado por el temporizador.
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    // Habilita las interrupciones del procesador.
    MAP_IntMasterEnable();

    // Configura el temporizador 0 en modo periódico.
    MAP_TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock *2);  // Ajusta el periodo para alternar cada 0.5 segundos

    // Configura la interrupción para el timeout del temporizador 0.
    MAP_IntEnable(INT_TIMER0A);
    MAP_TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Habilita el temporizador.
    MAP_TimerEnable(TIMER0_BASE, TIMER_A);

    // Bucle infinito mientras el temporizador corre.
    while(1)
    {
    }
}
