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
#include "driverlib/adc.h"       // Funciones para controlar el ADC (configuración, inicio de conversiones)
#include <string.h>
#define duty 4095 // ciclo de trabajo maximo del pwm en este caso debe de ser el tamaño de la resolucion de bist del adc 12bits
#define MAX_BUFFER_SIZE 100  // Tamaño máximo del buffer para almacenar la frase

uint32_t ui32SysClock;           // Variable para almacenar la frecuencia del reloj del sistema
char uartBuffer[MAX_BUFFER_SIZE]; // Buffer para almacenar la frase recibida
volatile uint8_t bufferIndex = 0; // Índice del buffer

uint32_t ui32SysClock;  // Variable para almacenar la frecuencia del reloj del sistema
uint8_t estado;         //variable para cambiar el estado del led en la interrupcion
uint32_t width;        // Variable para almacenar el ancho del pulso de PWM
uint32_t adcValue;
volatile uint32_t counter = 0;
static void configureSysClock(void);
static void config_timer(void);
static void config_uart(void);
static void config_pwm(void);           // Inicializar PWM
static void config_adc(void);        // Inicializa el ADC
static void config_gpio(void);
uint32_t ReadADC(void);               //lectura del adc
int main(void) {
    configureSysClock();  // Configurar el sistema a 120 MHz
    config_timer();       // configuracion del temporizador con interrupción
    config_uart();        // configuracion del UART
    config_pwm();         // configuracion del PWM
    config_adc();         // configuracion del adc el ADC
    config_gpio();        // configuracion de los GPIOs
    UARTprintf("Sistema UART listo para recibir frases...\r\n");

    // Bucle principal (no se necesita hacer nada aquí ya que la interrupción maneja el LED)
    while (1) {

        //adcValue = ReadADC(); // Llamar a la función para leer el ADC
        //width=adcValue;
        //UARTprintf("%d\r\n", adcValue); // Enviar el valor del ADC
        //PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, width);
        //GPIOPinWrite(GPIO_PORTN_BASE,GPIO_PIN_2, GPIO_PIN_2);
        //if(adcValue < 1)
        //{
           //PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, 1);
        //}
        //SysCtlDelay(ui32SysClock/12); // Ajustar el valor de delay según sea necesario
        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1)==0){
    		counter++;
    		while (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
                // Espera activa
            	}
            	// Esperar un pequeño tiempo para evitar rebotes del botón
            	SysCtlDelay(1000000);
            	 if (counter >= 3){
            		counter =0;
            	}
    	}
        //UARTprintf("%d\r\n", counter);
    }
}
// Función de manejo de la interrupción del temporizador
void Timer0IntHandler(void) {
    // Limpiar la interrupción del temporizador para poder seguir generando interrupciones
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    //Alternar el estado del LED en el pin PF1
    //estado = GPIOPinRead(GPIO_PORTN_BASE, GPIO_PIN_1);
    //GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, estado ^ GPIO_PIN_1);  // Alternar el LED
    switch (counter) {
            case 1:
                UARTprintf("motor1\r\n");
                break;
            case 2:
                UARTprintf("motor2\r\n");
                break;
            case 0:
                 UARTprintf("apagado\r\n");
                break;
            default:
                break;
        }

}
// Envio de datos para el uart mediante interrucpcion 
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
            UARTprintf("%s\r\n", uartBuffer);  // Imprimir la frase recibida
            if (strcmp(uartBuffer, "buzzer") == 0)
            {
                GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_4, GPIO_PIN_4);
            }
            else 
            {
                GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_4, 0x00);
            }
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

// Leer valor del ADC
uint32_t ReadADC(void) {
    // Disparar el ADC
    ADCProcessorTrigger(ADC0_BASE, 3);

    // Esperar a que la conversión esté completa
    while (!ADCIntStatus(ADC0_BASE, 3, false)) {}

    // Leer el valor del ADC
    ADCSequenceDataGet(ADC0_BASE, 3, &adcValue);

    // Limpiar la bandera de interrupción
    ADCIntClear(ADC0_BASE, 3);

    return adcValue; // Retornar el valor leído del ADC
}
// Configurar el Timer0 para generar una interrupción periódica
static void config_timer(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);  // Habilitar el reloj para Timer0

    // Configurar el temporizador 0 como un temporizador periódico de 32 bits
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

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
// Configurar UART0
static void config_uart(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA); // Habilitar el reloj para GPIO A
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);  // Habilitar el reloj para UART0

    // Configurar los pines para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX); // Configurar PA0 como RX
    GPIOPinConfigure(GPIO_PA1_U0TX); // Configurar PA1 como TX
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1); // Configurar como UART

    // Configurar UART0 a 115200 baudios, 8 bits de datos, sin paridad, 1 bit de parada
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
// Inicializar ADC
void config_adc(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE); // Habilitar el reloj para el puerto GPIO E (donde está PE3)
    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0); // Habilitar el reloj para el módulo ADC0

    // Configurar el pin PE3 como entrada analógica para el ADC
    GPIOPinTypeADC(GPIO_PORTE_BASE, GPIO_PIN_3); // Configurar el pin como entrada de ADC

    // Esperar a que el módulo ADC esté listo
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_ADC0)) {}

    // Configurar el secuenciador 3 para el ADC
    ADCSequenceConfigure(ADC0_BASE, 3, ADC_TRIGGER_PROCESSOR, 0); // Configurar secuenciador 3
    ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH0 | ADC_CTL_IE | ADC_CTL_END); // Configurar paso 0
    ADCSequenceEnable(ADC0_BASE, 3); // Habilitar el secuenciador 3
    ADCIntClear(ADC0_BASE, 3); // Limpiar interrupciones del secuenciador 3
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
    //
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_2);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_4);
    //
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_1);//boton1 interno
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
}
//
static void configureSysClock(void) {
    // Configurar el sistema a 120 MHz usando PLL
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_240), 120000000);
}