#include <linux/module.h>  // Necesario para todos los módulos
#include <linux/kernel.h>  // KERN_INFO
#include <linux/init.h>    // Macros __init y __exit
#include <linux/fs.h>      // Funciones y estructuras de file_operations
#include <linux/uaccess.h> // copy_to_user y copy_from_user
#include <linux/timer.h>   // Estructuras y funciones de Kernel Timers
#include <linux/jiffies.h> // Para el manejo de ticks (HZ)

#define SAMPLE_PERIOD_MS 1000 // Período de muestreo inicial en milisegundos

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Grupo UwUntu");
MODULE_DESCRIPTION("SignalMux: CDD para sensado de dos señales simuladas (senoidal y cuadrada) - TP5 de Sistemas de Computacion");

#define DEVICE_NAME "sig_mux" // Nombre del dispositivo que aparecerá en /dev
static int major_number;

/* --- Variables Globales para el TP --- */
static struct timer_list timer;
static int chosen_signal = 0; // 0 = Señal A, 1 = Señal B

// Variables para simular el hardware
static const int sin_table[12] = {50, 75, 93, 100, 93, 75, 50, 25, 7, 0, 7, 25};
static int index_sin = 0;

// Variables dinamicas configurables desde la web
static int amplitude_config = 100;
static int frequency_config = 1;
static int square_phase = 0;

// Valores instantaneos que leer el comando 'cat'
static int sin = 0;
static int square_waveform = 0;
static int counter_time = 0; // Contador para simular el paso del tiempo y cambiar las señales cada segundo

/* --- Función del Kernel Timer (Se ejecuta cada 1 segundo) --- */
/* --- En la función del Kernel Timer (timer_callback) --- */
static void timer_callback(struct timer_list *t)
{
    counter_time++;

    /* Senoidal */

    sin = (sin_table[index_sin] * amplitude_config) / 100;

    index_sin =
        (index_sin + frequency_config) %
        ARRAY_SIZE(sin_table);

    /* Cuadrada */

    square_phase += frequency_config;

    if (((square_phase / 6) % 2) == 0)
        square_waveform = amplitude_config;
    else
        square_waveform = 0;

    mod_timer(
        &timer,
        jiffies + msecs_to_jiffies(SAMPLE_PERIOD_MS));
}

/* --- Operación de Lectura (read) --- */
// Se ejecuta cuando el usuario hace un "cat /dev/signal_mux" o lee desde su script
static ssize_t device_read(struct file *filp, char __user *buffer, size_t len, loff_t *offset)
{
    char user_message[32];
    int size;
    int send_value;

    // Si el offset es mayor a 0, significa que ya leímos todo en el ciclo anterior
    if (*offset > 0)
        return 0;

    // Dependiendo de lo que eligió el usuario, preparamos el dato de la señal correspondiente
    if (chosen_signal == 0)
    {
        send_value = sin;
    }
    else
    {
        send_value = square_waveform;
    }

    // Convertimos el número a texto para que el Espacio de Usuario lo lea fácil
    size = snprintf(user_message, sizeof(user_message), "%d\n", send_value);

    // Copia segura desde el espacio de Kernel al espacio de Usuario
    if (copy_to_user(buffer, user_message, size) != 0)
    {
        return -EFAULT;
    }

    *offset += size; // Actualizamos el offset para no entrar en un bucle infinito de lectura
    return size;
}

/* --- Operación de Escritura (write) --- */
static ssize_t device_write(struct file *filp, const char *buffer, size_t len, loff_t *off)
{
    char kbuf[16];
    int value_received = 0;

    if (len > 15)
        len = 15;
    if (copy_from_user(kbuf, buffer, len))
        return -EFAULT;
    kbuf[len] = '\0';

    // Evaluamos el primer caracter (el prefijo)
    switch (kbuf[0])
    {
    case 'C': // Conmutación de canal
        chosen_signal = kbuf[1] - '0';
        printk(KERN_INFO "[SignalMux] Canal cambiado a: %d\n", chosen_signal);
        break;

    case 'A': // Ajuste de Amplitud
        // Convertimos el resto de la cadena a un entero (ej: "A250" -> 250)
        sscanf(&kbuf[1], "%d", &value_received);
        if (value_received >= 0)
        {
            amplitude_config = value_received;
        }
        printk(KERN_INFO "[SignalMux] Nueva Amplitud: %d\n", amplitude_config);
        break;

        // Podés agregar un caso 'F' para el período/frecuencia si querés
    case 'F':
        sscanf(&kbuf[1], "%d", &value_received);

        if (value_received > 0)
            frequency_config = value_received;

        printk(KERN_INFO,
               "[SignalMux] Frecuencia configurada: %d\n",
               frequency_config);

        break;
    }
    return len;
}

/* --- Mapeo de Operaciones de Archivo --- */
static struct file_operations fops = {
    .read = device_read,
    .write = device_write,
};

/* --- Inicialización del Módulo (__init) --- */
static int __init mi_modulo_init(void)
{
    // Registrar el Driver de Caracteres de forma clásica (estilo drv3/drv4 de tus PDFs)
    major_number = register_chrdev(0, DEVICE_NAME, &fops);
    if (major_number < 0)
    {
        printk(KERN_ALERT "[SignalMux]: Error al registrar el dispositivo\n");
        return major_number;
    }
    printk(KERN_INFO "[SignalMux]: Registrado con exito. Major Number: %d\n", major_number);

    // Inicializar y encender el Kernel Timer por primera vez
    timer_setup(&timer, timer_callback, 0);
    mod_timer(&timer, jiffies + msecs_to_jiffies(SAMPLE_PERIOD_MS)); // Primera alarma en 1s

    return 0;
}

/* --- Limpieza del Módulo (__exit) --- */
static void __exit mi_modulo_exit(void)
{
    // Apagar el timer para que no intente ejecutar código inexistente
    timer_shutdown(&timer);

    // Desregistrar el dispositivo de caracteres
    unregister_chrdev(major_number, DEVICE_NAME);
    printk(KERN_INFO "[SignalMux]: Modulo removido correctamente\n");
}

module_init(mi_modulo_init);
module_exit(mi_modulo_exit);