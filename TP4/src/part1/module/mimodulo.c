#include <linux/module.h> /* Requerido por todos los módulos */
#include <linux/kernel.h> /* Definición de KERN_INFO */
MODULE_LICENSE("GPL");	  /*  Licencia del modulo */
MODULE_DESCRIPTION("Modulo de ejemplo para TP4 - Sistemas de Computación - UNC");
MODULE_AUTHOR("Grupo: uwuntu");

/* Función que se invoca cuando se carga el módulo en el kernel */
int modulo_lin_init(void)
{
	printk(KERN_INFO "\n");
	printk(KERN_INFO "=====================================\n");
	printk(KERN_INFO "   TP4 - MODULO CARGADO\n");
	printk(KERN_INFO "=====================================\n");
	printk(KERN_INFO " u     u  w     w  u     u  n   n  ttttt  u    u \n");
	printk(KERN_INFO " u     u  w  w  w  u     u  nn  n    t    u    u \n");
	printk(KERN_INFO " u     u  w w w w  u     u  n n n    t    u    u \n");
	printk(KERN_INFO " u     u  ww   ww  u     u  n  nn    t    u    u \n");
	printk(KERN_INFO "  uuuu     w   w    uuuu    n   n    t     uuuu  \n");
	printk(KERN_INFO "\n");
	printk(KERN_INFO "[TP4] Modulo cargado correctamente\n");
	return 0;
}

/* Función que se invoca cuando se descarga el módulo del kernel */
void modulo_lin_clean(void)
{
	printk(KERN_INFO "\n");
	printk(KERN_INFO "=====================================\n");
	printk(KERN_INFO "   TP4 - MODULO DESCARGADO\n");
	printk(KERN_INFO "=====================================\n");
	printk(KERN_INFO "   Hasta luego desde kernel space\n");
	printk(KERN_INFO "\n");
}

/* Declaración de funciones init y exit */
module_init(modulo_lin_init);
module_exit(modulo_lin_clean);
