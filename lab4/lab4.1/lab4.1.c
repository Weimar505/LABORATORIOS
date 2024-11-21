//*****************************************************************************
// LIBRERIAS QUE PROPORCIOANA DEFINICIONES Y FUNCIONES NECESARIAS PARA CONTROLAR EL HADWARE
// DE LA PLACA, COMO LA CONFIGURACION DE PINES GPIO (ENTRADA/SALIDA), EL TEMPORIZADOR Y EL 
// DE RELOJ.
//*****************************************************************************

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
// VARIABLES GLOBALES
//****************************************************************************
// ALMACENA LA VELOCIDAD DEL RELOJ DEL SISTEMA (FRECUENCIA DEL MICROCONTROLADOR)
uint32_t g_ui32SysClock; 
// SE UTILIZA COMO UN INDICADOR PARA EL MANEJO DE INTERRUPCIONES (EN ESTE CASO, PARA LTERNAR EL ESATDO DE UN LED)
uint32_t g_ui32Flags;


//*****************************************************************************
// MANEJO DE ERRORES
//*****************************************************************************
//ESTA ES UNA RUTINA VACIA QUE SE LLAMA SI OSURRE UN ERROR EN LA LIBRERIA DEL MICROCONTROLADOR SOLO ESTA PRESENTE EN EL MODO DEPURACION
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
}
#endif

//*****************************************************************************
//HANDLER DE INTERRUPCION DEL TEMPORIZADOR 
//*****************************************************************************
void
Timer0IntHandler(void)
{
    // BORRA (LIMPIA) LA INTERRUPCION DEL TEMPORIZADOR PARA EVITAR QUE SE REPITA SIN CONTROL
    MAP_TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // ALTERNA EL PRIMER BIT DE g_ui32Flags. ESTO CAMBIA ENTRE 1 Y0 CADA VEZ QUE SE EJECUTA LA INTERRUPCION
    HWREGBITW(&g_ui32Flags, 0) ^= 1;

    // UTILIZA EL VALOR DEL FLAG PARA ENCENDER O APAGAR EL LED EN EL PIN GPIO
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, HWREGBITW(&g_ui32Flags, 0) ? GPIO_PIN_0 : 0);
}

//*****************************************************************************
//EL CODIGO EN LA FUNCION MAIN CONFIGURA Y HABILITA EL TEMPORIZADOR Y EL LED
//*****************************************************************************
int
main(void)
{
    // AQUI SE CONFIGURA EL RELOJ DEL SISTEMA PARA QUE FUNCIONE A 120MHZ USANDO EL PLL (PHASE LOCKED LOOP)
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);
 
    // HABILITA EL PUERTO GPIO QUE SE UTILIZA PARA EL LED INTEGRADO EN LA PLACA
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);

    // HABILITA EL PIN GPIO PARA EL LED (PN0).
    MAP_GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);

    // HABILITA EL PERIFERICO UTILIZADO EN ESTE EJEMPLO (TEMPORIZADOR TIMER0)
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    // ACTIVA LAS INTERRUPCIONES DEL PROCESADOR
    MAP_IntMasterEnable();

    // AQUI SE CONFIGURA EL TEMPORZADOR PARA QUE SEA PERIODICO (ES DECIR, QUE GENERE UNA INTERRUPCION AINTERVALO REGULARES) Y SE AJUSTA A LA DURACION DEL TEMPORIZADOR PARA QUE ACTIVE CADA MEDIO SEGUNDO (ASUMIENDO QUE g_ui32SysClock ES 120 MHZ
    MAP_TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    //MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock / 1); // AJUSTA EL PERIODO SEGUN SEA NECESARIO PARA 1 SEGUNDO
   //MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock / 0.5);//AJUSTA EL PERIODO SEGUN SEA NECESARIO PARA 2 SEGUNDO
   MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock / 0.2);  //AJUSTA EL PERIODO SEGUN SEA NECESARIO PARA 5 SEGUNDO
    // HABILITACION DE INTERRUPCIONES
    // SE HABILITA LA INTERRUPCION DEL TEMPORIZADOR Y EL PROPIO TEMPORIZADOR PARA QUE COMIENCE A CONTAR
    MAP_IntEnable(INT_TIMER0A);
    MAP_TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // ACTIVA EL TEMPORIZADOR
    MAP_TimerEnable(TIMER0_BASE, TIMER_A);

    // BUCLE ETERNO MIENTRAS SE EJECUTA EL TEMPORIZADOR
    while(1)
    {
    }
}

