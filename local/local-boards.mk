# List of configured boards. This boards should have a matching udev rule
# in `template/70-riotboards.rules` respecting the common configuration of
# /dev/riot/tty-$(BOARD)

# STM32 boards
STM32_BOARDS += p-nucleo-wb55
STM32_BOARDS += nucleo-l4r5zi
STM32_BOARDS += nucleo-l496zg
STM32_BOARDS += nucleo-l452re
STM32_BOARDS += nucleo-l432kc
STM32_BOARDS += nucleo-l433rc
STM32_BOARDS += stm32l476g-disco
STM32_BOARDS += p-l496g-cell02
STM32_BOARDS += b-l475e-iot01a
STM32_BOARDS += nucleo-l152re
STM32_BOARDS += nucleo-l073rz
STM32_BOARDS += b-l072z-lrwan1
STM32_BOARDS += i-nucleo-lrwan1
STM32_BOARDS += stm32l0538-disco
STM32_BOARDS += nucleo-f767zi
STM32_BOARDS += stm32f723e-disco
STM32_BOARDS += nucleo-f746zg
STM32_BOARDS += nucleo-f446re
STM32_BOARDS += nucleo-f410rb
STM32_BOARDS += nucleo-f303k8
STM32_BOARDS += nucleo-f303re
STM32_BOARDS += nucleo-f334r8
STM32_BOARDS += nucleo-f207zg
STM32_BOARDS += nucleo-f103rb
STM32_BOARDS += nucleo-f091rc
STM32_BOARDS += nucleo-f042k6
STM32_BOARDS += nucleo-f072rb
STM32_BOARDS += nucleo-f070rb
STM32_BOARDS += nucleo-f030r8

# NRF2 Boards
NRF5x_BOARDS += nrf52840-mdk
NRF5x_BOARDS += nrf52dk
NRF5x_BOARDS += nrf52840dk
NRF5x_BOARDS += dwm1001

# NXP Boards
NXP_BOARDS += frdm-kw41z
NXP_BOARDS += frdm-k64f
NXP_BOARDS += pba-d-01-kw2x
NXP_BOARDS += mbed_lpc1768
NXP_BOARDS += usb-kw41z

# Iotlab
IOTLAB_BOARDS += iotlab-m3

# Atmel
ATMEL_BOARDS += samr21-xpro
ATMEL_BOARDS += samr34-xpro
ATMEL_BOARDS += atmega256rfr2-xpro
ATMEL_BOARDS += hamilton

# TI
TI_BOARDS += z1
TI_BOARDS += remote-reva
TI_BOARDS += remote-revb
TI_BOARDS += ek-lm4f120xl
TI_BOARDS += cc2538dk

# RISC boards
RISC_BOARDS += hifive1b

# ARDUINO boards
ARDUINO_BOARDS += arduino-mega2560
ARDUINO_BOARDS += arduino-uno
ARDUINO_BOARDS += arduino-due
ARDUINO_BOARDS += arduino-zero

# EFM32 boards
EFM32_BOARDS += slstk3402a

# ESP
ESP_BOARDS += esp32-wroom-32

# Local Boards
LOCAL_BOARDS += $(STM32_BOARDS)
LOCAL_BOARDS += $(NRF5x_BOARDS)
LOCAL_BOARDS += $(NXP_BOARDS)
LOCAL_BOARDS += $(IOTLAB_BOARDS)
LOCAL_BOARDS += $(ATMEL_BOARDS)
LOCAL_BOARDS += $(TI_BOARDS)
LOCAL_BOARDS += $(RISC_BOARDS)
LOCAL_BOARDS += $(ARDUINO_BOARDS)
LOCAL_BOARDS += $(EFM32_BOARDS)
LOCAL_BOARDS += $(ESP_BOARDS)
