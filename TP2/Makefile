# ==============================
# CONFIG
# ==============================

CC = gcc
CFLAGS = -Wall -Wextra -O0 -g
ASFLAGS = --64 -g

TARGET = c/program

SRC_C = c/main_i2.c c/file_reader.c
SRC_ASM = c/process_value.s

OBJ = c/main_i2.o c/file_reader.o c/process_value.o

DATA_FILE = data/gini_values.txt

# ==============================
# UX / OUTPUT
# ==============================

MAKEFLAGS += --no-print-directory

BOLD   = \033[1m
GREEN  = \033[32m
YELLOW = \033[33m
BLUE   = \033[34m
RED    = \033[31m
RESET  = \033[0m

define log
	@printf "$(BOLD)$(BLUE)[INFO]$(RESET) %s\n" "$(1)"
endef

define ok
	@printf "$(BOLD)$(GREEN)[OK]$(RESET) %s\n" "$(1)"
endef

define warn
	@printf "$(BOLD)$(YELLOW)[WARN]$(RESET) %s\n" "$(1)"
endef

# ==============================
# PHONY
# ==============================

.PHONY: all run debug clean

# ==============================
# DEFAULT
# ==============================

all: run

# ==============================
# DATA GENERATION
# ==============================

$(DATA_FILE):
	$(call log,Generando archivo de datos...)
	@python3 python/data_formatter.py
	$(call ok,Archivo generado: $(DATA_FILE))

# ==============================
# COMPILATION
# ==============================

c/main_i2.o: c/main_i2.c
	$(call log,Compilando C: $<)
	@$(CC) $(CFLAGS) -c $< -o $@
	$(call ok,Objeto generado: $@)

c/file_reader.o: c/file_reader.c
	$(call log,Compilando C: $<)
	@$(CC) $(CFLAGS) -c $< -o $@
	$(call ok,Objeto generado: $@)

c/process_value.o: c/process_value.s
	$(call log,Ensamblando ASM: $<)
	@as $(ASFLAGS) -o $@ $<
	$(call ok,Objeto generado: $@)

# ==============================
# LINKING
# ==============================

$(TARGET): $(OBJ)
	$(call log,Linkeando binario: $(TARGET))
	@$(CC) $(CFLAGS) -o $@ $(OBJ)
	$(call ok,Binario listo: $(TARGET))

# ==============================
# RUN
# ==============================

run: $(DATA_FILE) $(TARGET)
	@printf "\n$(BOLD)$(GREEN)============================= $(RESET)\n"
	@printf "$(BOLD)$(GREEN) Ejecutando programa$(RESET)\n"
	@printf "$(BOLD)$(GREEN)============================= $(RESET)\n\n"
	@./$(TARGET)

# ==============================
# DEBUG
# ==============================

debug: $(DATA_FILE) $(TARGET)
	$(call warn,Iniciando GDB...)
	@gdb ./$(TARGET)

# ==============================
# CLEAN
# ==============================

clean:
	$(call warn,Limpiando archivos generados...)
	@rm -f c/*.o $(TARGET)
	@rm -f $(DATA_FILE)
	$(call ok,Limpieza completada)