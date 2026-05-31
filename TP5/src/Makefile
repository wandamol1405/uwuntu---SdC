obj-m += signal_mux.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

# Para Raspberry Pi, use:
# ARCH ?= arm
# CROSS_COMPILE ?= arm-linux-gnueabihf-   # Depende de si la Pi es de 32 o 64 bits

# obj-m += signal_mux.o

# # KDIR debe apuntar a la carpeta donde descargaste las cabeceras del kernel de la Pi en tu PC
# KDIR ?= /ruta/a/los/headers/del/kernel/de/la/raspberry

# all:
# 	make -C $(KDIR) M=$(PWD) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) modules

# clean:
# 	make -C $(KDIR) M=$(PWD) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) clean